"""Sphinx directives for embedding Wokwi diagrams in documentation.

This module provides two main directives:
1. WokwiDirective: Embed a single Wokwi diagram with explicit diagram/firmware URLs
2. WokwiExampleDirective: Embed Arduino examples with auto-discovery from ci.yml

Both directives support tabbed interfaces for displaying multiple targets/variations.
"""

from __future__ import annotations

from typing import List
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from .helpers import css_size, get_static_path, loading_choice, url_join
from .nodes import WokwiNode, WokwiTabsNode, TabListNode, TabPanelNode
from os import path



class WokwiDirective(Directive):
    """Directive to embed a single Wokwi diagram with explicit URLs.

    Usage:
        .. wokwi:: [name]
           :diagram: <url-to-diagram.json>
           :firmware: <url-to-firmware.bin>
           :width: 100%
           :height: 500px
           :loading: lazy
           :allowfullscreen:
           :tab: ESP32

    Options:
        name (optional text arg): Name/label for the diagram (used in tabs)
        diagram: URL to Wokwi diagram JSON file (required)
        firmware: URL to compiled firmware binary (required)
        width: CSS width value (default: 100%)
        height: CSS height value (default: 500px)
        loading: iframe loading strategy - lazy, eager, or auto (default: lazy)
        title: Title text for the iframe
        allowfullscreen: Enable fullscreen mode
        tab: Tab label (alternative to name argument)
        class: CSS class names to apply

    Returns:
        WokwiNode containing the diagram configuration
    """
    has_content = False
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    option_spec = {
        "name": directives.unchanged,
        "tab": directives.unchanged,
        "diagram": directives.uri,
        "firmware": directives.uri,
        "width": css_size,
        "height": css_size,
        "title": directives.unchanged,
        "allowfullscreen": directives.flag,
        "loading": loading_choice,
        "class": directives.class_option,
    }

    def run(self):
        env = self.state.document.settings.env
        cfg = env.app.config

        diagram_url = self.options.get("diagram")
        firmware_url = self.options.get("firmware")
        if not diagram_url or not firmware_url:
            raise self.error("wokwi directive: :diagram: and :firmware: are required (UF2/bin).")

        node = WokwiNode()
        node["iframe_page"] = cfg.docs_embed_wokwi_viewer_url
        node["iframe_page_params"] = {"api": "1"}  # Enable Wokwi API
        node["diagram_url"] = diagram_url
        node["firmware_url"] = firmware_url
        node["width"] = self.options.get("width", cfg.docs_embed_default_width)
        node["height"] = self.options.get("height", cfg.docs_embed_default_height)
        node["title"] = self.options.get("title", "Wokwi simulation")
        node["allowfullscreen"] = cfg.docs_embed_default_allowfullscreen if "allowfullscreen" not in self.options else True
        node["loading"] = self.options.get("loading", cfg.docs_embed_default_loading)
        node["classes"] = ["wokwi-embed"] + self.options.get("class", [])
        node["static_path"] = get_static_path(env.docname)
        node["suppress_header"] = False

        tab_label = (
            self.options.get("name")
            or self.options.get("tab")
            or (self.arguments[0].strip() if self.arguments else None)
        )
        if tab_label:
            node["tab_label"] = tab_label

        return [node]


class WokwiExampleDirective(Directive):
    """Directive to embed Arduino examples with auto-discovered targets.

    Embeds Wokwi simulations for Arduino ESP32 examples with multiple target support.
    Automatically discovers targets from ci.yml and creates tabbed interface for each.

    Usage:
        .. wokwi-example:: libraries/ESP32/examples/GPIO/Blink
           :width: 100%
           :height: 500px
           :allowfullscreen:

    Expected Directory Structure:
        Arduino Source:
            libraries/ESP32/examples/GPIO/Blink/
            ├── Blink.ino
            └── ci.yml

        Built Artifacts (_static/):
            _static/libraries/ESP32/examples/GPIO/Blink/
            ├── ci.yml (copied by the build process)
            ├── launchpad.toml (optional)
            ├── esp32/
            │   ├── Blink.ino.merged.bin
            │   └── diagram.esp32.json
            └── esp32s2/
                ├── Blink.ino.merged.bin
                └── diagram.esp32s2.json

    Configuration (in conf.py):
        docs_embed_public_root = "https://example.com"
        docs_embed_binaries_dir = "_static"
        docs_embed_esp_launchpad_url = "https://espressif.github.io/esp-launchpad"
        docs_embed_github_base_url = "https://github.com/espressif/esp-idf"
        docs_embed_github_branch = "master"
        docs_embed_skip_validation = False

    Features:
        - Reads ci.yml to auto-discover supported targets (ESP32, ESP32-S2, etc.)
        - Creates tabs for each target's simulation
        - Shows source code tab with .ino file content
        - Optionally links to ESP Launchpad configuration
        - Optionally links to GitHub source code
        - Validates file existence (configurable)

    Returns:
        WokwiTabsNode containing tabbed interface with code and diagram tabs
    """
    required_arguments = 1  # path to example directory
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
        "width": css_size,
        "height": css_size,
        "allowfullscreen": directives.flag,
        "loading": directives.unchanged,
        "class": directives.class_option,
    }

    has_content = False

    def run(self):
        import yaml

        env = self.state.document.settings.env
        app = env.app
        cfg = app.config

        # Example: libraries/ESP32/examples/GPIO/Blink -> sketch name: Blink
        example_path = self.arguments[0].strip()
        sketch_name = example_path.split("/")[-1]
        docs_embed_esp32_relative_root = "../.."  # shift to the project root

        docs_embed_public_root = getattr(cfg, "docs_embed_public_root", None)
        if not docs_embed_public_root:
            raise self.error("wokwi-example: 'docs_embed_public_root' must be configured in ENV or conf.py")

        docs_embed_binaries_dir = getattr(cfg, "docs_embed_binaries_dir", None)
        if not docs_embed_binaries_dir:
            raise self.error("wokwi-example: 'docs_embed_binaries_dir' must be configured in ENV or conf.py")
        docs_embed_binaries_dir = path.normpath(docs_embed_binaries_dir)

        # Build path to ci.yml
        ci_yml_path = path.join(env.srcdir, docs_embed_esp32_relative_root, example_path, "ci.yml")
        if not path.isfile(ci_yml_path):
            raise self.error(f"wokwi-example: ci.yml not found at {ci_yml_path}")

        # Load ci.yml
        try:
            with open(ci_yml_path, "r") as f:
                ci_data = yaml.safe_load(f)
        except Exception as e:
            raise self.error(f"wokwi-example: failed to parse ci.yml: {e}")

        # Extract targets
        upload_binary = ci_data.get("upload-binary", {})
        targets = upload_binary.get("targets", [])

        if not targets:
            raise self.error(f"wokwi-example: no targets found in ci.yml at {ci_yml_path}")

        # Get configuration
        skip_validation = getattr(cfg, "docs_embed_skip_validation", False)

        # Create WokwiNode instances for each target
        wokwi_nodes: List[WokwiNode] = []
        for target in targets:
            firmware_path = url_join(docs_embed_binaries_dir, example_path, target, f"{sketch_name}.ino.merged.bin")
            firmware_url = url_join(docs_embed_public_root, firmware_path)

            diagram_path = url_join(docs_embed_binaries_dir, example_path, target, f"diagram.{target}.json")
            diagram_url = url_join(docs_embed_public_root, diagram_path)

            # Validate files exist (unless skip_validation is set)
            if not skip_validation:
                firmware_full_path = url_join(env.srcdir, "..", firmware_path)
                if not path.isfile(firmware_full_path):
                    raise self.error(
                        f"wokwi-example: firmware file not found at {firmware_full_path}. "
                        f"Set 'docs_embed_skip_validation = True' in conf.py to bypass this check.")

                diagram_full_path = url_join(env.srcdir, "..", diagram_path)
                if not path.isfile(diagram_full_path):
                    raise self.error(
                        f"wokwi-example: diagram file not found at {diagram_full_path}. "
                        f"Set 'docs_embed_skip_validation = True' in conf.py to bypass this check.")

            # Create tab label (e.g., "ESP32", "ESP32-S2")
            if target.startswith('esp32'):
                base = target[5:]
                tab_label = f"ESP32-{base.upper()}" if base else "ESP32"
            else:
                tab_label = target.upper()

            # Create WokwiNode
            wn = WokwiNode()
            wn["iframe_page"] = cfg.docs_embed_wokwi_viewer_url
            wn["iframe_page_params"] = {"api": "1"}  # Enable Wokwi API
            wn["diagram_url"] = diagram_url
            wn["firmware_url"] = firmware_url
            wn["width"] = self.options.get("width", getattr(cfg, "docs_embed_default_width"))
            wn["height"] = self.options.get("height", getattr(cfg, "docs_embed_default_height"))
            wn["title"] = f"Wokwi simulation — {tab_label}"
            wn["allowfullscreen"] = getattr(cfg, "docs_embed_default_allowfullscreen") if "allowfullscreen" not in self.options else True
            wn["loading"] = self.options.get("loading", getattr(cfg, "docs_embed_default_loading"))
            wn["classes"] = ["wokwi-embed", "from-example"] + self.options.get("class", [])
            wn["static_path"] = get_static_path(env.docname)

            wn["tab_label"] = tab_label
            wn["suppress_header"] = True  # rendered inside tabs

            wokwi_nodes.append(wn)

        # Now create the tab structure
        code_panels: List[TabPanelNode] = []
        wokwi_panels: List[TabPanelNode] = []

        ino_filename = f"{sketch_name}.ino"
        ino_full_path = path.join(env.srcdir, docs_embed_esp32_relative_root, example_path, ino_filename)
        if path.isfile(ino_full_path):
            with open(ino_full_path, 'r', encoding='utf-8') as f:
                source_content = f.read()

            code_block = nodes.literal_block(source_content, source_content)
            code_block['language'] = 'arduino'
            code_block['classes'] = ['highlight']

            source_panel = TabPanelNode()
            source_panel["label"] = ino_filename
            source_panel["active"] = True
            source_panel.children = [code_block]
            code_panels.append(source_panel)

        for i, wn in enumerate(wokwi_nodes):
            panel = TabPanelNode()
            panel["label"] = wn["tab_label"]
            panel["active"] = False
            panel.children = [wn]
            wokwi_panels.append(panel)

        # Combine all panels
        panels = code_panels + wokwi_panels

        # Create tabs structure
        serial = env.new_serialno("wokwi-tabs") if env and hasattr(env, "new_serialno") else id(self)
        root_id = f"wokwi-tabs-{serial}"

        tablist = TabListNode()
        tablist["root_id"] = root_id
        labels = [p.get("label") or f"Tab {i+1}" for i, p in enumerate(panels)]
        tablist["labels"] = labels
        panel_ids = [f"{root_id}-panel-{i}" for i in range(len(panels))]
        tablist["panel_ids"] = panel_ids

        # Separate labels for code and wokwi
        tablist["tabs_code"] = [p.get("label") for p in code_panels]
        tablist["tabs_wokwi"] = [p.get("label") for p in wokwi_panels]

        tablist["static_path"] = get_static_path(env.docname)

        # Link to ESP Launchpad if launchpad.toml exists (optional)
        launchpad_path = path.join(docs_embed_binaries_dir, example_path, "launchpad.toml")
        launchpad_full_path = path.join(env.srcdir, "..", launchpad_path)
        if path.isfile(launchpad_full_path):
            launchpad_url = url_join(docs_embed_public_root, launchpad_path)
            launchpad_base_url = getattr(env.app.config, "docs_embed_esp_launchpad_url", "")

            # Properly construct URL with query parameters
            parsed = urlparse(launchpad_base_url.rstrip('/'))
            query_params = parse_qs(parsed.query)
            query_params['flashConfigURL'] = [launchpad_url]
            new_query = urlencode(query_params, doseq=True)

            # Reconstruct URL with new query parameters
            new_parsed = parsed._replace(query=new_query)
            tablist["launchpad_href"] = urlunparse(new_parsed)

        # Link to GitHub source .ino file
        github_base = getattr(cfg, "docs_embed_github_base_url")
        github_branch = getattr(cfg, "docs_embed_github_branch")
        if github_base and github_branch:
            tablist["github_href"] = url_join(github_base, "tree", github_branch, example_path, f"{sketch_name}.ino")

        for pid, panel in zip(panel_ids, panels):
            panel["panel_id"] = pid

        tabs_root = WokwiTabsNode()
        tabs_root.children = [tablist] + panels
        if "class" in self.options:
            tabs_root["classes"] = self.options["class"]
        tabs_root["variant"] = "example"

        return [tabs_root]

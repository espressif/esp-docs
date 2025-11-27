"""Sphinx plugin for Wokwi diagram embedding in documentation.

This module provides a Sphinx extension for embedding interactive Wokwi diagrams
and LaunchPad configurations in documentation. It handles configuration management,
directive registration, and node processing for multiple output formats.

Configuration:
    The plugin can be configured via:
    1. Environment variables (prefixed with uppercase config key name)
    2. conf.py settings in your Sphinx configuration

    See CONFIG_DEFAULTS for all available configuration options.
"""

from __future__ import annotations

import os
from pathlib import Path

from esp_docs.esp_extensions.docs_embed.sphinx.helpers import get_static_path

from .sphinx.nodes import WokwiNode, WokwiTabsNode, TabListNode, TabPanelNode
from .sphinx.directives import WokwiDirective, WokwiExampleDirective
from .sphinx import html
from sphinx.application import Sphinx


# Configuration defaults with their config keys
# Format: "config_key": default_value
# You can define these using environment variables or in conf.py
# None means that has to be defined externally (does not have a default)
CONFIG_DEFAULTS = {
    "docs_embed_wokwi_viewer_url": "https://wokwi.com/experimental/viewer",
    "docs_embed_default_width": "100%",
    "docs_embed_default_height": "500px",
    "docs_embed_default_allowfullscreen": True,
    "docs_embed_default_loading": "lazy",
    "docs_embed_esp_launchpad_url": "https://espressif.github.io/esp-launchpad",
    "docs_embed_about_wokwi_url": "https://docs.wokwi.com",
    "docs_embed_skip_validation": False,
    "docs_embed_github_base_url": None,  # Deduced from Github ENV in CI
    "docs_embed_github_branch": None,  # Deduced from Github ENV in CI
    "docs_embed_public_root": None,  # Deduced from Github ENV in CI
    "docs_embed_binaries_dir": None,  # Deduced from Github ENV in CI
}


def _override_config_from_env(app: Sphinx, config) -> None:
    """Override configuration values from environment variables.

    Checks for environment variables matching each config key name in uppercase.
    For example: docs_embed_github_branch -> DOCS_EMBED_GITHUB_BRANCH

    Required config values (set to None) must be provided via environment variables
    or will raise a RuntimeError.

    Args:
        app: Sphinx application instance
        config: Sphinx configuration object

    Raises:
        RuntimeError: If a required config value is not set and no env var provided
    """
    for config_key, config_val in CONFIG_DEFAULTS.items():
        env_var = config_key.upper()
        env_value = os.environ.get(env_var)
        if env_value is not None:
            # Handle boolean conversion for allowfullscreen
            if config_key == "docs_embed_default_allowfullscreen":
                env_value = env_value.lower() in ("true", "1", "yes", "on")
            setattr(config, config_key, env_value)


def _register_static(app: Sphinx) -> None:
    """Register static assets (CSS and JavaScript) for the Wokwi embed plugin.

    Adds the plugin's static files to Sphinx's html_static_path and registers
    the wokwi_embed.css and wokwi_embed.js files for inclusion in HTML output.

    Args:
        app: Sphinx application instance
    """
    pkg_static = Path(__file__).parent / "_static"
    if getattr(app.config, "html_static_path", None) is None:
        app.config.html_static_path = []
    if str(pkg_static) not in app.config.html_static_path:
        app.config.html_static_path.append(str(pkg_static))
    app.add_css_file("wokwi_embed.css")


def _add_wokwi_modules(app: Sphinx, pagename: str, templatename: str, context: dict, doctree) -> None:
    """Add import map and module scripts for Wokwi client library.

    Args:
        app: Sphinx application instance
        pagename: Name of the page being rendered
        templatename: Name of the template being used
        context: HTML context dictionary
        doctree: Document tree
    """
    # Calculate the correct static path based on page depth
    static_path = get_static_path(pagename)

    # Add import map and module scripts via metatags
    metatags = context.get("metatags", "")
    wokwi_modules = f"""
        <script type="importmap">
        {{
          "imports": {{
            "wokwi-client-js": "https://cdn.jsdelivr.net/npm/@wokwi/client@0.19.0/dist/wokwi-client.browser.js"
          }}
        }}
        </script>
        <script type="module" src="{static_path}wokwi_embed.js"></script>
    """
    metatags = wokwi_modules + metatags
    context["metatags"] = metatags


def setup(app: Sphinx) -> dict:
    """Setup the Wokwi embed Sphinx extension.

    Registers all configuration values, directives, nodes, and event handlers.
    This function is called automatically by Sphinx when loading the extension.

    Args:
        app: Sphinx application instance

    Returns:
        Dictionary with extension metadata (version, parallel safety flags)
    """
    # Register all config values with their defaults
    for config_key, default_value in CONFIG_DEFAULTS.items():
        app.add_config_value(config_key, default_value, "env")

    # Register nodes with their visitor methods for each output format
    # WokwiNode: Main diagram node
    app.add_node(
        WokwiNode,
        html=(html.visit_wokwi_html, html.depart_wokwi_html),
        singlehtml=(html.visit_wokwi_html, html.depart_wokwi_html),
        dirhtml=(html.visit_wokwi_html, html.depart_wokwi_html),
        epub=(html.visit_wokwi_html, html.depart_wokwi_html),
        text=(html.visit_wokwi_text, html.depart_wokwi_text),
        latex=(html.visit_wokwi_latex, html.depart_wokwi_latex),
        man=(html.visit_wokwi_text, html.depart_wokwi_text),
    )

    # WokwiTabsNode: Tabbed diagram view
    app.add_node(
        WokwiTabsNode,
        html=(html.visit_wokwi_tabs_html, html.depart_wokwi_tabs_html),
        singlehtml=(html.visit_wokwi_tabs_html, html.depart_wokwi_tabs_html),
        dirhtml=(html.visit_wokwi_tabs_html, html.depart_wokwi_tabs_html),
        epub=(html.visit_wokwi_tabs_html, html.depart_wokwi_tabs_html),
        text=(html.visit_wokwi_tabs_text, html.depart_wokwi_tabs_text),
        latex=(html.visit_wokwi_tabs_latex, html.depart_wokwi_tabs_latex),
        man=(html.visit_wokwi_tabs_text, html.depart_wokwi_tabs_text),
    )

    # TabListNode: Container for tab headers
    app.add_node(
        TabListNode,
        html=(html.visit_tablist_html, html.depart_tablist_html),
        singlehtml=(html.visit_tablist_html, html.depart_tablist_html),
        dirhtml=(html.visit_tablist_html, html.depart_tablist_html),
        epub=(html.visit_tablist_html, html.depart_tablist_html),
        text=(html.visit_tablist_text, html.depart_tablist_text),
        latex=(html.visit_tablist_latex, html.depart_tablist_latex),
        man=(html.visit_tablist_text, html.depart_tablist_text),
    )

    # TabPanelNode: Individual tab content
    app.add_node(
        TabPanelNode,
        html=(html.visit_tabpanel_html, html.depart_tabpanel_html),
        singlehtml=(html.visit_tabpanel_html, html.depart_tabpanel_html),
        dirhtml=(html.visit_tabpanel_html, html.depart_tabpanel_html),
        epub=(html.visit_tabpanel_html, html.depart_tabpanel_html),
        text=(html.visit_tabpanel_text, html.depart_tabpanel_text),
        latex=(html.visit_tabpanel_latex, html.depart_tabpanel_latex),
        man=(html.visit_tabpanel_text, html.depart_tabpanel_text),
    )

    # Register directives
    app.add_directive("wokwi", WokwiDirective)
    app.add_directive("wokwi-example", WokwiExampleDirective)

    # Register event handlers
    app.connect("config-inited", _override_config_from_env)
    app.connect("builder-inited", _register_static)
    app.connect("html-page-context", _add_wokwi_modules)

    return {
        "version": "0.0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

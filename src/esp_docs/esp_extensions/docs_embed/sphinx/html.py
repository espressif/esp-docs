"""Visitor functions for rendering Wokwi diagram nodes in various output formats.

This module provides visitor and departure functions for rendering custom AST nodes
in different output formats:
- HTML: Full interactive UI with tabs, buttons, and styling
- Text: Plain text fallback with URLs and labels
- LaTeX: PDF-compatible rendering with minimal formatting

Each node type has visitor/departure function pairs for each output format.
"""

from __future__ import annotations

from typing import Optional
from docutils import nodes as _n

from .helpers import _escape, iframe_url
from .nodes import WokwiNode, WokwiTabsNode, TabListNode, TabPanelNode


def _render_iframe_attrs(node: WokwiNode) -> tuple[str, str, str]:
    """Render iframe HTML attributes from WokwiNode configuration.

    Args:
        node: WokwiNode containing diagram and viewer configuration

    Returns:
        Tuple of (attribute_string, allowfullscreen_string, viewer_url)
        - attribute_string: Space-separated iframe attributes (src, width, height, etc.)
        - allowfullscreen_string: " allowfullscreen" if enabled, else ""
        - viewer_url: Complete iframe URL with diagram and firmware parameters
    """
    iframe_page = node.get("iframe_page", "")
    iframe_page_params = node.get("iframe_page_params", {})
    diagram_url = node.get("diagram_url", "")
    firmware_url = node.get("firmware_url", "")
    width = node.get("width")
    height = node.get("height")
    loading = node.get("loading", "lazy")
    classes = " ".join(node.get("classes", []))
    viewer_url = iframe_url(iframe_page, diagram_url, firmware_url, iframe_page_params)

    attrs = {
        "src": viewer_url,
        "width": _escape(str(width), quote=True),
        "height": _escape(str(height), quote=True),
        "loading": _escape(str(loading), quote=True),
        "class": _escape(classes, quote=True),
        "frameborder": "0",
    }
    attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items() if v)
    allow = " allowfullscreen" if bool(node.get("allowfullscreen")) else ""
    return attr_str, allow, viewer_url


def visit_wokwi_html(self, node: WokwiNode):
    """Visit WokwiNode and render as HTML iframe with Wokwi UI frame.

    Generates HTML for a single diagram viewer embedded in a styled frame
    with header showing Wokwi branding and action buttons (info, fullscreen).
    """
    attr_str, allow, _ = _render_iframe_attrs(node)
    iframe = f"<iframe {attr_str}{allow}></iframe>"

    if node.get("suppress_header"):
        self.body.append(iframe)
        raise _n.SkipNode

    about_wokwi_url = getattr(self.builder.app.config, "docs_embed_about_wokwi_url")
    static_path = node.get("static_path", "")

    self.body.append('<div class="wokwi-frame">')
    self.body.append('<div class="wokwi-tabsbar">')
    self.body.append('<div class="wokwi-groups-container">')

    # Single WOKWI SIMULATOR GROUP
    self.body.append('<div class="wokwi-group wokwi-group-simulator">')
    # Header with icon, label, and buttons
    self.body.append('<div class="wokwi-group-header">')
    self.body.append(f'<img src="{static_path}wokwi.svg" alt="Wokwi" class="wokwi-icon"/>')
    self.body.append('<div class="wokwi-group-label">WOKWI SIMULATOR</div>')
    # Add info and fullscreen buttons
    self.body.append('<div class="wokwi-header-actions">')
    if about_wokwi_url:
        self.body.append(
            f'<a class="wokwi-info-btn" href="{_escape(about_wokwi_url, True)}" target="_blank" rel="noopener" title="About Wokwi">ⓘ</a>'
        )
    self.body.append('<a class="wokwi-fullscreen-btn" href="#" title="Fullscreen simulation">⛶</a>')
    self.body.append("</div>")  # header-actions
    self.body.append("</div>")  # group header
    self.body.append("</div>")  # simulator group

    self.body.append("</div>")  # wokwi-groups-container
    self.body.append("</div>")  # tabsbar
    self.body.append(iframe)
    self.body.append("</div>")  # wokwi-frame
    raise _n.SkipNode


def depart_wokwi_html(self, node: WokwiNode):
    """Departure function for WokwiNode HTML rendering (no-op)."""
    pass


def visit_wokwi_tabs_html(self, node: WokwiTabsNode):
    """Visit WokwiTabsNode and render as HTML tabbed container.

    Creates the root div wrapper for a tabbed interface with appropriate
    CSS classes and data attributes for styling and JavaScript interaction.
    """
    classes = "wokwi-tabs" + (" " + " ".join(node.get("classes", [])) if node.get("classes") else "")
    data_variant = f' data-variant="{_escape(node.get("variant"), True)}"' if node.get("variant") else ""
    self.body.append(f'<div class="{classes}"{data_variant}>')


def depart_wokwi_tabs_html(self, node: WokwiTabsNode):
    """Departure function for WokwiTabsNode HTML rendering."""
    self.body.append("</div>")


def visit_tablist_html(self, node: TabListNode):
    """Visit TabListNode and render as HTML tab header bar.

    Generates the interactive tab buttons and header sections organized into groups:
    - CODE group: Source code file tab(s) with GitHub link
    - WOKWI SIMULATOR group: Diagram tab(s) with Wokwi branding
    - LAUNCHPAD group: Flash button with LaunchPad config link (optional)
    """
    labels = node.get("labels", [])
    panel_ids = node.get("panel_ids", [])
    tabs_code = node.get("tabs_code", [])
    tabs_wokwi = node.get("tabs_wokwi", [])
    github_href = node.get("github_href")
    about_wokwi_url = getattr(self.builder.app.config, "docs_embed_about_wokwi_url", None)
    launchpad_href = node.get("launchpad_href")
    static_path = node.get("static_path")

    self.body.append('<div class="wokwi-tabsbar">')
    self.body.append('<div class="wokwi-groups-container">')

    # CODE GROUP - First bordered section
    if tabs_code:
        self.body.append('<div class="wokwi-group wokwi-group-code">')
        # Header with GitHub icon and CODE label
        self.body.append('<div class="wokwi-group-header">')
        if github_href:
            self.body.append(f'<a href="{_escape(github_href, True)}" target="_blank" rel="noopener" title="View on GitHub">')
            self.body.append(f'<img src="{static_path}github.svg" alt="GitHub" class="wokwi-icon"/>')
            self.body.append('</a>')
        self.body.append('<div class="wokwi-group-label">CODE</div>')
        self.body.append("</div>")  # group header

        self.body.append('<div class="wokwi-tablist wokwi-code-tablist" data-wokwi="tablist">')
        for i, label in enumerate(tabs_code):
            panel_index = labels.index(label)
            pid = panel_ids[panel_index]
            selected = "true" if i == 0 else "false"
            self.body.append(
                f'<button class="wokwi-tab wokwi-code-tab" type="button" role="tab" '
                f'aria-selected="{selected}" data-target="{pid}">{_escape(label, True)}</button>'
            )
        self.body.append("</div>")  # code tablist
        self.body.append("</div>")  # code group

    # WOKWI SIMULATOR GROUP - Second bordered section
    if tabs_wokwi:
        self.body.append('<div class="wokwi-group wokwi-group-simulator">')
        # Header with icon, label, and buttons
        self.body.append('<div class="wokwi-group-header">')
        self.body.append(f'<img src="{static_path}wokwi.svg" alt="Wokwi" class="wokwi-icon"/>')
        self.body.append('<div class="wokwi-group-label">WOKWI SIMULATOR</div>')
        # Add info and fullscreen buttons
        self.body.append('<div class="wokwi-header-actions">')
        if about_wokwi_url:
            self.body.append(
                f'<a class="wokwi-info-btn" href="{_escape(about_wokwi_url, True)}" target="_blank" rel="noopener" title="About Wokwi">ⓘ</a>'
            )
        self.body.append('<a class="wokwi-fullscreen-btn" href="#" title="Fullscreen simulation" data-wokwi-only="true">⛶</a>')
        self.body.append("</div>")  # header-actions
        self.body.append("</div>")  # group header
        # Simulator tabs
        self.body.append('<div class="wokwi-tablist wokwi-wokwi-tablist" data-wokwi="tablist">')
        for i, label in enumerate(tabs_wokwi):
            panel_index = labels.index(label)
            pid = panel_ids[panel_index]
            selected = "true" if i == 0 and not tabs_code else "false"
            self.body.append(
                f'<button class="wokwi-tab wokwi-wokwi-tab" type="button" role="tab" '
                f'aria-selected="{selected}" data-target="{pid}">{_escape(label, True)}</button>'
            )
        self.body.append("</div>")  # wokwi tablist
        self.body.append("</div>")  # simulator group

    # LAUNCHPAD GROUP - Third bordered section
    if launchpad_href:
        self.body.append('<div class="wokwi-group wokwi-group-launchpad">')
        self.body.append('<div class="wokwi-group-label">launchpad</div>')
        self.body.append(
            f'<a class="wokwi-launchpad-btn" href="{_escape(launchpad_href, True)}" '
            f'data-base-href="{_escape(launchpad_href, True)}" '
            f'target="_blank" rel="noopener" title="Flash your chip">'
            f'<img src="{static_path}esp_launchpad.svg" alt="ESP Launchpad" class="launchpad-icon"/>'
            f'<span class="launchpad-text">Flash</span>'
            f'</a>'
        )
        self.body.append("</div>")  # launchpad group

    self.body.append("</div>")  # wokwi-groups-container
    self.body.append("</div>")  # tabsbar
    raise _n.SkipNode


def depart_tablist_html(self, node: TabListNode):
    """Departure function for TabListNode HTML rendering (no-op)."""
    pass


def visit_tabpanel_html(self, node: TabPanelNode):
    """Visit TabPanelNode and render as HTML tab content panel.

    Creates a tab panel div that can be shown/hidden via JavaScript based on
    tab selection. Stores viewer URL for use by interactive scripts.
    """
    pid = node.get("panel_id")
    active = "true" if node.get("active") else "false"

    viewer_url: Optional[str] = None
    for ch in node.children:
        if isinstance(ch, WokwiNode):
            _attr, _allow, url = _render_iframe_attrs(ch)
            viewer_url = url
            break

    data_attr = f' data-viewer-url="{_escape(viewer_url, True)}"' if viewer_url else ""
    self.body.append(f'<div class="wokwi-panel" id="{pid}" role="tabpanel" data-active="{active}"{data_attr}>')


def depart_tabpanel_html(self, node: TabPanelNode):
    """Departure function for TabPanelNode HTML rendering."""
    self.body.append("</div>")


def _fallback_text(viewer_url: str) -> str:
    """Generate fallback text representation of a Wokwi diagram.

    Args:
        viewer_url: Complete iframe URL

    Returns:
        Human-readable text representation
    """
    return f"Wokwi simulation: {viewer_url}"


def visit_wokwi_text(self, node: WokwiNode):
    """Visit WokwiNode and render as plain text (fallback format).

    Used for text-based output formats where HTML/interactive content isn't supported.
    Outputs viewer URL so users can access the diagram if needed.
    """
    viewer_url = iframe_url(node.get("iframe_page"), node.get("diagram_url"), node.get("firmware_url"))
    self.add_text(_fallback_text(viewer_url))
    raise _n.SkipNode


def depart_wokwi_text(self, node: WokwiNode):
    """Departure function for WokwiNode text rendering (no-op)."""
    pass


def visit_wokwi_tabs_text(self, node: WokwiTabsNode):
    """Visit WokwiTabsNode and render as plain text tabs header."""
    self.add_text("Tabs:\n")


def depart_wokwi_tabs_text(self, node: WokwiTabsNode):
    """Departure function for WokwiTabsNode text rendering (no-op)."""
    pass


def visit_tablist_text(self, node: TabListNode):
    """Visit TabListNode and render as plain text tab list."""
    labels = node.get("labels", [])
    for i, lbl in enumerate(labels, 1):
        self.add_text(f"  {i}. {lbl}\n")
    raise _n.SkipNode


def depart_tablist_text(self, node: TabListNode):
    """Departure function for TabListNode text rendering (no-op)."""
    pass


def visit_tabpanel_text(self, node: TabPanelNode):
    """Visit TabPanelNode and render as plain text section."""
    label = node.get("label") or "Tab"
    self.add_text(f"\n[{label}]\n")


def depart_tabpanel_text(self, node: TabPanelNode):
    """Departure function for TabPanelNode text rendering."""
    self.add_text("\n")


def visit_wokwi_latex(self, node: WokwiNode):
    """Visit WokwiNode and render as LaTeX URL reference.

    Generates a clickable URL for PDF output, since interactive iframes
    are not supported in LaTeX/PDF format.
    """
    viewer_url = iframe_url(node.get("iframe_page"), node.get("diagram_url"), node.get("firmware_url"))
    self.body.append(r"\url{" + viewer_url + "}")
    raise _n.SkipNode


def depart_wokwi_latex(self, node: WokwiNode):
    """Departure function for WokwiNode LaTeX rendering (no-op)."""
    pass


def visit_wokwi_tabs_latex(self, node: WokwiTabsNode):
    """Visit WokwiTabsNode and render as LaTeX spacing."""
    self.body.append("\\par\\medskip{}\n")


def depart_wokwi_tabs_latex(self, node: WokwiTabsNode):
    """Departure function for WokwiTabsNode LaTeX rendering."""
    self.body.append("\\par\\medskip{}\n")


def visit_tablist_latex(self, node: TabListNode):
    """Visit TabListNode and render as LaTeX tab list."""
    labels = node.get("labels", [])
    if labels:
        self.body.append("\\textbf{Tabs:} " + ", ".join(labels) + "\\\\\n")
    raise _n.SkipNode


def depart_tablist_latex(self, node: TabListNode):
    """Departure function for TabListNode LaTeX rendering (no-op)."""
    pass


def visit_tabpanel_latex(self, node: TabPanelNode):
    """Visit TabPanelNode and render as LaTeX panel header."""
    label = node.get("label") or "Tab"
    self.body.append("\\textbf{" + label + "}: ")


def depart_tabpanel_latex(self, node: TabPanelNode):
    """Departure function for TabPanelNode LaTeX rendering."""
    self.body.append("\\par\n")

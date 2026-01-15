"""Docutils AST nodes for Wokwi diagram rendering in Sphinx.

This module defines custom AST nodes used to represent Wokwi diagram elements
in the Sphinx documentation abstract syntax tree. These nodes are used by
directives to structure diagram content and by visitors to render them in
various output formats (HTML, LaTeX, etc.).

Node Hierarchy:
    - WokwiNode: Single embedded diagram
    - WokwiTabsNode: Tabbed diagram view (contains TabList + TabPanels)
        - TabListNode: Tab header buttons
        - TabPanelNode: Tab content area
"""

from __future__ import annotations

from docutils import nodes


class WokwiNode(nodes.General, nodes.Element):
    """Represents a single embedded Wokwi diagram with viewer frame UI.
    
    This node wraps all content related to a single diagram iframe including
    the diagram viewer, any interactive controls, and metadata.
    """

    pass


class WokwiTabsNode(nodes.General, nodes.Element):
    """Root container for tabbed diagram view.
    
    This node represents a tabbed interface that can display multiple diagrams.
    It contains a TabListNode with tab headers and one or more TabPanelNode
    elements, each containing diagram content.
    
    Structure:
        WokwiTabsNode
        ├── TabListNode (tab headers)
        │   └── tab button elements
        └── TabPanelNode* (tab panels, repeating)
            └── WokwiNode (diagram content)
    """

    pass


class TabListNode(nodes.General, nodes.Element):
    """Clickable tab headers area.
    
    This node represents the clickable buttons that switch between tab panels.
    Each tab corresponds to a TabPanelNode in the parent WokwiTabsNode.
    """

    pass


class TabPanelNode(nodes.General, nodes.Element):
    """Single tab panel wrapping arbitrary children.
    
    This node represents one panel (pane) in a tabbed interface. It contains
    the content that should be displayed when its corresponding tab is active.
    Typically contains a WokwiNode for diagram display, but can hold other
    elements as needed.
    """

    pass

"""
:menuitem: role – render a Kconfig option as a linked chip.

Usage::

    :menuitem:`CONFIG_ESP_WIFI_STATIC_RX_BUFFER_NUM`

The role resolves the explicit ``CONFIG_*`` labels emitted by the generated
Kconfig reference. Unknown names use Sphinx's standard missing-reference
warning and degrade to plain text.
"""
from docutils import nodes
from sphinx.roles import XRefRole


class MenuitemRole(XRefRole):
    """Resolve a Kconfig label through Sphinx's standard ``:ref:`` domain."""

    def __init__(self):
        super().__init__(innernodeclass=nodes.inline, warn_dangling=True)

    def process_link(self, env, refnode, has_explicit_title, title, target):
        target = target.strip().upper()
        if not target.startswith('CONFIG_'):
            target = 'CONFIG_' + target

        refnode['refdomain'] = 'std'
        refnode['reftype'] = 'ref'
        # Kconfig choice values are explicit targets inside lists rather than
        # titled sections. Resolve every menu item through ``anonlabels`` so
        # both section labels and these captionless targets are supported.
        refnode['refexplicit'] = True
        if not has_explicit_title:
            title = target
        return title, target.lower()

    def result_nodes(self, document, env, node, is_ref):
        chip = nodes.inline(classes=['kconfig-menupath-chip', 'kconfig-menuitem-chip'])
        chip += node
        return [chip], []


def setup(app):
    app.add_role('menuitem', MenuitemRole())

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.2'}

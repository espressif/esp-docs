#!/usr/bin/env python3
"""Unit and integration tests for the :menuitem: role."""

import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx

from esp_docs.idf_extensions import menupath_role


class TestMenuitemRole(unittest.TestCase):

    def test_normalizes_config_target(self):
        role = menupath_role.MenuitemRole()
        refnode = addnodes.pending_xref()

        title, target = role.process_link(None, refnode, False, 'foo', 'foo')

        self.assertEqual(title, 'CONFIG_FOO')
        self.assertEqual(target, 'config_foo')
        self.assertEqual(refnode['refdomain'], 'std')
        self.assertEqual(refnode['reftype'], 'ref')
        self.assertTrue(refnode['refexplicit'])

    def test_preserves_explicit_title(self):
        role = menupath_role.MenuitemRole()
        refnode = addnodes.pending_xref()

        title, target = role.process_link(
            None, refnode, True, 'Wi-Fi buffers', 'CONFIG_ESP_WIFI_STATIC_RX_BUFFER_NUM'
        )

        self.assertEqual(title, 'Wi-Fi buffers')
        self.assertEqual(target, 'config_esp_wifi_static_rx_buffer_num')

    def test_wraps_reference_in_chip(self):
        role = menupath_role.MenuitemRole()
        refnode = addnodes.pending_xref()

        result, messages = role.result_nodes(None, None, refnode, True)

        self.assertEqual(messages, [])
        self.assertIsInstance(result[0], nodes.inline)
        self.assertIn('kconfig-menuitem-chip', result[0]['classes'])
        self.assertIs(result[0][0], refnode)

    def test_setup_registers_only_menuitem_role(self):
        app = MagicMock()

        menupath_role.setup(app)

        app.add_role.assert_called_once()
        name, role = app.add_role.call_args.args
        self.assertEqual(name, 'menuitem')
        self.assertIsInstance(role, menupath_role.MenuitemRole)


class TestMenuitemSphinxIntegration(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.srcdir = self.root / 'src'
        self.outdir = self.root / 'html'
        self.doctreedir = self.root / 'doctrees'
        self.srcdir.mkdir()
        (self.srcdir / 'conf.py').write_text(
            "extensions = ['esp_docs.idf_extensions.menupath_role']\n",
            encoding='utf-8',
        )

    def tearDown(self):
        self.tempdir.cleanup()

    def build(self, source):
        (self.srcdir / 'index.rst').write_text(source, encoding='utf-8')
        warnings = io.StringIO()
        app = Sphinx(
            str(self.srcdir),
            str(self.srcdir),
            str(self.outdir),
            str(self.doctreedir),
            'html',
            status=io.StringIO(),
            warning=warnings,
            freshenv=True,
        )
        app.build()
        html = (self.outdir / 'index.html').read_text(encoding='utf-8')
        return html, warnings.getvalue()

    def test_resolves_generated_kconfig_label(self):
        html, warnings = self.build(
            "Kconfig\n"
            "=======\n\n"
            "CONFIG_CHOICE\n"
            "----------\n\n"
            "Available options:\n\n"
            "  .. _CONFIG_FOO:\n\n"
            "- FOO\n\n"
            "Use :menuitem:`FOO`.\n"
        )

        self.assertNotIn('undefined label', warnings)
        self.assertIn('kconfig-menuitem-chip', html)
        self.assertIn('href="#config-foo"', html)
        self.assertIn('CONFIG_FOO', html)

    def test_unknown_option_warns_and_degrades_to_text(self):
        html, warnings = self.build(
            "Kconfig\n"
            "=======\n\n"
            "Use :menuitem:`MISSING`.\n"
        )

        self.assertIn("undefined label: 'config_missing'", warnings.lower())
        self.assertIn('CONFIG_MISSING', html)


if __name__ == '__main__':
    unittest.main()

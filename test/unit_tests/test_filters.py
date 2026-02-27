import re
import unittest


class TestTocTreeFilterRegex(unittest.TestCase):
    """Test the regex pattern used by TocTreeFilt and ListFilter."""

    RE_PATTERN = re.compile(r'^\s*:(.+?):\s*(.+)$')

    def test_simple_filter_tag(self):
        m = self.RE_PATTERN.match(':esp32: Some Page <page>')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), 'esp32')
        self.assertEqual(m.group(2), 'Some Page <page>')

    def test_compound_filter_expression(self):
        m = self.RE_PATTERN.match(':esp32 or esp32s2: Shared Page <shared>')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), 'esp32 or esp32s2')
        self.assertEqual(m.group(2), 'Shared Page <shared>')

    def test_no_filter_plain_entry(self):
        m = self.RE_PATTERN.match('plain_page')
        self.assertIsNone(m)

    def test_indented_filter(self):
        m = self.RE_PATTERN.match('   :esp32: indented <page>')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), 'esp32')

    def test_not_filter_expression(self):
        m = self.RE_PATTERN.match(':not esp32: Other Target Page <other>')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), 'not esp32')


class TestTocTreeFilterEntry(unittest.TestCase):
    """Test the filter_entry logic without full Sphinx setup."""

    RE_PATTERN = re.compile(r'^\s*:(.+?):\s*(.+)$')

    def _filter_entry(self, entry, active_tags):
        """Simulate TocTreeFilt.filter_entry / ListFilter.filter_entry."""
        m = self.RE_PATTERN.match(entry)
        if m is not None:
            tag_filter, entry = m.groups()
            # Simplified tag evaluation: check if any active tag appears in the filter
            if not any(tag in tag_filter for tag in active_tags):
                return None
        return entry

    def test_matching_tag_includes_entry(self):
        result = self._filter_entry(':esp32: BT Page <bt>', ['esp32'])
        self.assertEqual(result, 'BT Page <bt>')

    def test_non_matching_tag_excludes_entry(self):
        result = self._filter_entry(':esp32: BT Page <bt>', ['esp32s2'])
        self.assertIsNone(result)

    def test_unfiltered_entry_always_included(self):
        result = self._filter_entry('general_page', [])
        self.assertEqual(result, 'general_page')

    def test_empty_active_tags_excludes_filtered(self):
        result = self._filter_entry(':esp32: Some Page <page>', [])
        self.assertIsNone(result)


class TestListFilterEntry(unittest.TestCase):
    """Test list filter with numbered list items."""

    RE_PATTERN = re.compile(r'^\s*:(.+?):\s*(.+)$')

    def test_numbered_list_item_with_filter(self):
        m = self.RE_PATTERN.match(':esp32: #. Step for ESP32 only')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(2), '#. Step for ESP32 only')

    def test_bullet_list_item_with_filter(self):
        m = self.RE_PATTERN.match(':esp32s2: - Item for S2')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(2), '- Item for S2')


if __name__ == '__main__':
    unittest.main()

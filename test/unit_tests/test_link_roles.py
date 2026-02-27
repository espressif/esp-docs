import unittest

from esp_docs.esp_extensions.link_roles import url_join


class TestUrlJoin(unittest.TestCase):

    def test_basic_join(self):
        result = url_join('https://github.com', 'espressif', 'esp-idf')
        self.assertEqual(result, 'https://github.com/espressif/esp-idf')

    def test_collapses_double_slashes(self):
        result = url_join('https://github.com/', '/espressif/', '/esp-idf')
        self.assertEqual(result, 'https://github.com/espressif/esp-idf')

    def test_preserves_https_double_slash(self):
        result = url_join('https://github.com', 'repo')
        self.assertTrue(result.startswith('https://'))

    def test_single_component(self):
        result = url_join('https://example.com')
        self.assertEqual(result, 'https://example.com')

    def test_many_components(self):
        result = url_join('https://github.com', 'org', 'repo', 'tree', 'main', 'path/to/file')
        self.assertEqual(result, 'https://github.com/org/repo/tree/main/path/to/file')

    def test_trailing_slashes_collapsed(self):
        result = url_join('https://github.com/', 'repo/')
        self.assertNotIn('//', result.replace('https://', ''))


if __name__ == '__main__':
    unittest.main()

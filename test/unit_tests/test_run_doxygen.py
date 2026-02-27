import os
import tempfile
import unittest

from esp_docs.esp_extensions.run_doxygen import (
    get_api_name,
    header_to_xml_path,
    find_doxygen_dir,
    get_rst_header,
)


class TestGetApiName(unittest.TestCase):

    def test_simple_header(self):
        self.assertEqual(get_api_name('components/driver/include/driver/uart.h'), 'uart.h')

    def test_hpp_header(self):
        self.assertEqual(get_api_name('components/cxx/include/esp_event.hpp'), 'esp_event.hpp')

    def test_nested_path(self):
        self.assertEqual(get_api_name('a/b/c/d/spi_master.h'), 'spi_master.h')

    def test_no_match(self):
        self.assertEqual(get_api_name('no_slash_file.txt'), '')


class TestHeaderToXmlPath(unittest.TestCase):

    def test_underscores_doubled(self):
        result = header_to_xml_path('spi_master.h', '/xml')
        self.assertIn('spi__master', result)

    def test_slashes_replaced(self):
        result = header_to_xml_path('driver/uart.h', '/xml')
        self.assertIn('driver_2uart', result)

    def test_extension_format(self):
        result = header_to_xml_path('file.h', '/xml')
        self.assertTrue(result.endswith('_8h.xml'))

    def test_hpp_extension(self):
        result = header_to_xml_path('file.hpp', '/xml')
        self.assertTrue(result.endswith('_8hpp.xml'))


class TestFindDoxygenDir(unittest.TestCase):

    def test_doxyfile_in_dir(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, 'Doxyfile'), 'w').close()
            self.assertEqual(find_doxygen_dir(d), d)

    def test_doxyfile_in_subdir(self):
        with tempfile.TemporaryDirectory() as d:
            sub = os.path.join(d, 'doxygen')
            os.makedirs(sub)
            open(os.path.join(sub, 'Doxyfile'), 'w').close()
            self.assertEqual(find_doxygen_dir(d), sub)

    def test_no_doxyfile_returns_original(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(find_doxygen_dir(d), d)


class TestGetRstHeader(unittest.TestCase):

    def test_header_format(self):
        result = get_rst_header('Functions')
        self.assertIn('Functions', result)
        self.assertIn('^' * len('Functions'), result)

    def test_underline_matches_length(self):
        name = 'Type Definitions'
        result = get_rst_header(name)
        lines = result.strip().split('\n')
        self.assertEqual(len(lines[0]), len(lines[1]))


if __name__ == '__main__':
    unittest.main()

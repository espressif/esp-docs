import json
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from esp_docs.modified_files import normalize_modified_file_path, parse_modified_files_arg
from esp_docs.esp_extensions.run_doxygen import (
    ApiPath,
    convert_api_xml_to_inc,
    find_doxygen_dir,
    get_api_name,
    get_rst_header,
    header_to_xml_path,
    should_keep_api_reference,
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


class TestModifiedFilesHelpers(unittest.TestCase):

    def test_parse_modified_files_arg_supports_multiple_cli_args(self):
        self.assertEqual(
            parse_modified_files_arg([
                'components/driver/include/driver/uart.h',
                'docs/en/api-reference/system/ota.rst',
            ]),
            [
                'components/driver/include/driver/uart.h',
                'docs/en/api-reference/system/ota.rst',
            ],
        )

    def test_parse_modified_files_arg_supports_semicolon_delimited_arg(self):
        self.assertEqual(
            parse_modified_files_arg([
                '.gitlab-ci.yml;.gitlab/ci/common.yml;components/driver/include/driver/uart.h;'
            ]),
            [
                '.gitlab-ci.yml',
                '.gitlab/ci/common.yml',
                'components/driver/include/driver/uart.h',
            ],
        )

    def test_normalize_modified_file_path_keeps_project_relative_path(self):
        self.assertEqual(
            normalize_modified_file_path('./components/driver/include/driver/uart.h'),
            'components/driver/include/driver/uart.h',
        )

    def test_should_keep_api_reference_for_matching_modified_header(self):
        modified_files = {'components/driver/include/driver/uart.h'}
        self.assertTrue(
            should_keep_api_reference('components/driver/include/driver/uart.h', modified_files, fast_build=True)
        )

    def test_should_drop_api_reference_for_non_matching_header(self):
        modified_files = {'components/driver/include/driver/spi_master.h'}
        self.assertFalse(
            should_keep_api_reference('components/driver/include/driver/uart.h', modified_files, fast_build=True)
        )

    def test_should_keep_api_reference_for_normal_build(self):
        self.assertTrue(
            should_keep_api_reference('components/driver/include/driver/uart.h', set(), fast_build=False)
        )


class TestConvertApiXmlToInc(unittest.TestCase):

    def make_app(self, build_dir, modified_files='[]'):
        return SimpleNamespace(
            config=SimpleNamespace(
                build_dir=build_dir,
                modified_files=modified_files,
                project_path='/tmp/project',
            )
        )

    def make_api_path(self, build_dir, header_path='components/driver/include/driver/uart.h'):
        return ApiPath(
            header_path=header_path,
            api_name='uart.h',
            xml_file_path=os.path.join(build_dir, 'xml', 'uart_8h.xml'),
            inc_file_path=os.path.join(build_dir, 'inc', 'uart.inc'),
        )

    @patch('esp_docs.esp_extensions.run_doxygen.generate_directives', return_value='generated rst')
    @patch('esp_docs.esp_extensions.run_doxygen.get_header_paths')
    def test_fast_build_without_modified_files_blanks_output(self, mock_get_header_paths, mock_generate_directives):
        with tempfile.TemporaryDirectory() as build_dir:
            os.makedirs(os.path.join(build_dir, 'xml'))
            mock_get_header_paths.return_value = [self.make_api_path(build_dir)]

            with patch.dict(os.environ, {'DOCS_FAST_BUILD': 'y'}, clear=False):
                convert_api_xml_to_inc(self.make_app(build_dir), [])

            with open(os.path.join(build_dir, 'inc', 'uart.inc'), 'r', encoding='utf-8') as inc_file:
                self.assertEqual(inc_file.read(), '')
            mock_generate_directives.assert_called_once()

    @patch('esp_docs.esp_extensions.run_doxygen.generate_directives', return_value='generated rst')
    @patch('esp_docs.esp_extensions.run_doxygen.get_header_paths')
    def test_fast_build_keeps_matching_modified_header(self, mock_get_header_paths, mock_generate_directives):
        with tempfile.TemporaryDirectory() as build_dir:
            os.makedirs(os.path.join(build_dir, 'xml'))
            mock_get_header_paths.return_value = [self.make_api_path(build_dir)]
            modified_files = json.dumps(['components/driver/include/driver/uart.h'])

            with patch.dict(os.environ, {'DOCS_FAST_BUILD': 'y'}, clear=False):
                convert_api_xml_to_inc(self.make_app(build_dir, modified_files=modified_files), [])

            with open(os.path.join(build_dir, 'inc', 'uart.inc'), 'r', encoding='utf-8') as inc_file:
                self.assertEqual(inc_file.read(), 'generated rst')
            mock_generate_directives.assert_called_once()

    @patch('esp_docs.esp_extensions.run_doxygen.generate_directives', return_value='generated rst')
    @patch('esp_docs.esp_extensions.run_doxygen.get_header_paths')
    def test_fast_build_blanks_non_matching_header(self, mock_get_header_paths, mock_generate_directives):
        with tempfile.TemporaryDirectory() as build_dir:
            os.makedirs(os.path.join(build_dir, 'xml'))
            mock_get_header_paths.return_value = [self.make_api_path(build_dir)]
            modified_files = json.dumps(['components/driver/include/driver/spi_master.h'])

            with patch.dict(os.environ, {'DOCS_FAST_BUILD': 'y'}, clear=False):
                convert_api_xml_to_inc(self.make_app(build_dir, modified_files=modified_files), [])

            with open(os.path.join(build_dir, 'inc', 'uart.inc'), 'r', encoding='utf-8') as inc_file:
                self.assertEqual(inc_file.read(), '')
            mock_generate_directives.assert_called_once()

    @patch('esp_docs.esp_extensions.run_doxygen.generate_directives', return_value='generated rst')
    @patch('esp_docs.esp_extensions.run_doxygen.get_header_paths')
    def test_normal_build_keeps_output(self, mock_get_header_paths, mock_generate_directives):
        with tempfile.TemporaryDirectory() as build_dir:
            os.makedirs(os.path.join(build_dir, 'xml'))
            mock_get_header_paths.return_value = [self.make_api_path(build_dir)]

            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop('DOCS_FAST_BUILD', None)
                convert_api_xml_to_inc(self.make_app(build_dir), [])

            with open(os.path.join(build_dir, 'inc', 'uart.inc'), 'r', encoding='utf-8') as inc_file:
                self.assertEqual(inc_file.read(), 'generated rst')
            mock_generate_directives.assert_called_once()


if __name__ == '__main__':
    unittest.main()

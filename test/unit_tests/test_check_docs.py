import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from esp_docs.build_docs import print_sphinx_failure_summary
from esp_docs.check_docs import sanitize_line, check_docs, group_log_messages


class TestSanitizeLine(unittest.TestCase):

    def test_strip_path_keeps_filename(self):
        line = '/home/user/project/docs/api/uart.rst:42: WARNING: duplicate'
        result = sanitize_line(line)
        self.assertIn('uart.rst', result)
        self.assertNotIn('/home/user/project/docs/api/', result)

    def test_strip_line_number(self):
        line = 'uart.rst:42: WARNING: something'
        result = sanitize_line(line)
        self.assertIn(':line:', result)
        self.assertNotIn(':42:', result)

    def test_strip_duplicate_line_number(self):
        line = 'uart.rst:42. duplicate definition'
        result = sanitize_line(line)
        self.assertIn(':line.', result)
        self.assertNotIn(':42.', result)

    def test_strip_terminal_control_chars(self):
        line = '\x1B[39;49;00muart.rst: WARNING: something\x1B[0m'
        result = sanitize_line(line)
        self.assertNotIn('\x1B', result)
        self.assertIn('uart.rst', result)

    def test_combined_sanitization(self):
        line = '\x1B[31m/long/path/to/file.rst:123: WARNING: bad ref\x1B[0m'
        result = sanitize_line(line)
        self.assertNotIn('\x1B', result)
        self.assertNotIn('/long/path/to/', result)
        self.assertIn('file.rst', result)
        self.assertIn(':line:', result)

    def test_plain_line_unchanged(self):
        line = 'simple warning text without path or line number'
        result = sanitize_line(line)
        self.assertEqual(line, result)


class TestCheckDocs(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def _write_file(self, name, lines):
        path = os.path.join(self.temp_dir, name)
        with open(path, 'w') as f:
            f.write('\n'.join(lines) + '\n' if lines else '')
        return path

    def test_no_warnings_passes(self):
        log = self._write_file('log.txt', ['some normal line'])
        known = self._write_file('known.txt', ['some normal line\n'])
        out = os.path.join(self.temp_dir, 'sanitized.txt')
        result = check_docs('en', 'esp32', log, known, out)
        self.assertEqual(result, 0)

    def test_new_warning_fails(self):
        log = self._write_file('log.txt', ['a new unknown warning'])
        known = self._write_file('known.txt', [])
        out = os.path.join(self.temp_dir, 'sanitized.txt')
        result = check_docs('en', 'esp32', log, known, out)
        self.assertEqual(result, 1)

    def test_new_warning_summary_mentions_fatal_warnings(self):
        log = self._write_file('sphinx-warning-log.txt', ['index.rst:10: WARNING: unknown target'])
        known = self._write_file('known.txt', [])
        out = os.path.join(self.temp_dir, 'sanitized.txt')

        stdout = io.StringIO()
        with redirect_stdout(stdout):
            result = check_docs('en', 'esp32', log, known, out)

        output = stdout.getvalue()
        self.assertEqual(result, 1)
        self.assertIn('=== BUILD FAILED ===', output)
        self.assertIn('Sphinx warnings are treated as errors (fatal)', output)
        self.assertIn('This job fails on new warnings.', output)
        self.assertIn('New sphinx warning entries: 1', output)

    def test_multiline_warning_is_grouped_for_display(self):
        grouped = group_log_messages([
            type('Message', (), {'sanitized_text': 'file.h:line: warning: bad docs\n'}),
            type('Message', (), {'sanitized_text': "  parameter 'max'\n"}),
        ], 'sanitized_text')

        self.assertEqual(grouped, ["file.h:line: warning: bad docs\n  parameter 'max'"])

    def test_missing_log_file_fails(self):
        known = self._write_file('known.txt', [])
        out = os.path.join(self.temp_dir, 'sanitized.txt')
        result = check_docs('en', 'esp32', '/nonexistent/log.txt', known, out)
        self.assertEqual(result, 1)

    def test_missing_known_warnings_file_ok(self):
        log = self._write_file('log.txt', [])
        out = os.path.join(self.temp_dir, 'sanitized.txt')
        result = check_docs('en', 'esp32', log, '/nonexistent/known.txt', out)
        self.assertEqual(result, 0)

    def test_doxygen_anonymous_struct_filtered(self):
        warning = 'file.h:line: warning: parameters of member SomeStruct::@1 are not (all) documented'
        log = self._write_file('log.txt', [warning])
        # Use 'doxygen' in the known warnings filename to activate the filter
        known = self._write_file('doxygen-known.txt', [])
        out = os.path.join(self.temp_dir, 'sanitized.txt')
        result = check_docs('en', 'esp32', log, known, out)
        self.assertEqual(result, 0)

    def test_known_warning_matches(self):
        warning_line = 'file.rst:10: WARNING: known issue'
        sanitized = sanitize_line(warning_line) + '\n'
        log = self._write_file('log.txt', [warning_line])
        known = self._write_file('known.txt', [sanitized])
        out = os.path.join(self.temp_dir, 'sanitized.txt')
        result = check_docs('en', 'esp32', log, known, out)
        self.assertEqual(result, 0)


class TestBuildFailureSummary(unittest.TestCase):
    def test_sphinx_failure_summary_mentions_fatal_error(self):
        temp_dir = tempfile.mkdtemp()
        output_log = os.path.join(temp_dir, 'sphinx-build-output-html.txt')
        with open(output_log, 'w') as f:
            f.write('Configuration error:\n')
            f.write('broken conf.py\n')

        build_info = {
            'language': 'en',
            'target': 'generic',
        }

        stdout = io.StringIO()
        with redirect_stdout(stdout):
            print_sphinx_failure_summary(build_info, 'html', 4, output_log)

        output = stdout.getvalue()
        self.assertIn('=== BUILD FAILED ===', output)
        self.assertIn('en/generic: Sphinx build error (fatal)', output)
        self.assertIn('en/generic: Exit code: 4', output)
        self.assertIn('en/generic: Full output:', output)
        self.assertIn('broken conf.py', output)


if __name__ == '__main__':
    unittest.main()

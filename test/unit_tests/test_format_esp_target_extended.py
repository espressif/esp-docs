import os.path
import unittest
from unittest.mock import MagicMock, patch

from esp_docs.esp_extensions.format_esp_target import StringSubstituter, check_content


class TestStringSubstituterMultiTarget(unittest.TestCase):
    """Test StringSubstituter.init_sub_strings for multiple targets."""

    def _make_sub(self, target):
        sub = StringSubstituter()
        config = MagicMock()
        config.idf_target = target
        config.build_dir = os.path.dirname(os.path.realpath(__file__))
        sub.init_sub_strings(config)
        return sub

    def test_esp32s2_name(self):
        sub = self._make_sub('esp32s2')
        self.assertEqual(sub.substitute_strings['{IDF_TARGET_NAME}'], 'ESP32-S2')

    def test_esp32s2_toolchain(self):
        sub = self._make_sub('esp32s2')
        self.assertEqual(sub.substitute_strings['{IDF_TARGET_TOOLCHAIN_PREFIX}'], 'xtensa-esp32s2-elf')

    def test_esp32c3_toolchain_riscv(self):
        sub = self._make_sub('esp32c3')
        self.assertEqual(sub.substitute_strings['{IDF_TARGET_TOOLCHAIN_PREFIX}'], 'riscv32-esp-elf')

    def test_cfg_prefix_strips_hyphen(self):
        sub = self._make_sub('esp32s2')
        self.assertEqual(sub.substitute_strings['{IDF_TARGET_CFG_PREFIX}'], 'ESP32S2')

    def test_no_target_skips_init(self):
        sub = StringSubstituter()
        config = MagicMock()
        config.idf_target = None
        sub.init_sub_strings(config)
        self.assertEqual(sub.substitute_strings, {})

    def test_datasheet_urls_populated(self):
        sub = self._make_sub('esp32')
        self.assertIn('datasheet', sub.substitute_strings['{IDF_TARGET_DATASHEET_EN_URL}'])
        self.assertIn('datasheet', sub.substitute_strings['{IDF_TARGET_DATASHEET_CN_URL}'])


class TestAddSub(unittest.TestCase):
    """Test the add_sub method for runtime substitution additions."""

    def setUp(self):
        self.sub = StringSubstituter()
        config = MagicMock()
        config.idf_target = 'esp32'
        config.build_dir = os.path.dirname(os.path.realpath(__file__))
        self.sub.init_sub_strings(config)

    def test_add_sub_basic(self):
        app = MagicMock()
        app.config = MagicMock()
        app.config.build_dir = os.path.dirname(os.path.realpath(__file__))
        self.sub.add_sub(app, {'FLASH_SIZE': '4096'})
        self.assertEqual(self.sub.substitute_strings['{IDF_TARGET_FLASH_SIZE}'], '4096')

    def test_add_sub_strips_ul_suffix(self):
        app = MagicMock()
        app.config = MagicMock()
        app.config.build_dir = os.path.dirname(os.path.realpath(__file__))
        self.sub.add_sub(app, {'VALUE': '(1024UL)'})
        self.assertEqual(self.sub.substitute_strings['{IDF_TARGET_VALUE}'], '1024')

    def test_add_sub_strips_u_suffix(self):
        app = MagicMock()
        app.config = MagicMock()
        app.config.build_dir = os.path.dirname(os.path.realpath(__file__))
        self.sub.add_sub(app, {'COUNT': '(32U)'})
        self.assertEqual(self.sub.substitute_strings['{IDF_TARGET_COUNT}'], '32')

    def test_add_sub_after_substitute(self):
        app = MagicMock()
        app.config = MagicMock()
        app.config.build_dir = os.path.dirname(os.path.realpath(__file__))
        self.sub.add_sub(app, {'MY_VAL': '42'})
        result = self.sub.substitute('Value is {IDF_TARGET_MY_VAL}')
        self.assertEqual(result, 'Value is 42')


class TestCheckContent(unittest.TestCase):

    @patch('esp_docs.esp_extensions.format_esp_target.logging')
    def test_warns_on_unreplaced_tag(self, mock_logging):
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger
        check_content('Still has {IDF_TARGET_UNKNOWN} tag', 'test.rst')
        mock_logger.warning.assert_called_once()

    @patch('esp_docs.esp_extensions.format_esp_target.logging')
    def test_no_warning_on_clean_content(self, mock_logging):
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger
        check_content('All substitutions resolved', 'test.rst')
        mock_logger.warning.assert_not_called()


class TestLocalSubGroupTargets(unittest.TestCase):
    """Extended tests for local substitution with grouped targets."""

    def setUp(self):
        self.sub = StringSubstituter()
        config = MagicMock()
        config.idf_target = 'esp32c3'
        config.build_dir = os.path.dirname(os.path.realpath(__file__))
        self.sub.init_sub_strings(config)

    def test_falls_back_to_default_for_unlisted_target(self):
        content = (
            '{IDF_TARGET_FEATURE:default="generic", esp32="specific"}'
            'Using {IDF_TARGET_FEATURE}'
        )
        result = self.sub.substitute(content)
        self.assertEqual(result, 'Using generic')

    def test_grouped_target_match(self):
        content = (
            '{IDF_TARGET_ARCH:default="RISC-V", esp32, esp32s2, esp32s3="Xtensa"}'
            'Architecture: {IDF_TARGET_ARCH}'
        )
        result = self.sub.substitute(content)
        self.assertEqual(result, 'Architecture: RISC-V')

    def test_multiple_local_subs(self):
        content = (
            '{IDF_TARGET_PIN_A:default="IO1", esp32="IO2"}\n'
            '{IDF_TARGET_PIN_B:default="IO3", esp32="IO4"}\n'
            '{IDF_TARGET_PIN_A} and {IDF_TARGET_PIN_B}'
        )
        result = self.sub.substitute(content)
        self.assertEqual(result, '\n\nIO1 and IO3')


if __name__ == '__main__':
    unittest.main()

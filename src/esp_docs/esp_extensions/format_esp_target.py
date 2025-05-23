import os
import os.path
import pprint
import re

from docutils import io, nodes, statemachine, utils
from docutils.parsers.rst import directives
from docutils.utils.error_reporting import ErrorString, SafeString
from sphinx.directives.other import Include as BaseInclude
from sphinx.util import logging
from esp_docs.constants import TARGET_NAMES, TOOLCHAIN_PREFIX


def setup(app):

    # Config values not available when setup is called
    app.connect('config-inited', lambda _, config: sub.init_sub_strings(config))
    app.connect('source-read', sub.substitute_source_read_cb)

    # Signal to inject any additional substitution
    app.add_event('format-esp-target-add-sub')
    app.connect('format-esp-target-add-sub', sub.add_sub)

    # Override the default include directive to include formatting with idf_target
    # This is needed since there are no source-read events for includes
    app.add_directive('include', FormatedInclude, override=True)

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.2'}


def check_content(content, docname):
    # Log warnings for any {IDF_TARGET} expressions that haven't been replaced
    logger = logging.getLogger(__name__)

    errors = re.findall(r'{IDF_TARGET_.*?}', content)

    for err in errors:
        logger.warning('Badly formated string substitution: {}'.format(err), location=docname)


class StringSubstituter:
    """ Allows for string substitution of target related strings
        before any markup is parsed

        Supports the following replacements (examples shown is for target=esp32s2):
        {IDF_TARGET_NAME}, replaced with the current target name, e.g. ESP32-S2 Beta
        {IDF_TARGET_TOOLCHAIN_PREFIX}, replaced with the toolchain prefix, e.g. xtensa-esp32-elf
        {IDF_TARGET_PATH_NAME}, replaced with the path name, e.g. esp32s2
        {IDF_TARGET_CFG_PREFIX}, replaced with the prefix used for config parameters, e.g. ESP32S2
        {IDF_TARGET_TRM_EN_URL}, replaced with the url to the English technical reference manual
        {IDF_TARGET_TRM_CN_URL}, replaced with the url to the Chinese technical reference manual
        {IDF_TARGET_DATASHEET_EN_URL}, replaced with the url to the English datasheet
        {IDF_TARGET_DATASHEET_CN_URL}, replaced with the url to the Chinese datasheet

        Also supports defines of local (single rst file) with the format:
        {IDF_TARGET_TX_PIN:default="IO3",esp32="IO4",esp32s2="IO5"}

        This will define a replacement of the tag {IDF_TARGET_TX_PIN} in the current rst-file, see e.g. uart.rst for example

        Provides, and listens to the `format-esp-target-add-sub`-event, which can be used to add custom substitutions

    """

    TRM_EN_URL = {'esp8266': 'https://www.espressif.com/sites/default/files/documentation/esp8266-technical_reference_en.pdf',
                  'esp32': 'https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf',
                  'esp32s2': 'https://www.espressif.com/sites/default/files/documentation/esp32-s2_technical_reference_manual_en.pdf',
                  'esp32c3': 'https://www.espressif.com/sites/default/files/documentation/esp32-c3_technical_reference_manual_en.pdf',
                  'esp32s3': 'https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf',
                  'esp32h2': 'https://www.espressif.com/sites/default/files/documentation/esp32-h2_technical_reference_manual_en.pdf',
                  'esp32h21': 'https://www.espressif.com/sites/default/files/documentation/esp32-h21_technical_reference_manual_en.pdf',
                  'esp32h4': 'https://www.espressif.com/sites/default/files/documentation/esp32-h4_technical_reference_manual_en.pdf',
                  'esp32c2': 'https://www.espressif.com/sites/default/files/documentation/esp8684_technical_reference_manual_en.pdf',
                  'esp32c5': 'https://www.espressif.com/sites/default/files/documentation/esp32-c5_technical_reference_manual_en.pdf',
                  'esp32c6': 'https://www.espressif.com/sites/default/files/documentation/esp32-c6_technical_reference_manual_en.pdf',
                  'esp32c61': 'https://www.espressif.com/sites/default/files/documentation/esp32-c61_technical_reference_manual_en.pdf',
                  'esp32p4': 'https://www.espressif.com/sites/default/files/documentation/esp32-p4_technical_reference_manual_en.pdf',
                  'other': 'N/A'}

    TRM_CN_URL = {'esp8266': 'https://www.espressif.com/sites/default/files/documentation/esp8266-technical_reference_cn.pdf',
                  'esp32': 'https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_cn.pdf',
                  'esp32s2': 'https://www.espressif.com/sites/default/files/documentation/esp32-s2_technical_reference_manual_cn.pdf',
                  'esp32c3': 'https://www.espressif.com/sites/default/files/documentation/esp32-c3_technical_reference_manual_cn.pdf',
                  'esp32s3': 'https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_cn.pdf',
                  'esp32h2': 'https://www.espressif.com/sites/default/files/documentation/esp32-h2_technical_reference_manual_cn.pdf',
                  'esp32h21': 'https://www.espressif.com/sites/default/files/documentation/esp32-h21_technical_reference_manual_cn.pdf',
                  'esp32h4': 'https://www.espressif.com/sites/default/files/documentation/esp32-h4_technical_reference_manual_cn.pdf',
                  'esp32c2': 'https://www.espressif.com/sites/default/files/documentation/esp8684_technical_reference_manual_cn.pdf',
                  'esp32c5': 'https://www.espressif.com/sites/default/files/documentation/esp32-c5_technical_reference_manual_cn.pdf',
                  'esp32c6': 'https://www.espressif.com/sites/default/files/documentation/esp32-c6_technical_reference_manual_cn.pdf',
                  'esp32c61': 'https://www.espressif.com/sites/default/files/documentation/esp32-c61_technical_reference_manual_cn.pdf',
                  'esp32p4': 'https://www.espressif.com/sites/default/files/documentation/esp32-p4_technical_reference_manual_cn.pdf',
                  'other': 'N/A'}

    DATASHEET_EN_URL = {'esp8266': 'https://www.espressif.com/sites/default/files/documentation/0a-esp8266ex_datasheet_en.pdf',
                        'esp32': 'https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf',
                        'esp32s2': 'https://www.espressif.com/sites/default/files/documentation/esp32-s2_datasheet_en.pdf',
                        'esp32c3': 'https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf',
                        'esp32s3': 'https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf',
                        'esp32h2': 'https://www.espressif.com/sites/default/files/documentation/esp32-h2_datasheet_en.pdf',
                        'esp32h21': 'https://www.espressif.com/sites/default/files/documentation/esp32-h21_datasheet_en.pdf',
                        'esp32h4': 'https://www.espressif.com/sites/default/files/documentation/esp32-h4_datasheet_en.pdf',
                        'esp32c2': 'https://www.espressif.com/sites/default/files/documentation/esp8684_datasheet_en.pdf',
                        'esp32c5': 'https://www.espressif.com/sites/default/files/documentation/esp32-c5_datasheet_en.pdf',
                        'esp32c6': 'https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf',
                        'esp32c61': 'https://www.espressif.com/sites/default/files/documentation/esp32-c61_datasheet_en.pdf',
                        'esp32p4': 'https://www.espressif.com/sites/default/files/documentation/esp32-p4_datasheet_en.pdf',
                        'other': 'N/A'}

    DATASHEET_CN_URL = {'esp8266': 'https://www.espressif.com/sites/default/files/documentation/0a-esp8266ex_datasheet_cn.pdf',
                        'esp32': 'https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_cn.pdf',
                        'esp32s2': 'https://www.espressif.com/sites/default/files/documentation/esp32-s2_datasheet_cn.pdf',
                        'esp32c3': 'https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_cn.pdf',
                        'esp32s3': 'https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_cn.pdf',
                        'esp32h2': 'https://www.espressif.com/sites/default/files/documentation/esp32-h2_datasheet_cn.pdf',
                        'esp32h21': 'https://www.espressif.com/sites/default/files/documentation/esp32-h21_datasheet_cn.pdf',
                        'esp32h4': 'https://www.espressif.com/sites/default/files/documentation/esp32-h4_datasheet_cn.pdf',
                        'esp32c2': 'https://www.espressif.com/sites/default/files/documentation/esp8684_datasheet_cn.pdf',
                        'esp32c5': 'https://www.espressif.com/sites/default/files/documentation/esp32-c5_datasheet_cn.pdf',
                        'esp32c6': 'https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_cn.pdf',
                        'esp32c61': 'https://www.espressif.com/sites/default/files/documentation/esp32-c61_datasheet_cn.pdf',
                        'esp32p4': 'https://www.espressif.com/sites/default/files/documentation/esp32-p4_datasheet_cn.pdf',
                        'other': 'N/A'}

    RE_PATTERN = re.compile(r'^\s*{IDF_TARGET_(\w+?):(.+?)}', re.MULTILINE)

    SUB_LOG_FILE = "IDF_TARGET-substitutions.txt"

    def __init__(self):
        self.substitute_strings = {}

    def add_pair(self, tag, replace_value):
        self.substitute_strings[tag] = replace_value

    def log_subs_to_file(self, config):
        with open(os.path.join(config.build_dir, self.SUB_LOG_FILE), 'w') as f:
            pprint.pprint(self.substitute_strings, f)
            print('Saved substitution list to %s' % f.name)

    def init_sub_strings(self, config):

        if not config.idf_target:
            return

        self.target_name = config.idf_target
        self.add_pair('{IDF_TARGET_NAME}', TARGET_NAMES[config.idf_target])
        self.add_pair('{IDF_TARGET_PATH_NAME}', config.idf_target)
        self.add_pair('{IDF_TARGET_TOOLCHAIN_PREFIX}', TOOLCHAIN_PREFIX[config.idf_target])
        self.add_pair('{IDF_TARGET_CFG_PREFIX}', TARGET_NAMES[config.idf_target].replace('-', ''))
        self.add_pair('{IDF_TARGET_TRM_EN_URL}', self.TRM_EN_URL[config.idf_target])
        self.add_pair('{IDF_TARGET_TRM_CN_URL}', self.TRM_CN_URL[config.idf_target])
        self.add_pair('{IDF_TARGET_DATASHEET_EN_URL}', self.DATASHEET_EN_URL[config.idf_target])
        self.add_pair('{IDF_TARGET_DATASHEET_CN_URL}', self.DATASHEET_CN_URL[config.idf_target])

        self.log_subs_to_file(config)

    def add_local_subs(self, matches):
        local_sub_strings = {}

        for sub_def in matches:
            if len(sub_def) != 2:
                raise ValueError('IDF_TARGET_X substitution define invalid, val={}'.format(sub_def))

            tag = '{' + 'IDF_TARGET_{}'.format(sub_def[0]) + '}'

            match_default = re.match(r'^\s*default(\s*)=(\s*)\"(.*?)\"', sub_def[1])

            if match_default is None:
                # There should always be a default value
                raise ValueError('No default value in IDF_TARGET_X substitution define, val={}'.format(sub_def))

            match_target = re.match(r'^.*{}\b(.*?)=(\s*)\"(.*?)\"'.format(self.target_name), sub_def[1])

            if match_target is None:
                sub_value = match_default.groups()[2]
            else:
                sub_value = match_target.groups()[2]

            local_sub_strings[tag] = sub_value

        return local_sub_strings

    def substitute(self, content):
        # Add any new local tags that matches the reg.ex.
        sub_defs = re.findall(self.RE_PATTERN, content)

        local_sub_strings = {}

        if len(sub_defs) != 0:
            local_sub_strings.update(self.add_local_subs(sub_defs))

        # Remove the tag defines
        content = re.sub(self.RE_PATTERN, '', content)

        for key in local_sub_strings:
            content = content.replace(key, local_sub_strings[key])

        for key in self.substitute_strings:
            content = content.replace(key, self.substitute_strings[key])

        return content

    def substitute_source_read_cb(self, app, docname, source):
        source[0] = self.substitute(source[0])

        check_content(source[0], docname)

    def add_sub(self, app, subs):
        for name, value in subs.items():
            try:
                sub_name = f'{{IDF_TARGET_{name}}}'

                # We dont do do any complex interpretation of the value,
                # but try to fix the most common formatting "issues"
                sub_val = value.strip('()')
                if sub_val.endswith('UL'):
                    sub_val = sub_val[:-2]
                if sub_val.endswith('U'):
                    sub_val = sub_val[:-1]

                self.add_pair(sub_name, sub_val)
            except Exception:
                # Dont fail build just because we got a value we cannot parse, silently drop it instead
                continue

        self.log_subs_to_file(app.config)


# Shared between read source callbacks and .. include:: directive, but read only
sub = StringSubstituter()


class FormatedInclude(BaseInclude):

    """
    Include and format content read from a separate source file.

    Code is based on the default include directive from docutils
    but extended to also format the content according to IDF target.

    """
    def run(self):

        # For code or literal include blocks we run the normal include
        if 'literal' in self.options or 'code' in self.options:
            return super(FormatedInclude, self).run()

        """Include a file as part of the content of this reST file."""
        if not self.state.document.settings.file_insertion_enabled:
            raise self.warning('"%s" directive disabled.' % self.name)
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1)

        source_dir = os.path.dirname(os.path.abspath(source))

        rel_filename, filename = self.env.relfn2path(self.arguments[0])
        self.arguments[0] = filename
        self.env.note_included(filename)
        path = directives.path(self.arguments[0])

        if path.startswith('<') and path.endswith('>'):
            path = os.path.join(self.standard_include_path, path[1:-1])
        path = os.path.normpath(os.path.join(source_dir, path))

        path = utils.relative_path(None, path)
        path = nodes.reprunicode(path)

        encoding = self.options.get(
            'encoding', self.state.document.settings.input_encoding)
        e_handler = self.state.document.settings.input_encoding_error_handler
        tab_width = self.options.get(
            'tab-width', self.state.document.settings.tab_width)
        try:
            self.state.document.settings.record_dependencies.add(path)
            include_file = io.FileInput(source_path=path,
                                        encoding=encoding,
                                        error_handler=e_handler)
        except UnicodeEncodeError:
            raise self.severe(u'Problems with "%s" directive path:\n'
                              'Cannot encode input file path "%s" '
                              '(wrong locale?).' %
                              (self.name, SafeString(path)))
        except IOError as error:
            raise self.severe(u'Problems with "%s" directive path:\n%s.' %
                              (self.name, ErrorString(error)))
        startline = self.options.get('start-line', None)
        endline = self.options.get('end-line', None)
        try:
            if startline or (endline is not None):
                lines = include_file.readlines()
                rawtext = ''.join(lines[startline:endline])
            else:
                rawtext = include_file.read()
        except UnicodeError as error:
            raise self.severe(u'Problem with "%s" directive:\n%s' %
                              (self.name, ErrorString(error)))

        # Format input
        rawtext = sub.substitute(rawtext)

        # start-after/end-before: no restrictions on newlines in match-text,
        # and no restrictions on matching inside lines vs. line boundaries
        after_text = self.options.get('start-after', None)
        if after_text:
            # skip content in rawtext before *and incl.* a matching text
            after_index = rawtext.find(after_text)
            if after_index < 0:
                raise self.severe('Problem with "start-after" option of "%s" '
                                  'directive:\nText not found.' % self.name)
            rawtext = rawtext[after_index + len(after_text):]
        before_text = self.options.get('end-before', None)
        if before_text:
            # skip content in rawtext after *and incl.* a matching text
            before_index = rawtext.find(before_text)
            if before_index < 0:
                raise self.severe('Problem with "end-before" option of "%s" '
                                  'directive:\nText not found.' % self.name)
            rawtext = rawtext[:before_index]

        include_lines = statemachine.string2lines(rawtext, tab_width,
                                                  convert_whitespace=True)

        self.state_machine.insert_input(include_lines, path)
        return []

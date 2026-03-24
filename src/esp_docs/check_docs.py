import os
import re
import sys

from collections import namedtuple

LogMessage = namedtuple('LogMessage', 'original_text sanitized_text')

SANITIZE_FILENAME_REGEX = re.compile('[^:]*/([^/:]*)(:.*)')
SANITIZE_LINENUM_REGEX = re.compile('([^:]*)(:[0-9]+:)(.*)')
SANITIZE_DUPLICATE_LINENUM_REGEX = re.compile(r'([^:]*)(:[0-9]+\.)(.*)')
SANITIZE_TERMINAL_CONTROL_REGEX = re.compile(r'\x1B\[[0-9;]*[a-zA-Z]|\[[0-9;]+m')

ANSI_RESET = '\033[0m'
ANSI_BOLD = '\033[1m'
ANSI_RED = '\033[31m'
ANSI_YELLOW = '\033[33m'


def sanitize_line(line):
    """
    Clear a log message from insignificant parts

    filter:
        - only filename, no path at the beginning
        - no line numbers after the filename
        - no line numbers from duplicate definitions
        - terminal control characters (like color codes [39;49;00m)
    """

    line = re.sub(SANITIZE_TERMINAL_CONTROL_REGEX, '', line)  # Remove terminal control characters first
    line = re.sub(SANITIZE_FILENAME_REGEX, r'\1\2', line)
    line = re.sub(SANITIZE_LINENUM_REGEX, r'\1:line:\3', line)
    line = re.sub(SANITIZE_DUPLICATE_LINENUM_REGEX, r'\1:line.\3', line)
    return line


def supports_color():
    if os.environ.get('NO_COLOR'):
        return False

    if os.environ.get('CI'):
        return True

    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


def style_text(text, color=None, bold=False):
    if not supports_color():
        return text

    styles = []
    if bold:
        styles.append(ANSI_BOLD)
    if color == 'red':
        styles.append(ANSI_RED)
    elif color == 'yellow':
        styles.append(ANSI_YELLOW)

    if not styles:
        return text

    return ''.join(styles) + text + ANSI_RESET


def format_path_for_display(path):
    try:
        rel_path = os.path.relpath(path)
        if len(rel_path) < len(path):
            return rel_path
    except ValueError:
        pass

    return path


def warning_type_from_log(log_file):
    basename = os.path.basename(log_file).lower()
    if 'doxygen' in basename:
        return 'Doxygen'

    return 'Sphinx'


def group_log_messages(messages, text_attr):
    grouped = []

    for msg in messages:
        text = getattr(msg, text_attr).rstrip('\n')
        if grouped and text[:1].isspace():
            grouped[-1] += '\n' + text
        else:
            grouped.append(text)

    return grouped


def check_docs(language, target, log_file, known_warnings_file, out_sanitized_log_file):
    """
    Check for Documentation warnings in `log_file`: should only contain (fuzzy) matches to `known_warnings_file`

    It prints all unknown messages with `target`/`language` prefix
    It leaves `out_sanitized_log_file` file for observe and debug
    """

    # Sanitize all messages
    all_messages = list()

    try:
        with open(log_file) as f, open(out_sanitized_log_file, 'w') as o:
            for line in f:
                sanitized_line = sanitize_line(line)
                all_messages.append(LogMessage(line, sanitized_line))
                o.write(sanitized_line)
    except FileNotFoundError:
        print(style_text('=== BUILD FAILED ===', color='red', bold=True))
        print(style_text('{}: expected warning log was not generated'.format(format_path_for_display(log_file)), color='red', bold=True))
        return 1

    known_messages = list()

    try:
        with open(known_warnings_file) as k:
            for known_line in k:
                known_messages.append(known_line)
    except FileNotFoundError:
        pass

    if 'doxygen' in known_warnings_file:
        # Clean a known Doxygen limitation: it's expected to always document anonymous
        # structs/unions but we don't do this in our docs, so filter these all out with a regex
        # (this won't match any named field, only anonymous members -
        # ie the last part of the field is is just <something>::@NUM not <something>::name)
        RE_ANONYMOUS_FIELD = re.compile(r'.+:line: warning: parameters of member [^:\s]+(::[^:\s]+)*(::@\d+)+ are not \(all\) documented')
        all_messages = [msg for msg in all_messages if not re.match(RE_ANONYMOUS_FIELD, msg.sanitized_text)]

    # Collect all new messages that are not match with the known messages.
    # The order is an important.
    new_messages = list()
    known_idx = 0
    for msg in all_messages:
        try:
            known_idx = known_messages.index(msg.sanitized_text, known_idx)
        except ValueError:
            new_messages.append(msg)

    if new_messages:
        build_id = '%s/%s' % (language, target)
        warning_type = warning_type_from_log(log_file)
        display_log = format_path_for_display(log_file)
        display_sanitized_log = format_path_for_display(out_sanitized_log_file)
        display_known_warnings = format_path_for_display(known_warnings_file)
        grouped_messages = group_log_messages(new_messages, 'sanitized_text')

        print('\n%s' % style_text('=== BUILD FAILED ===', color='red', bold=True))
        print(style_text('%s: %s warnings are treated as errors (fatal)' % (build_id, warning_type), color='red', bold=True))
        print('%s: This job fails on new warnings.' % build_id)
        print('%s: New %s warning entries: %d' % (build_id, warning_type.lower(), len(grouped_messages)))
        print('%s: Warning log: %s' % (build_id, display_log))
        print('%s: Sanitized log: %s' % (build_id, display_sanitized_log))
        print('%s: Known warnings: %s' % (build_id, display_known_warnings))
        print('%s: New warning entries:' % build_id)

        for entry in grouped_messages:
            formatted_entry = entry.replace('\n', '\n    ')
            print(style_text('%s:   - %s' % (build_id, formatted_entry), color='yellow'))

        return 1

    return 0

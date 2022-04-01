import re

from collections import namedtuple

LogMessage = namedtuple('LogMessage', 'original_text sanitized_text')

SANITIZE_FILENAME_REGEX = re.compile('[^:]*/([^/:]*)(:.*)')
SANITIZE_LINENUM_REGEX = re.compile('([^:]*)(:[0-9]+:)(.*)')
SANITIZE_DUPLICATE_LINENUM_REGEX = re.compile(r'([^:]*)(:[0-9]+\.)(.*)')


def sanitize_line(line):
    """
    Clear a log message from insignificant parts

    filter:
        - only filename, no path at the beginning
        - no line numbers after the filename
        - no line numbers from duplicate definitions
    """

    line = re.sub(SANITIZE_FILENAME_REGEX, r'\1\2', line)
    line = re.sub(SANITIZE_LINENUM_REGEX, r'\1:line:\3', line)
    line = re.sub(SANITIZE_DUPLICATE_LINENUM_REGEX, r'\1:line.\3', line)
    return line


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
        print("{} not generated".format(log_file))
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
        print('\n%s/%s: Build failed due to new/different warnings (%s):\n' % (language, target, log_file))
        for msg in new_messages:
            print('%s/%s: %s' % (language, target, msg.original_text), end='')
        print('\n%s/%s: (Check files %s and %s for full details.)' % (language, target, known_warnings_file, log_file))

        return 1

    return 0

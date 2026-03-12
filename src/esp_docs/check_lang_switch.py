#!/usr/bin/env python3
# coding=utf-8
#
# This script checks that all RST files included in toctree directives have
# the appropriate :link_to_translation: directive (e.g., :link_to_translation:`zh_CN:[中文]`
# for English files and :link_to_translation:`en:[English]` for Chinese files).
#
# Copyright 2026 Espressif Systems (Shanghai) PTE LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import fnmatch
import os
import re
import sys


LANGUAGES = ['en', 'zh_CN']
LINK_TO_TRANSLATION_PATTERN = re.compile(r':link_to_translation:`([^`]+)`')
TOC_TREE_PATTERN = re.compile(r'\.\.\s+toctree::', re.IGNORECASE)
TOC_ENTRY_PATTERN = re.compile(r'^\s+([^\s<:]+)', re.MULTILINE)


def find_rst_files(docs_dir, language):
    """Find all RST files in the specified language directory."""
    lang_dir = os.path.join(docs_dir, language)
    if not os.path.exists(lang_dir):
        return []

    rst_files = []
    for root, dirs, files in os.walk(lang_dir):
        # Skip hidden directories and build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '_build']
        for file in files:
            if file.endswith('.rst'):
                rst_files.append(os.path.join(root, file))

    return rst_files


def parse_toctree_entries(rst_file, target=None):
    """Parse toctree entries from an RST file.

    Args:
        rst_file: Path to the RST file containing the toctree
        target: Target name (e.g., 'esp32', 'esp32s2') to replace {IDF_TARGET_PATH_NAME} macro
    """
    entries = []

    try:
        with open(rst_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError) as e:
        print("Warning: Could not read file {}: {}".format(rst_file, e), file=sys.stderr)
        return entries

    # Find all toctree directives
    toctree_matches = list(TOC_TREE_PATTERN.finditer(content))

    for match in toctree_matches:
        # Find the content block after the toctree directive
        start_pos = match.end()

        # Find the next directive or non-indented content that ends the toctree
        # Look for lines that are indented (toctree entries) or blank lines
        lines = content[start_pos:].split('\n')
        found_entries = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Skip blank lines (they're allowed between entries)
            if not stripped:
                continue

            # Check if this is a new directive (starts with ..) - this ends the toctree
            if stripped.startswith('..'):
                break

            # Check if this is a toctree option (starts with :)
            if stripped.startswith(':'):
                continue

            # Check if line is indented (toctree entries are indented)
            # If we've found entries before and this line is not indented, we've reached the end
            if found_entries and not line.startswith((' ', '\t')):
                # Non-indented content line - end of this toctree
                break

            # Only process indented lines as toctree entries
            if not line.startswith((' ', '\t')):
                continue

            # This should be a toctree entry
            # First, check if there's a label format: "Label <entry>" or just "entry"
            stripped_line = stripped

            # Handle entries with labels like "Page One <page1>"
            if '<' in stripped_line and '>' in stripped_line:
                # Extract the entry from inside < >
                entry_match = re.search(r'<([^>]+)>', stripped_line)
                if entry_match:
                    entry = entry_match.group(1).strip()
                else:
                    # Fallback: use everything before <
                    entry = stripped_line.split('<')[0].strip()
            else:
                # Handle entries with filter tags like ":filter: entry"
                if ':' in stripped_line and not stripped_line.startswith(':'):
                    # Check if it's a filter tag
                    parts = stripped_line.split(':', 1)
                    if len(parts) == 2:
                        entry = parts[1].strip()
                    else:
                        entry = stripped_line
                else:
                    # Simple entry without label or filter
                    # Use the whole stripped line as the entry
                    entry = stripped_line

            # Clean up the entry
            entry = entry.strip()

            # Replace {IDF_TARGET_PATH_NAME} macro with target value if provided
            if target and '{IDF_TARGET_PATH_NAME}' in entry:
                entry = entry.replace('{IDF_TARGET_PATH_NAME}', target)

            # Remove .rst extension if present
            if entry.endswith('.rst'):
                entry = entry[:-4]

            if entry:
                entries.append(entry)
                found_entries = True

    return entries


def resolve_toctree_entry(entry, base_dir, language, containing_file=None):
    """Resolve a toctree entry to an actual RST file path.

    Args:
        entry: The toctree entry (e.g., 'page1', 'folder/page1')
        base_dir: Base docs directory (e.g., 'docs')
        language: Language directory (e.g., 'en')
        containing_file: Path to the RST file containing the toctree (optional)

    Returns:
        Resolved absolute path to the RST file, or None if not found
    """
    # Remove .rst extension if present
    if entry.endswith('.rst'):
        entry = entry[:-4]

    # Determine the base directory for resolving relative paths
    if containing_file:
        # Use the directory of the containing file as the base
        containing_dir = os.path.dirname(containing_file)
        # Remove the language directory from the path to get the relative base
        # containing_file is like: docs/en/index.rst or docs/en/folder/index.rst
        # containing_dir is like: docs/en or docs/en/folder
        # We want to resolve relative to this directory
        if '/' in entry:
            # Relative path like 'folder/page1' - resolve relative to containing_dir
            rst_path = os.path.join(containing_dir, entry + '.rst')
        else:
            # Simple entry like 'page1' - same directory as containing file
            rst_path = os.path.join(containing_dir, entry + '.rst')
    else:
        # Fallback: resolve relative to language directory
        if '/' in entry:
            # Relative path from language directory
            rst_path = os.path.join(base_dir, language, entry + '.rst')
        else:
            # Same directory as language directory
            rst_path = os.path.join(base_dir, language, entry + '.rst')

    # Normalize the path
    rst_path = os.path.normpath(rst_path)

    # Check if file exists
    if os.path.exists(rst_path) and os.path.isfile(rst_path):
        return rst_path

    # Try with index.rst if the entry points to a directory
    # If entry is 'folder' and folder/index.rst exists, use that
    entry_dir = os.path.join(os.path.dirname(rst_path), os.path.basename(entry))
    if os.path.isdir(entry_dir):
        index_path = os.path.join(entry_dir, 'index.rst')
        if os.path.exists(index_path):
            return index_path

    # Don't fallback to index.rst in the containing directory - that's wrong
    # If the file doesn't exist, return None
    return None


def check_if_translation_only_has_link(translation_file, original_language):
    """Check if translation file only contains an include directive pointing to the original file.

    When a translation is not ready, the file typically contains only:
    .. include:: ../../en/api-guides/build-system-v2.rst

    Args:
        translation_file: Path to the translation file
        original_language: Language of the original file ('en' or 'zh_CN')

    Returns:
        True if the file only contains an include directive to the original, False otherwise
    """
    if not os.path.exists(translation_file):
        return False

    try:
        with open(translation_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return False

    # Remove whitespace and check if content is essentially empty except for include directive
    lines = [line.strip() for line in content.split('\n') if line.strip()]

    # If file has very few lines, it might be a placeholder
    if len(lines) <= 3:
        # Check if it contains an .. include:: directive pointing to the original language
        # Pattern: .. include:: ../../en/... or .. include:: ../en/... etc.
        include_pattern = re.compile(r'\.\.\s+include::\s+(.+)', re.IGNORECASE)
        matches = include_pattern.findall(content)

        for match in matches:
            include_path = match.strip()
            # Check if the include path points to the original language folder
            # Paths like: ../../en/..., ../en/..., en/..., /path/to/en/...
            if '/' + original_language + '/' in include_path or include_path.startswith(original_language + '/'):
                # This is a placeholder file that only includes the original
                return True

    return False


def check_link_to_translation(rst_file, expected_language, docs_dir):
    """Check if an RST file has the appropriate link_to_translation directive.

    Args:
        rst_file: Path to the RST file to check
        expected_language: Expected language in the link (e.g., 'zh_CN' for English files)
        docs_dir: Base docs directory for resolving translation file paths
    """
    try:
        with open(rst_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError) as e:
        return False, "Could not read file: {}".format(e)

    # Find all link_to_translation directives
    matches = LINK_TO_TRANSLATION_PATTERN.findall(content)

    if not matches:
        # Check if translation file doesn't exist, or if current file or translation file is a placeholder
        # Get the language of the current file
        rel_path = os.path.relpath(rst_file, docs_dir)
        if rel_path.startswith('en/'):
            current_language = 'en'
            translation_language = 'zh_CN'
        elif rel_path.startswith('zh_CN/'):
            current_language = 'zh_CN'
            translation_language = 'en'
        else:
            # Can't determine, report error
            return False, "Missing :link_to_translation: directive"

        # Check if the current file itself is a placeholder (includes the translation language file)
        if check_if_translation_only_has_link(rst_file, translation_language):
            # Current file is a placeholder that includes the translation, don't report error
            return True, None

        # Check if translation file doesn't exist
        translation_path = rst_file.replace('/' + current_language + '/', '/' + translation_language + '/')
        if not os.path.exists(translation_path):
            # Translation file doesn't exist, don't report error
            return True, None

        # Check if translation file is a placeholder (includes the current/original language file)
        if check_if_translation_only_has_link(translation_path, current_language):
            # Translation file is a placeholder that includes the original, don't report error
            return True, None

        return False, "Missing :link_to_translation: directive"

    # Check for multiple links - should only have one
    if len(matches) > 1:
        return False, "Multiple :link_to_translation: directives found (expected exactly one)"

    # Check if the match has the expected language
    match = matches[0]
    # Parse the language from the match (format: "zh_CN:[中文]" or "en:[English]")
    parts = match.split(':', 1)
    if len(parts) >= 1:
        lang = parts[0].strip()
        if lang == expected_language:
            return True, None
        else:
            return False, "Incorrect :link_to_translation: directive (found '{}', expected '{}')".format(lang, expected_language)

    return False, "Missing :link_to_translation:`{}:` directive".format(expected_language)


def load_excluded_files_from_warnings(docs_dir):
    """Load list of files to ignore from lang-linkcheck-warnings.txt.

    The warnings file should contain one file path per line (relative to docs_dir,
    with language prefix and .rst extension, e.g., "en/page.rst" or "zh_CN/folder/page.rst").
    Lines starting with # are treated as comments and ignored.

    Wildcards are supported: use * to match any string and ? to match any single character.
    Examples:
      en/getting-started/*       matches all .rst under en/getting-started/
      en/**/internal.rst          (fnmatch does not support **; use * for one segment)
      zh_CN/api-reference/*.rst  matches all .rst in zh_CN/api-reference/

    Args:
        docs_dir: Base docs directory

    Returns:
        Tuple of (exact_paths, patterns) where exact_paths is a set of literal paths to ignore,
        and patterns is a list of fnmatch patterns (entries containing * or ?).
    """
    exact_paths = set()
    patterns = []
    warnings_file = os.path.join(docs_dir, 'lang-linkcheck-warnings.txt')

    if not os.path.exists(warnings_file):
        return exact_paths, patterns

    try:
        with open(warnings_file, 'r', encoding='utf-8') as f:
            for line in f:
                # Strip whitespace and skip empty lines and comments
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Normalize path separators
                normalized = line.replace('\\', '/')
                if '*' in normalized or '?' in normalized:
                    patterns.append(normalized)
                else:
                    exact_paths.add(normalized)
    except (IOError, UnicodeDecodeError) as e:
        if os.environ.get('DEBUG_LANG_LINKCHECK', ''):
            print("Warning: Could not read lang-linkcheck-warnings.txt: {}".format(e), file=sys.stderr)

    return exact_paths, patterns


def check_lang_switch(docs_dir, language='en', target=None):
    """Check translation links for files in toctrees for a given language.

    Args:
        docs_dir: Base docs directory
        language: Language to check ('en' or 'zh_CN')
        target: Target name (e.g., 'esp32', 'esp32s2') to replace {IDF_TARGET_PATH_NAME} macro

    Returns:
        Tuple of (errors, passed_files) where:
        - errors: List of (file_path, error_msg) tuples for files missing translation links
        - passed_files: List of file paths that passed the check
    """
    errors = []
    passed_files = []
    checked_files = set()

    # Load excluded files from warnings file (exact paths and wildcard patterns)
    ignored_exact, ignored_patterns = load_excluded_files_from_warnings(docs_dir)

    # Find all RST files in this language
    rst_files = find_rst_files(docs_dir, language)

    # Determine the other language
    other_language = 'zh_CN' if language == 'en' else 'en'

    # Collect all files referenced in toctrees
    toctree_files = set()

    for rst_file in rst_files:
        entries = parse_toctree_entries(rst_file, target)
        if entries:
            rel_rst_file = os.path.relpath(rst_file, docs_dir)
            # Debug: show what was parsed from each file
            if os.environ.get('DEBUG_TOCTREE', ''):
                print(f"  [{language}] {rel_rst_file}: found {len(entries)} toctree entries: {entries}")
        for entry in entries:
            resolved_file = resolve_toctree_entry(entry, docs_dir, language, rst_file)
            if resolved_file and os.path.exists(resolved_file):
                toctree_files.add(resolved_file)
            elif resolved_file:
                # File path was resolved but doesn't exist - might be a macro issue
                rel_rst_file = os.path.relpath(rst_file, docs_dir)
                if os.environ.get('DEBUG_TOCTREE', ''):
                    print(f"    Warning: Resolved '{entry}' -> {os.path.relpath(resolved_file, docs_dir)} (not found)")

    # Always check index.rst files (homepages) even if they're not in a toctree
    lang_dir = os.path.join(docs_dir, language)
    index_file = os.path.join(lang_dir, 'index.rst')
    if os.path.exists(index_file):
        toctree_files.add(index_file)

    # Check each file in toctree
    for rst_file in toctree_files:
        if rst_file in checked_files:
            continue
        checked_files.add(rst_file)

        rel_path = os.path.relpath(rst_file, docs_dir)

        # Check if this file should be ignored (exact path or wildcard pattern)
        # rel_path is like "en/page.rst" or "zh_CN/folder/page.rst"
        if rel_path in ignored_exact:
            continue
        if any(fnmatch.fnmatch(rel_path, p) for p in ignored_patterns):
            continue

        has_link, error_msg = check_link_to_translation(rst_file, other_language, docs_dir)
        if not has_link:
            errors.append((rel_path, error_msg))
        else:
            passed_files.append(rel_path)

    return errors, passed_files


def run_lang_linkcheck(languages_to_check, target=None):
    """Run the language link check and print results.

    This function runs from the current working directory, which should be the docs directory.

    Args:
        languages_to_check: List of languages to check (e.g., ['en', 'zh_CN'])
        target: Target name (e.g., 'esp32', 'esp32s2') to replace {IDF_TARGET_PATH_NAME} macro

    Returns:
        Exit code: 0 if successful, 1 if errors found
    """
    # Use current working directory as docs directory
    docs_dir = os.getcwd()

    if not os.path.exists(docs_dir):
        print("Error: Current directory '{}' does not exist".format(docs_dir), file=sys.stderr)
        return 1

    all_errors = []
    all_passed_files = []
    errors_by_language = {'en': [], 'zh_CN': []}

    for language in languages_to_check:
        errors, passed_files = check_lang_switch(docs_dir, language, target)
        errors_by_language[language] = errors
        all_errors.extend(errors)
        all_passed_files.extend(passed_files)

    # Print results organized by language and missing link type
    print("\n" + "="*80)
    print("TRANSLATION LINK CHECK RESULTS")
    print("="*80)

    # List files missing Chinese translation links
    en_missing_zh = [e for lang in ['en'] if lang in languages_to_check for e in errors_by_language[lang]]
    if en_missing_zh:
        print("\n[EN] Files missing link to Chinese translation ({}):".format(len(en_missing_zh)))
        for file_path, error_msg in en_missing_zh:
            print("  ✗ {}: {}".format(file_path, error_msg))
    else:
        if 'en' in languages_to_check:
            print("\n[EN] ✓ All files have link to Chinese translation")

    # List files missing English translation links
    zh_missing_en = [e for lang in ['zh_CN'] if lang in languages_to_check for e in errors_by_language[lang]]
    if zh_missing_en:
        print("\n[ZH_CN] Files missing link to English translation ({}):".format(len(zh_missing_en)))
        for file_path, error_msg in zh_missing_en:
            print("  ✗ {}: {}".format(file_path, error_msg))
    else:
        if 'zh_CN' in languages_to_check:
            print("\n[ZH_CN] ✓ All files have link to English translation")

    # List files that passed the check
    if all_passed_files:
        print("\n[PASSED] Files with correct translation links ({}):".format(len(all_passed_files)))
        for file_path in sorted(all_passed_files):
            print("  ✓ {}".format(file_path))

    if all_errors:
        print("\n" + "="*80)
        print("ERROR: Found {} file(s) missing translation links.".format(len(all_errors)))
        print("Please add the appropriate :link_to_translation: directive to these files.")
        print("\nExample:")
        print("  For English files: :link_to_translation:`zh_CN:[中文]`")
        print("  For Chinese files: :link_to_translation:`en:[English]`")
        print("="*80)
        return 1
    else:
        print("\n" + "="*80)
        print("SUCCESS: All files in toctrees have translation links.")
        print("="*80)
        return 0

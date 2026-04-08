from __future__ import unicode_literals

import json
import os


def parse_modified_files_arg(modified_files):
    if not modified_files:
        return []

    normalized_paths = []
    for value in modified_files:
        if not value:
            continue

        normalized_paths.extend(
            path for path in value.split(';') if path
        )

    return normalized_paths


def normalize_modified_file_path(file_path, project_path=None):
    normalized_path = file_path

    if project_path and os.path.isabs(normalized_path):
        normalized_path = os.path.relpath(normalized_path, project_path)

    normalized_path = os.path.normpath(normalized_path).replace('\\', '/')

    if normalized_path == '.':
        return ''

    while normalized_path.startswith('./'):
        normalized_path = normalized_path[2:]

    return normalized_path


def get_modified_files(config):
    modified_files = config.modified_files

    if not modified_files:
        return set()

    if isinstance(modified_files, str):
        modified_files = json.loads(modified_files)

    return {
        normalize_modified_file_path(path, config.project_path)
        for path in modified_files
        if path
    }

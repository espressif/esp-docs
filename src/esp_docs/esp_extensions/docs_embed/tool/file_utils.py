"""Utility functions for file operations: loading and saving JSON, YAML, and TOML files.

This module provides functions for safely loading and saving configuration files
with proper error handling, encoding, and formatting. All functions support both
relative and absolute paths and create parent directories as needed.
"""


from pathlib import Path
import json
import sys
from typing import Any, Dict

import click
import yaml
import tomli_w

def load_json(file_path: Path) -> Dict[str, Any]:
    """Load and parse a JSON file with error handling.

    Args:
        file_path: Path to the JSON file to load

    Returns:
        Dictionary containing the parsed JSON data

    Raises:
        SystemExit: If file not found or JSON is invalid
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        click.echo(f"Error: JSON file not found at {file_path}", err=True)
        sys.exit(1)
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON in {file_path}: {e}", err=True)
        sys.exit(1)


def load_yaml(file_path: Path) -> Dict[str, Any]:
    """Load and parse a YAML file with error handling.

    Args:
        file_path: Path to the YAML file to load

    Returns:
        Dictionary containing the parsed YAML data

    Raises:
        SystemExit: If file not found or YAML is invalid
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        click.echo(f"Error: YAML file not found at {file_path}", err=True)
        sys.exit(1)
    except yaml.YAMLError as e:
        click.echo(f"Error: Invalid YAML in {file_path}: {e}", err=True)
        sys.exit(1)


def save_yaml(file_path: Path, data: Dict[str, Any], override: bool = False) -> None:
    """Save data as a YAML file with proper formatting.

    Creates parent directories if they don't exist. Uses safe_dump to avoid
    arbitrary code execution and formats output for readability.

    Args:
        file_path: Path where the YAML file will be saved
        data: Dictionary to serialize as YAML
        override: If False, skip if file exists; if True, overwrite existing file

    Raises:
        SystemExit: If file write operation fails
    """
    if file_path.exists() and not override:
        click.echo(f"Warning: {file_path} already exists. Use --override to overwrite.")
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, indent=2)
    except Exception as e:
        click.echo(f"Error: Failed to write YAML to {file_path}: {e}", err=True)
        sys.exit(1)

    click.echo(f"Saved: {file_path}")


def save_json(file_path: Path, data: Dict[str, Any], override: bool = False) -> None:
    """Save data as a JSON file with proper formatting.

    Creates parent directories if they don't exist. Uses 2-space indentation
    for readability and preserves Unicode characters.

    Args:
        file_path: Path where the JSON file will be saved
        data: Dictionary to serialize as JSON
        override: If False, skip if file exists; if True, overwrite existing file

    Raises:
        SystemExit: If file write operation fails
    """
    if file_path.exists() and not override:
        click.echo(f"Warning: {file_path} already exists. Use --override to overwrite.")
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, separators=(',', ': '))
    except Exception as e:
        click.echo(f"Error: Failed to write JSON to {file_path}: {e}", err=True)
        sys.exit(1)

    click.echo(f"Saved: {file_path}")


def save_toml(file_path: Path, data: Dict[str, Any], override: bool = False) -> None:
    """Save data as a TOML file with proper formatting.

    Creates parent directories if they don't exist. TOML format is commonly used
    for configuration files and is more human-readable than JSON.

    Args:
        file_path: Path where the TOML file will be saved
        data: Dictionary to serialize as TOML
        override: If False, skip if file exists; if True, overwrite existing file

    Raises:
        SystemExit: If file write operation fails
    """
    if file_path.exists() and not override:
        click.echo(f"Warning: {file_path} already exists. Use --override to overwrite.")
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(file_path, 'wb') as f:
            tomli_w.dump(data, f)
    except Exception as e:
        click.echo(f"Error: Failed to write TOML to {file_path}: {e}", err=True)
        sys.exit(1)

    click.echo(f"Saved: {file_path}")

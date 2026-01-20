#!/usr/bin/env python3
"""
Diagram and CI synchronization CLI for Wokwi examples.

This module provides command-line tools for managing Wokwi diagram files,
CI configuration, and ESP LaunchPad configuration for embedded system projects.
"""

import sys
import click
from esp_docs.esp_extensions.docs_embed.tool.wokwi_tool import (
    DiagramSync,
    target_to_boards,
)


# CLI Commands
@click.group(
    help="docs-embed: Utility to manage Wokwi diagrams and ESP LaunchPad configurations"
)
@click.option(
    "--path",
    default=".",
    type=str,
    help="Path to the directory with examples",
)
@click.pass_context
def main(ctx: click.Context, path: str):
    """Main command group for diagram synchronization tools.

    All commands operate on a specified directory containing project files.
    By default, uses the current directory (.).
    """
    ctx.ensure_object(dict)
    ctx.obj["path"] = path


@main.command(name="init-diagram")
@click.option(
    "--platforms",
    type=str,
    required=True,
    help=f"Comma-separated list of platforms to initialise. Valid: {', '.join(target_to_boards.keys())}",
)
@click.option(
    "--override/--no-override",
    type=bool,
    default=False,
    help="Override existing files",
)
@click.pass_context
def init_project(ctx: click.Context, platforms: str, override: bool):
    """Initialize a new project with Wokwi diagrams and CI configuration.

    Creates default diagram files and initializes the CI configuration for the
    specified platforms.

    Examples:
      docs-embed init-diagram --platforms esp32,esp32s2
      docs-embed --path folder/examples init-diagram --platforms esp32,esp32s2 --override
    """
    try:
        sync = DiagramSync(ctx.obj.get("path"))
        platforms_list = [p.strip() for p in platforms.split(",") if p.strip()]
        allowed = set(target_to_boards.keys())
        invalid = [p for p in platforms_list if p not in allowed]

        if invalid:
            click.echo(
                f"Invalid platform(s): {', '.join(invalid)}. Allowed: {', '.join(sorted(allowed))}",
                err=True,
            )
            sys.exit(1)

        sync.init_project(platforms_list, override)
    except FileNotFoundError as e:
        click.echo(f"Error: Directory not found - {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--platform",
    help="Specific platform to process (e.g., esp32, esp32s2, esp32s3). If not specified, processes all diagrams.",
)
@click.option(
    "--override/--no-override",
    default=False,
    help="Override existing ci.yml content in the upload-binary section",
)
@click.pass_context
def ci_from_diagram(ctx: click.Context, platform, override):
    """Generate ci.yml from diagram files.

    Reads diagram.*.json files and extracts their configuration to generate
    or update the ci.yml file with the upload-binary section.

    Examples:
      docs-embed ci-from-diagram
      docs-embed --path folder/examples ci-from-diagram --platform esp32 --override
    """
    try:
        sync = DiagramSync(ctx.obj.get("path"))
        click.echo("Generating ci.yml from diagram files...")
        sync.generate_ci_from_diagram(platform, override)
    except FileNotFoundError as e:
        click.echo(f"Error: Directory not found - {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--platform",
    help="Specific platform to process (e.g., esp32, esp32s2, esp32s3). If not specified, processes all platforms in ci.yml.",
)
@click.option(
    "--override/--no-override",
    default=False,
    help="Override existing diagram files",
)
@click.pass_context
def diagram_from_ci(ctx: click.Context, platform, override):
    """Generate diagram files from ci.yml configuration.

    Reads platform-specific diagram configurations from ci.yml and generates
    diagram.*.json files by merging them with default diagram templates.

    Examples:
      docs-embed diagram-from-ci
      docs-embed --path folder/examples diagram-from-ci --platform esp32 --override
    """
    try:
        sync = DiagramSync(ctx.obj.get("path"))
        click.echo("Generating diagram files from ci.yml...")
        sync.generate_diagram_from_ci(platform, override)
    except FileNotFoundError as e:
        click.echo(f"Error: Directory not found - {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--storage-url-prefix",
    type=str,
    required=True,
    envvar="STORAGE_URL_PREFIX",
    help="Base URL prefix where firmware binaries are hosted",
)
@click.option(
    "--repo-url-prefix",
    type=str,
    required=True,
    envvar="REPO_URL_PREFIX",
    help="Base URL prefix for the repository resources",
)
@click.option(
    "--override/--no-override",
    default=False,
    help="Override existing launchpad.toml file",
)
@click.pass_context
def launchpad_config(ctx: click.Context, storage_url_prefix, repo_url_prefix, override):
    """Generate ESP LaunchPad configuration file.

    Creates a TOML configuration file for ESP LaunchPad with firmware images,
    supported chipsets, and project metadata extracted from ci.yml.

    Can use environment variables:
      - STORAGE_URL_PREFIX: URL prefix for firmware binaries
      - REPO_URL_PREFIX: URL prefix for repository

    Examples:
      docs-embed launchpad-config --storage-url-prefix https://storage.url --repo-url-prefix https://repo.url
      docs-embed --path folder/examples launchpad-config \\
        --storage-url-prefix https://storage.url \\
        --repo-url-prefix https://repo.url --override
    """
    try:
        sync = DiagramSync(ctx.obj.get("path"))
        click.echo("Generating ESP LaunchPad configuration...")
        sync.generate_launchpad_config(storage_url_prefix, repo_url_prefix, override)
    except FileNotFoundError as e:
        click.echo(f"Error: Directory not found - {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

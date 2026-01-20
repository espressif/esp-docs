#!/usr/bin/env python3
"""
Diagram and CI synchronization script for ESP32 Arduino examples.

This module provides tools for synchronizing Wokwi diagram files with CI configuration
and generating LaunchPad configuration files from project metadata.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import click

from esp_docs.esp_extensions.docs_embed.sphinx.helpers import url_join
from esp_docs.esp_extensions.docs_embed.tool.file_utils import load_json, load_yaml, save_yaml, save_json, save_toml

# Mapping of platform names to Wokwi board types
target_to_boards = {
    'esp32': 'board-esp32-devkit-c-v4',
    'esp32c3': 'board-esp32-c3-devkitm-1',
    'esp32c6': 'board-esp32-c6-devkitc-1',
    'esp32h2': 'board-esp32-h2-devkitm-1',
    'esp32p4': 'board-esp32-p4-function-ev',
    'esp32s2': 'board-esp32-s2-devkitm-1',
    'esp32s3': 'board-esp32-s3-devkitc-1',
}

# File naming constants
DIAGRAM_FILE_PREFIX = "diagram."
DIAGRAM_FILE_SUFFIX = ".json"
LAUNCHPAD_CONFIG_FILE = "launchpad.toml"
CI_CONFIG_FILE = "ci.yml"
README_FILE = "README.md"


class DiagramSync:
    """Main class for synchronizing diagram files with CI configuration."""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        if not self.base_path.exists():
            raise FileNotFoundError(f"Base path {self.base_path} does not exist")
        if not self.base_path.is_dir():
            raise NotADirectoryError(f"Base path {self.base_path} is not a directory")

        self.serial_connections = [
            ["esp:RX", "$serialMonitor:TX", "", []],
            ["esp:TX", "$serialMonitor:RX", "", []]
        ]

        # Default diagram configuration
        self.default_diagram_config = {
            'version': 1,
            'author': 'Espressif Systems',
            'editor': 'wokwi',
            'parts': [],
            'dependencies': {}
        }

    def init_project(self, platforms_list: List[str], override: bool) -> None:
        """Initialize project by generating diagrams for specified platforms.

        Args:
            platforms_list: List of platform names to generate diagrams for
            override: Whether to overwrite existing diagram files
        """
        click.echo(f"Initializing project in {self.base_path}")

        for platform in platforms_list:
            click.echo(f"Generating diagram for platform: {platform}")
            self.generate_diagram(platform, override, {})

    # Data Processing
    def is_serial_connection(self, connection: List[str]) -> bool:
        """Return True if the connection is a serial monitor connection."""
        return connection[:3] in [conn[:3] for conn in self.serial_connections]

    def filter_parts(self, parts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out board parts from diagram parts."""
        return [part for part in parts if not part.get("type", "").startswith("board-")]

    def filter_connections(self, connections: List[List[str]]) -> List[List[str]]:
        """Filter out serial monitor connections."""
        return [conn for conn in connections if not self.is_serial_connection(conn)]

    def get_platforms_from_ci(self) -> List[str]:
        """Get all platforms from ci.yml targets.

        Reads the ci.yml file and extracts platform names from the
        upload-binary section.

        Returns:
            List of platform names from ci.yml, or empty list if file doesn't exist
        """
        ci_file = self.base_path / CI_CONFIG_FILE
        if not ci_file.exists():
            return []

        ci_data = load_yaml(ci_file)
        return ci_data.get("upload-binary", {}).get("targets", [])

    def get_platforms_from_diagrams(self) -> List[str]:
        """Get all platforms from existing diagram files.

        Scans the base directory for diagram.*.json files and extracts
        platform names from the filenames.

        Returns:
            List of platform names found in diagram files
        """
        platforms = []
        for file_path in self.base_path.glob(f"{DIAGRAM_FILE_PREFIX}*{DIAGRAM_FILE_SUFFIX}"):
            if file_path.name.startswith(DIAGRAM_FILE_PREFIX) and file_path.name.endswith(DIAGRAM_FILE_SUFFIX):
                platform = file_path.name.replace(DIAGRAM_FILE_PREFIX, "").replace(DIAGRAM_FILE_SUFFIX, "")
                if platform != "default":
                    platforms.append(platform)
        return platforms

    # Diagram Generation
    def create_default_diagram(self, platform: str) -> Dict[str, Any]:
        """Create default diagram with platform-specific pin handling."""
        # Special case for esp32p4
        if platform == 'esp32p4':
            rx_pin = '38'
            tx_pin = '37'
        else:
            rx_pin = 'RX'
            tx_pin = 'TX'

        diagram = self.default_diagram_config.copy()
        diagram['connections'] = [
            [f'esp:{tx_pin}', '$serialMonitor:RX', '', []],
            [f'esp:{rx_pin}', '$serialMonitor:TX', '', []]
        ]

        board_type = target_to_boards.get(platform)
        if not board_type:
            raise ValueError(
                f"Unknown or unsupported platform: '{platform}'. "
                f"Valid platforms are: {', '.join(target_to_boards.keys())}"
            )

        diagram['parts'] = [{
            "type": board_type,
            "id": "esp",
            "top": 0,
            "left": 0,
            "attrs": {}
        }]
        return diagram

    def platform_to_chipset(self, platform: str) -> str:
        """Convert platform name to ESP LaunchPad chipset format."""
        if platform == 'esp32':
            return 'ESP32'
        elif platform.startswith('esp32'):
            base = platform[5:]  # Remove 'esp32' prefix
            if len(base) == 2:  # e.g., 's3', 'c3', 'h2', 'p4'
                return f'ESP32-{base.upper()}'
        raise ValueError(f"Unknown platform '{platform}'. Cannot map to chipset name.")

    def generate_ci_from_diagram(self, platform: Optional[str] = None, override: bool = False) -> None:
        """Generate ci.yml from diagram files.

        Processes diagram files and extracts platform-specific configuration
        to generate or update the ci.yml file with upload-binary section.

        Args:
            platform: Optional specific platform to process. If None, all platforms are processed.
            override: Whether to overwrite the upload-binary section if it exists
        """
        platforms = [platform] if platform else self.get_platforms_from_diagrams()

        if not platforms:
            click.echo("No diagram files found to process")
            return

        # Load existing ci.yml if it exists
        ci_file = self.base_path / CI_CONFIG_FILE
        ci_data = {}
        if ci_file.exists():
            ci_data = load_yaml(ci_file)
            if ci_data.get("upload-binary") and not override:
                click.echo("ci.yml already has 'upload-binary' section. Use --override to overwrite.")
                return

        # Ensure upload-binary structure exists in ci_data
        if "upload-binary" not in ci_data:
            ci_data["upload-binary"] = {}

        upload_binary = ci_data["upload-binary"]
        upload_binary["targets"] = upload_binary.get("targets", [])
        upload_binary["diagram"] = upload_binary.get("diagram", {})

        # Process each platform
        for plat in platforms:
            self._process_diagram_file_to_ci(plat, upload_binary)

        # Ensure the modified upload_binary is saved back to ci_data
        ci_data["upload-binary"] = upload_binary
        save_yaml(ci_file, ci_data, True)

    def _process_diagram_file_to_ci(self, platform: str, upload_binary: Dict[str, Any]) -> None:
        """Process a single diagram file and update upload_binary configuration.

        Args:
            platform: Platform name to process
            upload_binary: Dictionary to update with processed configuration
        """
        # Add platform to targets if not already present
        if platform not in upload_binary["targets"]:
            upload_binary["targets"].append(platform)

        diagram_file = self.base_path / f"{DIAGRAM_FILE_PREFIX}{platform}{DIAGRAM_FILE_SUFFIX}"
        if not diagram_file.exists():
            click.echo(f"- {platform}: Warning: {diagram_file.name} not found, skipping")
            return

        diagram_data = load_json(diagram_file)

        # Build platform-specific diagram
        parts = self.filter_parts(diagram_data.get("parts", []))
        connections = self.filter_connections(diagram_data.get("connections", []))
        dependencies = diagram_data.get("dependencies")

        # Skip platforms with no meaningful content
        if not parts and not connections and not dependencies:
            click.echo(f"- {platform}: Skipping: no parts, connections, or dependencies")
            return

        platform_diagram = {
            "parts": parts,
            "connections": connections
        }

        # Add dependencies if they exist
        if dependencies:
            platform_diagram["dependencies"] = dependencies

        # Update platform data
        upload_binary["diagram"][platform] = platform_diagram

        click.echo(
            f"- {platform}: Processed with {len(platform_diagram['parts'])} parts and "
            f"{len(platform_diagram['connections'])} connections"
        )

    def generate_diagram_from_ci(self, platform: Optional[str] = None, override: bool = False) -> None:
        """Generate diagram files from ci.yml.

        Reads platform-specific diagram configuration from ci.yml and generates
        diagram.*.json files by merging them with default diagram configurations.

        Args:
            platform: Optional specific platform to generate. If None, generates for all platforms in ci.yml
            override: Whether to overwrite existing diagram files
        """
        platforms = [platform] if platform else self.get_platforms_from_ci()

        if not platforms:
            click.echo("No platforms found in ci.yml")
            return

        # Load ci.yml
        ci_file = self.base_path / CI_CONFIG_FILE
        if not ci_file.exists():
            click.echo(f"Error: {CI_CONFIG_FILE} not found", err=True)
            return

        ci_data = load_yaml(ci_file)

        # Process each platform
        for plat in platforms:
            self.generate_diagram(plat, override, ci_data.get("upload-binary", {}))

    def generate_diagram(self, platform: str, override: bool = False, config_data: Optional[Dict[str, Any]] = None) -> None:
        """Generate a diagram file for the specified platform.

        Args:
            platform: Target platform name
            override: Whether to overwrite existing diagram files
            config_data: Configuration data containing platform-specific diagram settings
        """
        if config_data is None:
            config_data = {}

        diagram_file = self.base_path / f"diagram.{platform}.json"

        # Check if file exists and we're not overriding
        if diagram_file.exists() and not override:
            click.echo(f"Warning: diagram.{platform}.json already exists. Use --override to overwrite.")
            return

        platform_diagram = config_data.get("diagram", {}).get(platform, {})

        # Start with default diagram for this platform
        diagram_data = self.create_default_diagram(platform)

        # Add platform-specific parts
        if platform_parts := platform_diagram.get("parts"):
            diagram_data["parts"].extend(platform_parts)

        # Add platform-specific connections
        if platform_connections := platform_diagram.get("connections"):
            existing_connections = diagram_data.get("connections", [])
            diagram_data["connections"] = existing_connections + platform_connections

        # Add dependencies if they exist
        if platform_dependencies := platform_diagram.get("dependencies"):
            diagram_data["dependencies"] = platform_dependencies

        save_json(diagram_file, diagram_data, True)

    def generate_launchpad_config(self, storage_url_prefix: str, repo_url_prefix: str, override: bool = False, output_dir: Optional[Path] = None) -> None:
        """Generate ESP LaunchPad config file from ci.yml targets.

        Creates a TOML configuration file for ESP LaunchPad with firmware images,
        supported chipsets, and project metadata extracted from ci.yml.

        Args:
            storage_url_prefix: Base URL prefix for firmware images
            repo_url_prefix: Base URL prefix for repository resources
            override: Whether to overwrite existing config files
            output_dir: Optional output directory. If None, uses base_path
        """
        project_name = self.base_path.name
        config_file = (output_dir / LAUNCHPAD_CONFIG_FILE) if output_dir else (self.base_path / LAUNCHPAD_CONFIG_FILE)

        if config_file.exists() and not override:
            click.echo(f"Warning: {config_file} already exists. Use --override to overwrite.")
            return

        # Load ci.yml to get platforms
        ci_file = self.base_path / CI_CONFIG_FILE
        if not ci_file.exists():
            click.echo("Error: ci.yml not found", err=True)
            return

        ci_data = load_yaml(ci_file)
        platforms = ci_data.get("upload-binary", {}).get("targets", [])

        if not platforms:
            click.echo("No platforms found in ci.yml")
            return

        # Convert platforms to chipsets
        chipsets = [self.platform_to_chipset(platform) for platform in platforms]

        # create firmware_images_url link from base_path (removing 'docs/' prefix if present)
        firmware_images_url = url_join(storage_url_prefix, self.base_path.as_posix().lstrip("docs/")) + "/"

        # Generate config data structure
        config_data = {
            'esp_toml_version': 1.0,
            'firmware_images_url': firmware_images_url,
            'supported_apps': [project_name],
            project_name: {
                'chipsets': chipsets,
                'image': {}
            }
        }

        # Add image configurations for each platform
        for platform in platforms:
            self._add_platform_image_config(config_data, project_name, platform)

        # Extract description from ci.yml if available
        description = ci_data.get("upload-binary", {}).get("description")
        if description:
            click.echo(f"- Found description in ci.yml: {description}")
            config_data[project_name]['description'] = description

        save_toml(config_file, config_data, override)

        click.echo(f"Generated ESP LaunchPad config: {config_file}")
        click.echo(f"Supported chipsets: {', '.join(chipsets)}")

    def _add_platform_image_config(self, config_data: Dict[str, Any], project_name: str, platform: str) -> None:
        """Add platform-specific image configuration to LaunchPad config.

        Args:
            config_data: Configuration dictionary to update
            project_name: Name of the project
            platform: Platform name
        """
        chipset = self.platform_to_chipset(platform)
        lowercase_chipset = chipset.lower()
        binary_name = url_join(platform, f"{project_name}.ino.merged.bin")
        config_data[project_name]['image'][lowercase_chipset] = binary_name

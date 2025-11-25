#!/usr/bin/env python3

import json
import yaml
import tempfile
import shutil
import unittest
from pathlib import Path

from esp_docs.esp_extensions.docs_embed.tool.wokwi_tool import DiagramSync, target_to_boards


class TestDiagramSyncInit(unittest.TestCase):
    """Test DiagramSync initialization."""

    def test_init_with_valid_directory(self):
        """Test initialization with valid directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sync = DiagramSync(tmpdir)
            self.assertEqual(sync.base_path, Path(tmpdir))
            self.assertIsInstance(sync.serial_connections, list)
            self.assertIsInstance(sync.default_diagram_config, dict)

    def test_init_with_nonexistent_path(self):
        """Test initialization with non-existent path raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            DiagramSync("/nonexistent/path/that/does/not/exist")

    def test_init_with_file_instead_of_directory(self):
        """Test initialization with file path raises NotADirectoryError."""
        with tempfile.NamedTemporaryFile() as tmpfile:
            with self.assertRaises(NotADirectoryError):
                DiagramSync(tmpfile.name)


class TestDiagramSyncDataProcessing(unittest.TestCase):
    """Test data processing methods."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sync = DiagramSync(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_is_serial_connection_true(self):
        """Test serial connection detection returns True."""
        serial_conn = ["esp:RX", "$serialMonitor:TX", "", []]
        self.assertTrue(self.sync.is_serial_connection(serial_conn))

    def test_is_serial_connection_false(self):
        """Test non-serial connection detection returns False."""
        normal_conn = ["led:VCC", "esp:GPIO2", "red", []]
        self.assertFalse(self.sync.is_serial_connection(normal_conn))

    def test_filter_parts(self):
        """Test filtering board parts from parts list."""
        parts = [
            {"type": "board-esp32-devkit-c-v4", "id": "esp"},
            {"type": "wokwi-led", "id": "led1"},
            {"type": "board-esp32-s3-devkitc-1", "id": "esp2"},
            {"type": "wokwi-resistor", "id": "r1"}
        ]

        filtered = self.sync.filter_parts(parts)
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]["type"], "wokwi-led")
        self.assertEqual(filtered[1]["type"], "wokwi-resistor")

    def test_filter_connections(self):
        """Test filtering serial connections from connections list."""
        connections = [
            ["esp:RX", "$serialMonitor:TX", "", []],
            ["led:VCC", "esp:GPIO2", "red", []],
            ["esp:TX", "$serialMonitor:RX", "", []],
            ["r1:1", "led:A", "", []]
        ]

        filtered = self.sync.filter_connections(connections)
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0][0], "led:VCC")
        self.assertEqual(filtered[1][0], "r1:1")

    def test_platform_to_chipset_esp32(self):
        """Test platform to chipset conversion for ESP32."""
        self.assertEqual(self.sync.platform_to_chipset("esp32"), "ESP32")

    def test_platform_to_chipset_esp32s3(self):
        """Test platform to chipset conversion for ESP32-S3."""
        self.assertEqual(self.sync.platform_to_chipset("esp32s3"), "ESP32-S3")

    def test_platform_to_chipset_esp32c3(self):
        """Test platform to chipset conversion for ESP32-C3."""
        self.assertEqual(self.sync.platform_to_chipset("esp32c3"), "ESP32-C3")

    def test_platform_to_chipset_invalid(self):
        """Test platform to chipset conversion with invalid platform."""
        with self.assertRaises(ValueError):
            self.sync.platform_to_chipset("invalid")


class TestDiagramSyncPlatformDiscovery(unittest.TestCase):
    """Test platform discovery methods."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sync = DiagramSync(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_get_platforms_from_ci_with_file(self):
        """Test getting platforms from existing ci.yml."""
        ci_file = Path(self.tmpdir) / "ci.yml"
        ci_data = {
            "upload-binary": {
                "targets": ["esp32", "esp32s2", "esp32s3"]
            }
        }
        with open(ci_file, 'w') as f:
            yaml.safe_dump(ci_data, f)

        platforms = self.sync.get_platforms_from_ci()
        self.assertEqual(platforms, ["esp32", "esp32s2", "esp32s3"])

    def test_get_platforms_from_ci_without_file(self):
        """Test getting platforms when ci.yml doesn't exist."""
        platforms = self.sync.get_platforms_from_ci()
        self.assertEqual(platforms, [])

    def test_get_platforms_from_diagrams(self):
        """Test getting platforms from diagram files."""
        # Create diagram files
        for platform in ["esp32", "esp32s3", "esp32c3"]:
            diagram_file = Path(self.tmpdir) / f"diagram.{platform}.json"
            with open(diagram_file, 'w') as f:
                json.dump({"version": 1}, f)

        platforms = self.sync.get_platforms_from_diagrams()
        self.assertIn("esp32", platforms)
        self.assertIn("esp32s3", platforms)
        self.assertIn("esp32c3", platforms)


class TestDiagramSyncDiagramGeneration(unittest.TestCase):
    """Test diagram generation methods."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sync = DiagramSync(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_create_default_diagram_esp32(self):
        """Test creating default diagram for ESP32."""
        diagram = self.sync.create_default_diagram("esp32")

        self.assertEqual(diagram["version"], 1)
        self.assertEqual(diagram["author"], "Espressif Systems")
        self.assertEqual(len(diagram["parts"]), 1)
        self.assertEqual(diagram["parts"][0]["type"], "board-esp32-devkit-c-v4")
        self.assertEqual(len(diagram["connections"]), 2)
        # Check RX/TX pins
        self.assertIn("esp:TX", diagram["connections"][0][0])
        self.assertIn("esp:RX", diagram["connections"][1][0])

    def test_create_default_diagram_esp32p4(self):
        """Test creating default diagram for ESP32-P4 with special pins."""
        diagram = self.sync.create_default_diagram("esp32p4")

        self.assertEqual(diagram["parts"][0]["type"], "board-esp32-p4-function-ev")
        # Check special pins for P4
        self.assertIn("esp:37", diagram["connections"][0][0])
        self.assertIn("esp:38", diagram["connections"][1][0])

    def test_create_default_diagram_invalid_platform(self):
        """Test creating diagram for invalid platform."""
        with self.assertRaises(ValueError):
            self.sync.create_default_diagram("invalid_platform")

    def test_generate_diagram(self):
        """Test generating diagram file."""
        self.sync.generate_diagram("esp32", override=True)

        diagram_file = Path(self.tmpdir) / "diagram.esp32.json"
        self.assertTrue(diagram_file.exists())

        with open(diagram_file, 'r') as f:
            diagram_data = json.load(f)

        self.assertEqual(diagram_data["version"], 1)
        self.assertEqual(diagram_data["parts"][0]["type"], "board-esp32-devkit-c-v4")

    def test_generate_ci_from_diagram(self):
        """Test generating ci.yml from diagram files."""
        # Create diagram files
        for platform in ["esp32", "esp32s3"]:
            diagram_file = Path(self.tmpdir) / f"diagram.{platform}.json"
            diagram_data = {
                "version": 1,
                "parts": [
                    {"type": "board-" + platform, "id": "esp"},
                    {"type": "wokwi-led", "id": "led1"}
                ],
                "connections": [
                    ["esp:RX", "$serialMonitor:TX", "", []],
                    ["esp:TX", "$serialMonitor:RX", "", []],
                    ["led1:VCC", "esp:GPIO2", "red", []]
                ]
            }
            with open(diagram_file, 'w') as f:
                json.dump(diagram_data, f)

        # Generate CI
        self.sync.generate_ci_from_diagram(override=True)

        # Check ci.yml was created
        ci_file = Path(self.tmpdir) / "ci.yml"
        self.assertTrue(ci_file.exists())

        with open(ci_file, 'r') as f:
            ci_data = yaml.safe_load(f)

        self.assertIn("upload-binary", ci_data)
        self.assertIn("targets", ci_data["upload-binary"])
        self.assertIn("diagram", ci_data["upload-binary"])
        self.assertIn("esp32", ci_data["upload-binary"]["targets"])
        self.assertIn("esp32s3", ci_data["upload-binary"]["targets"])

    def test_generate_diagram_from_ci(self):
        """Test generating diagram files from ci.yml."""
        # Create ci.yml
        ci_file = Path(self.tmpdir) / "ci.yml"
        ci_data = {
            "upload-binary": {
                "targets": ["esp32", "esp32s2"],
                "diagram": {
                    "esp32": {
                        "parts": [{"type": "wokwi-led", "id": "led1"}],
                        "connections": [["led1:VCC", "esp:GPIO2", "red", []]]
                    },
                    "esp32s2": {
                        "parts": [{"type": "wokwi-resistor", "id": "r1"}],
                        "connections": [["r1:1", "esp:GPIO3", "", []]]
                    }
                }
            }
        }
        with open(ci_file, 'w') as f:
            yaml.safe_dump(ci_data, f)

        # Generate diagrams
        self.sync.generate_diagram_from_ci(override=True)

        # Check diagram files were created
        esp32_diagram = Path(self.tmpdir) / "diagram.esp32.json"
        esp32s2_diagram = Path(self.tmpdir) / "diagram.esp32s2.json"

        self.assertTrue(esp32_diagram.exists())
        self.assertTrue(esp32s2_diagram.exists())

        with open(esp32_diagram, 'r') as f:
            diagram_data = json.load(f)

        # Check it has both default and custom parts
        self.assertTrue(any(p["type"].startswith("board-") for p in diagram_data["parts"]))
        self.assertTrue(any(p["type"] == "wokwi-led" for p in diagram_data["parts"]))


class TestDiagramSyncConfigGeneration(unittest.TestCase):
    """Test LaunchPad config generation."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sync = DiagramSync(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_generate_launchpad_config(self):
        """Test generating LaunchPad config file."""
        # Create ci.yml
        ci_file = Path(self.tmpdir) / "ci.yml"
        ci_data = {
            "upload-binary": {
                "targets": ["esp32", "esp32s3"],
                "description": "Test project description"
            }
        }
        with open(ci_file, 'w') as f:
            yaml.safe_dump(ci_data, f)

        storage_url = "https://storage.example.com/binaries"
        repo_url = "https://github.com/user/repo/tree/main"

        # Generate config
        self.sync.generate_launchpad_config(storage_url, repo_url, override=True)

        # Check launchpad.toml was created
        config_file = Path(self.tmpdir) / "launchpad.toml"
        self.assertTrue(config_file.exists())

        with open(config_file, 'r') as f:
            content = f.read()

        # Check content
        self.assertIn("esp_toml_version = 1.0", content)
        self.assertIn(f'firmware_images_url = "', content)
        self.assertIn(storage_url, content)
        self.assertIn('esp32 = ', content)
        self.assertIn('esp32-s3 = ', content)

    def test_generate_launchpad_config_without_readme(self):
        """Test generating LaunchPad config without README.md."""
        # Create ci.yml
        ci_file = Path(self.tmpdir) / "ci.yml"
        ci_data = {
            "upload-binary": {
                "targets": ["esp32"]
            }
        }
        with open(ci_file, 'w') as f:
            yaml.safe_dump(ci_data, f)

        storage_url = "https://storage.example.com/binaries"
        repo_url = "https://github.com/user/repo/tree/main"

        # Generate config
        self.sync.generate_launchpad_config(storage_url, repo_url, override=True)

        # Check launchpad.toml was created
        config_file = Path(self.tmpdir) / "launchpad.toml"
        self.assertTrue(config_file.exists())

        with open(config_file, 'r') as f:
            content = f.read()

        # Should not have readme URL
        self.assertNotIn('config_readme_url', content)


class TestTargetToBoards(unittest.TestCase):
    """Test target_to_boards mapping."""

    def test_all_platforms_supported(self):
        """Test that all expected platforms are in target_to_boards."""
        expected_platforms = ['esp32', 'esp32c3', 'esp32c6', 'esp32h2', 'esp32p4', 'esp32s2', 'esp32s3']
        for platform in expected_platforms:
            self.assertIn(platform, target_to_boards)
            self.assertTrue(target_to_boards[platform].startswith('board-'))


if __name__ == '__main__':
    unittest.main()


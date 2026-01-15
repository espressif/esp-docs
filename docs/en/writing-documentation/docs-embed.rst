Wokwi Simulator Integration
============================

This page describes how to embed interactive Wokwi simulators into your documentation using the esp-docs Sphinx extension. The Wokwi integration allows you to include interactive circuit simulations directly in your documentation, enabling readers to experiment with ESP32-based projects without physical hardware.

Overview
--------

The Wokwi embed extension provides two main features:

1. **Interactive Simulator Embedding**: Embed Wokwi circuit simulators directly in your documentation pages
2. **Arduino Example Integration**: Automatically discover and embed multiple target variants of Arduino examples with tabbed interfaces

The extension includes both a Sphinx plugin for embedding simulators in documentation and a CLI tool for managing diagram files and CI configuration.

Sphinx Plugin Setup
-------------------

To use the Wokwi embed extension in your documentation, you need to enable it in your Sphinx configuration.

Enabling the Extension
^^^^^^^^^^^^^^^^^^^^^^

Add the extension to your ``extensions`` list in ``conf.py`` or ``conf_common.py``:

.. code-block:: python

    extensions += [
        'esp_docs.esp_extensions.docs_embed',
    ]

Configuration Options
^^^^^^^^^^^^^^^^^^^^^

The extension can be configured via environment variables or in your ``conf.py`` file. Environment variables take precedence over ``conf.py`` settings. Environment variable names are the uppercase version of the config key (e.g., ``docs_embed_wokwi_viewer_url`` becomes ``DOCS_EMBED_WOKWI_VIEWER_URL``).

Available Configuration Options:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Config Key
     - Default
     - Description
   * - ``docs_embed_wokwi_viewer_url``
     - ``https://wokwi.com/experimental/viewer``
     - Base URL for the Wokwi viewer iframe
   * - ``docs_embed_default_width``
     - ``100%``
     - Default width for embedded simulators
   * - ``docs_embed_default_height``
     - ``500px``
     - Default height for embedded simulators
   * - ``docs_embed_default_allowfullscreen``
     - ``True``
     - Enable fullscreen mode by default
   * - ``docs_embed_default_loading``
     - ``lazy``
     - Default iframe loading strategy (lazy, eager, or auto)
   * - ``docs_embed_esp_launchpad_url``
     - ``https://espressif.github.io/esp-launchpad``
     - Base URL for ESP LaunchPad integration
   * - ``docs_embed_about_wokwi_url``
     - ``https://docs.wokwi.com``
     - URL for Wokwi documentation/about page
   * - ``docs_embed_skip_validation``
     - ``False``
     - Skip file existence validation (useful for CI builds)
   * - ``docs_embed_github_base_url``
     - ``None`` (required for wokwi-example)
     - Base URL for GitHub repository (for source code links)
   * - ``docs_embed_github_branch``
     - ``None`` (required for wokwi-example)
     - GitHub branch name (for source code links)
   * - ``docs_embed_public_root``
     - ``None`` (required for wokwi-example)
     - Public URL root where documentation is hosted
   * - ``docs_embed_binaries_dir``
     - ``None`` (required for wokwi-example)
     - Directory path where firmware binaries are stored (relative to source)

Example Configuration
^^^^^^^^^^^^^^^^^^^^^

Here's an example configuration in ``conf.py``:

.. code-block:: python

    # Wokwi embed configuration
    docs_embed_public_root = "https://docs.espressif.com"
    docs_embed_binaries_dir = "_static"
    docs_embed_github_base_url = "https://github.com/espressif/arduino-esp32"
    docs_embed_github_branch = "master"
    docs_embed_skip_validation = False

Or using environment variables:

.. code-block:: bash

    export DOCS_EMBED_PUBLIC_ROOT="https://docs.espressif.com"
    export DOCS_EMBED_BINARIES_DIR="_static"
    export DOCS_EMBED_GITHUB_BASE_URL="https://github.com/espressif/arduino-esp32"
    export DOCS_EMBED_GITHUB_BRANCH="master"

Basic Wokwi Embed Directive
----------------------------

The ``.. wokwi::`` directive allows you to embed a single Wokwi simulator with explicit diagram and firmware URLs.

Syntax
^^^^^^

.. code-block:: rst

    .. wokwi:: [name]
       :diagram: <URL to Wokwi diagram JSON>
       :firmware: <URL to firmware binary>
       :width: <CSS width value>
       :height: <CSS height value>
       :loading: <lazy|eager|auto>
       :allowfullscreen:
       :title: <iframe title>
       :class: <CSS class names>

Options
^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Option
     - Description
   * - ``name`` (optional argument)
     - Name/label for the diagram (used in tabs if multiple diagrams are grouped)
   * - ``:diagram:`` (required)
     - URL to Wokwi diagram JSON file
   * - ``:firmware:`` (required)
     - URL to compiled firmware binary (UF2 or BIN format)
   * - ``:width:`` (optional)
     - CSS width value (default: ``100%``)
   * - ``:height:`` (optional)
     - CSS height value (default: ``500px``)
   * - ``:loading:`` (optional)
     - iframe loading strategy: ``lazy``, ``eager``, or ``auto`` (default: ``lazy``)
   * - ``:title:`` (optional)
     - Title text for the iframe (default: ``Wokwi simulation``)
   * - ``:allowfullscreen:`` (optional flag)
     - Enable fullscreen mode for the simulator
   * - ``:tab:`` (optional)
     - Tab label (alternative to name argument)
   * - ``:class:`` (optional)
     - Additional CSS class names to apply

Examples
^^^^^^^^

Basic embed with default settings:

.. code-block:: rst

    .. wokwi::
       :diagram: https://example.com/diagram.json
       :firmware: https://example.com/firmware.bin

Custom size and fullscreen:

.. code-block:: rst

    .. wokwi::
       :diagram: https://example.com/diagram.json
       :firmware: https://example.com/firmware.bin
       :width: 800px
       :height: 600px
       :allowfullscreen:

With custom title and loading strategy:

.. code-block:: rst

    .. wokwi:: ESP32 Blink Example
       :diagram: https://example.com/blink-diagram.json
       :firmware: https://example.com/blink-firmware.bin
       :title: ESP32 LED Blink Simulation
       :loading: eager

Arduino Example Embed Directive
--------------------------------

The ``.. wokwi-example::`` directive automatically discovers and embeds Arduino examples with support for multiple ESP32 targets. It reads the ``ci.yml`` configuration file to determine which targets are available and creates a tabbed interface for each target.

Syntax
^^^^^^

.. code-block:: rst

    .. wokwi-example:: <path-to-example-directory>
       :width: <CSS width value>
       :height: <CSS height value>
       :allowfullscreen:
       :loading: <lazy|eager|auto>
       :class: <CSS class names>

The directive takes a single required argument: the path to the example directory relative to the source root.

Options
^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Option
     - Description
   * - ``:width:`` (optional)
     - CSS width value (default: ``100%``)
   * - ``:height:`` (optional)
     - CSS height value (default: ``500px``)
   * - ``:allowfullscreen:`` (optional flag)
     - Enable fullscreen mode
   * - ``:loading:`` (optional)
     - iframe loading strategy
   * - ``:class:`` (optional)
     - Additional CSS class names

Expected Directory Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The directive expects the following directory structure:

**Arduino Source Directory:**
::

    libraries/ESP32/examples/GPIO/Blink/
    ├── Blink.ino
    └── ci.yml

**Built Artifacts (in _static/):**
::

    _static/libraries/ESP32/examples/GPIO/Blink/
    ├── ci.yml (copied by build process)
    ├── launchpad.toml (optional, for ESP LaunchPad integration)
    ├── esp32/
    │   ├── Blink.ino.merged.bin
    │   └── diagram.esp32.json
    └── esp32s2/
        ├── Blink.ino.merged.bin
        └── diagram.esp32s2.json

The ``ci.yml`` file should contain an ``upload-binary`` section with a ``targets`` list:

.. code-block:: yaml

    upload-binary:
      targets:
        - esp32
        - esp32s2
      diagram:
        esp32:
          parts: [...]
          connections: [...]
        esp32s2:
          parts: [...]
          connections: [...]

Features
^^^^^^^^

The ``wokwi-example`` directive provides several automatic features:

- **Auto-discovery**: Reads ``ci.yml`` to discover supported targets (ESP32, ESP32-S2, ESP32-S3, etc.)
- **Tabbed Interface**: Creates tabs for each target's simulation
- **Source Code Tab**: Automatically includes a tab showing the ``.ino`` file content with syntax highlighting
- **ESP LaunchPad Integration**: If ``launchpad.toml`` exists, adds a link to flash the example via ESP LaunchPad
- **GitHub Source Link**: If configured, adds a link to the source code on GitHub
- **File Validation**: Validates that required files exist (can be disabled with ``docs_embed_skip_validation``)

Example
^^^^^^^

.. code-block:: rst

    .. wokwi-example:: libraries/ESP32/examples/GPIO/Blink
       :width: 100%
       :height: 600px
       :allowfullscreen:

This will create a tabbed interface with:
- A "Blink.ino" tab showing the source code
- An "ESP32" tab with the ESP32 simulation
- An "ESP32-S2" tab with the ESP32-S2 simulation (if configured in ci.yml)

CLI Tool - docs-embed
---------------------

The ``docs-embed`` CLI tool helps manage Wokwi diagram files, CI configuration, and ESP LaunchPad configuration for your Arduino examples.

Installation
^^^^^^^^^^^^

The tool is installed as part of the esp-docs package. You can use it directly:

.. code-block:: bash

    docs-embed --help

All commands support a ``--path`` option to specify the directory to operate on (defaults to current directory).

init-diagram Command
^^^^^^^^^^^^^^^^^^^^

Initialize a new project with Wokwi diagrams and CI configuration for specified platforms.

**Syntax:**
::

    docs-embed init-diagram --platforms <platform1,platform2,...> [--override]

**Options:**
- ``--platforms`` (required): Comma-separated list of platforms to initialize.
- ``--override``: Override existing diagram files if they already exist

**Example:**

.. code-block:: bash

    docs-embed init-diagram --platforms esp32,esp32s2
    docs-embed --path folder/examples init-diagram --platforms esp32,esp32s2 --override

This command creates default ``diagram.<platform>.json`` files for each specified platform with basic board configurations and serial monitor connections.

ci-from-diagram Command
^^^^^^^^^^^^^^^^^^^^^^^

Generate or update ``ci.yml`` from existing diagram files. This command reads ``diagram.*.json`` files and extracts their configuration to populate the ``upload-binary`` section in ``ci.yml``.

**Syntax:**
::

    docs-embed ci-from-diagram [--platform <platform>] [--override]

**Options:**
- ``--platform`` (optional): Specific platform to process (e.g., ``esp32``, ``esp32s2``). If not specified, processes all diagrams found
- ``--override``: Override existing ``upload-binary`` section in ``ci.yml``

**Example:**

.. code-block:: bash

    docs-embed ci-from-diagram
    docs-embed --path folder/examples ci-from-diagram --platform esp32 --override

This command:
- Scans for ``diagram.*.json`` files
- Extracts parts, connections, and dependencies from each diagram
- Updates ``ci.yml`` with the extracted configuration
- Adds platforms to the ``targets`` list if not already present

diagram-from-ci Command
^^^^^^^^^^^^^^^^^^^^^^^^

Generate diagram files from ``ci.yml`` configuration. This is the reverse operation of ``ci-from-diagram`` - it reads platform-specific diagram configurations from ``ci.yml`` and generates ``diagram.*.json`` files.

**Syntax:**
::

    docs-embed diagram-from-ci [--platform <platform>] [--override]

**Options:**
- ``--platform`` (optional): Specific platform to generate. If not specified, generates for all platforms in ``ci.yml``
- ``--override``: Override existing diagram files

**Example:**

.. code-block:: bash

    docs-embed diagram-from-ci
    docs-embed --path folder/examples diagram-from-ci --platform esp32 --override

This command:
- Reads ``ci.yml`` to get the list of targets
- For each target, merges the diagram configuration from ``ci.yml`` with default board configuration
- Generates ``diagram.<platform>.json`` files

launchpad-config Command
^^^^^^^^^^^^^^^^^^^^^^^^

Generate ESP LaunchPad configuration file (``launchpad.toml``) from ``ci.yml``. This creates a TOML configuration file that ESP LaunchPad can use to flash firmware to physical hardware.

**Syntax:**
::

    docs-embed launchpad-config --storage-url-prefix <URL> --repo-url-prefix <URL> [--override]

**Options:**
- ``--storage-url-prefix`` (required): Base URL prefix where firmware binaries are hosted. Can also be set via ``STORAGE_URL_PREFIX`` environment variable
- ``--repo-url-prefix`` (required): Base URL prefix for the repository resources. Can also be set via ``REPO_URL_PREFIX`` environment variable
- ``--override``: Override existing ``launchpad.toml`` file

**Example:**

.. code-block:: bash

    docs-embed launchpad-config \
        --storage-url-prefix https://storage.example.com \
        --repo-url-prefix https://github.com/user/repo

    # Using environment variables
    export STORAGE_URL_PREFIX="https://storage.example.com"
    export REPO_URL_PREFIX="https://github.com/user/repo"
    docs-embed launchpad-config

This command:
- Reads ``ci.yml`` to extract firmware information for each target
- Generates ``launchpad.toml`` with firmware images, supported chipsets, and project metadata
- Creates URLs for firmware binaries using the provided storage URL prefix

Workflow Examples
-----------------

Complete Workflow
^^^^^^^^^^^^^^^^^

Here's a complete workflow for adding Wokwi simulation to an Arduino example:

1. **Initialize diagrams for your platforms:**
   ::

       cd libraries/ESP32/examples/GPIO/Blink
       docs-embed init-diagram --platforms esp32,esp32s2

2. **Customize the diagram files** (optional):
   Edit ``diagram.esp32.json`` and ``diagram.esp32s2.json`` to add components, connections, etc.

3. **Generate CI configuration from diagrams:**
   ::

       docs-embed ci-from-diagram

4. **Embed in documentation:**
   ::

       .. wokwi-example:: libraries/ESP32/examples/GPIO/Blink

5. **Generate Documentation:**
Before generating the documentation, make sure you have configured settings in your ``conf.py`` file.


Synchronizing Diagrams and CI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you modify diagram files and want to update ``ci.yml``:

::

    docs-embed ci-from-diagram --override

If you modify ``ci.yml`` and want to regenerate diagram files:

::

    docs-embed diagram-from-ci --override

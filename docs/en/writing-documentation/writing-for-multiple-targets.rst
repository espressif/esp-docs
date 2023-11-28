Writing for Multiple Targets
============================

Espressif provides a rich list of chip products, e.g., ESP32, ESP32-S2, ESP32-C3, which are referred to as "targets" in ``ESP-Docs``. Technical documentation differs for each specific chip, yet a large part of the content is reusable among different targets.

To facilitate the writing of documents that can be reused for multiple different chips, several functionalities are provided in ``ESP-Docs`` for writers to deal with target-specific inline text, paragraph, bullet point, and even document while building the documentation for all Espressif's chips from the same files.

.. _target-specific-inline-text:

Target-Specific Inline Text
---------------------------

When the content is reusable for all ESP chips, but you need to refer to the specific chip name, toolchain name, path, hardware/software specification, or other inline text that varies among different targets in the paragraph, consider using the substitution macros supplied by the extension :project_file:`Format ESP Target <src/esp_docs/esp_extensions/format_esp_target.py>`. Substitution macros allow you to generate target-specific inline text from the same source file with the target passed to the Sphinx command line.

For example, in the following reStructuredText content, the substitution macros (referred to as tag hereinafter)  ``IDF_TARGET_NAME``, ``IDF_TARGET_PATH_NAME``, ``IDF_TARGET_TOOLCHAIN_PREFIX``, and ``IDF_TARGET_TOOLCHAIN_PREFIX`` defined in ``esp_extensions/format_esp_target.py`` are used::

    This is {IDF_TARGET_NAME} with /{IDF_TARGET_PATH_NAME}/soc.c, compiled with `{IDF_TARGET_TOOLCHAIN_PREFIX}-gcc` with `CONFIG_{IDF_TARGET_TOOLCHAIN_PREFIX}_MULTI_DOC`.

The text will be rendered for ESP32-S2 chip as the following::

    This is ESP32-S2 with /esp32s2/soc.c, compiled with `xtensa-esp32s2-elf-gcc` with `CONFIG_ESP32S2_MULTI_DOC`.

This extension also supports markup for defining local substitutions within a single source file. Place a definition like the following in a single line to define a target-dependent substitution of the tag ``IDF_TARGET_SUFFIX`` in the current reStructuredText file::

    {IDF_TARGET_SUFFIX:default="DEFAULT_VALUE", esp32="ESP32_VALUE", esp32s2="ESP32S2_VALUE", esp32c3="ESP32C3_VALUE"}

For example::

    {IDF_TARGET_TX_PIN:default="IO3", esp32="IO4", esp32s2="IO5", esp32c3="IO6"}

The above line will define a substitution for the tag ``IDF_TARGET_TX_PIN``, which would be replaced by the text "IO5" if Sphinx is called with the target esp32s2 and "IO3" if called with esp32s3. You may also use the text "Not updated" for the default value.

In the case when multiple targets have the same value (may not be the default value) to be substituted, you can even group such targets together to avoid re-writing the same values multiple times.

For example::
    {IDF_TARGET_SBV2_KEY:default="RSA-3072", esp32c6, esp32h2="RSA-3072 or ECDSA-256 or ECDSA-192"}

The above line will define a substitution for the tag ``IDF_TARGET_SBV2_KEY``, which would be replaced by the text "RSA-3072 or ECDSA-256 or ECDSA-192" if Sphinx is called with the target esp32c6 or esp32h2 and "RSA-3072" if called with any other target.

.. note::

    * These single-file definitions can be placed anywhere in the reStructuredText file on their own line, but the name of the directive must start with ``IDF_TARGET_``.
    * Also note that these replacements cannot be used inside markup that rely on alignment of characters, e.g., tables.

ESP-Docs also allows other extensions to add additional substitutions through Sphinx events. For example, in ESP-IDF it is possible to use defines from ``soc_caps.h``::

    The target has {IDF_TARGET_SOC_SPI_PERIPH_NUM} SPI peripherals.

The text will be rendered for ESP32-S2 as the following::

    The target has 3 SPI peripherals.

For a full overview of available substitutions in your project, you can take a look at ``IDF_TARGET-substitutions.txt``, which is generated in the build folder when a project is built.



Target-Specific Paragraph
--------------------------

In a document shared by multiple targets, occasionally there will be paragraphs only applicable to one or some of the targets, or the paragraphs should be customized for different targets. ``ESP-Docs`` introduces the ``.. only:: TAG`` directive provided by the `Sphinx selective exclude <https://github.com/pfalcon/sphinx_selective_exclude>`__ extension to help you define specific chip targets for target-specific content in the document.

To use the ``.. only:: TAG`` directive, simply follow the steps described below:

1. Define the target of the content and replace "TAG" with one of the following options:

* Chip names. For example:

    * esp32 > ``.. only:: esp32``
    * esp32s2 > ``.. only:: esp32s2``
    * esp32c3 > ``.. only:: esp32c3``

* Or other tags you define and configure based on your own needs. For example, there are two kinds of customized tags in `esp-idf <https://github.com/espressif/esp-idf>`__:

    * Tags defined in the ``sdkconfig.h`` header files, e.g., ``CONFIG_FREERTOS_UNICORE``, which are generated by the default menuconfig settings for the target.

    * Tags defined in the ``*_caps.h`` header files, e.g., ``SOC_BT_SUPPORTED`` and ``SOC_CAN_SUPPORTED``.

2. Place the directive before the content that you want to exclude from the rest of the document::

    .. only:: esp32

        ESP32-specific content.

.. note::

    Note that it is required to leave a blank line after the directive and to indent before the content.

In this way, Sphinx will only generate the content for the target that you have defined using the directive, e.g., ESP32 in the example above.

This directive also supports the boolean operators ``and``, ``or``, and ``not``. For example:

    * ``.. only:: not esp32c2``
    * ``.. only:: esp32 or esp32s2``
    * ``.. only:: SOC_BT_SUPPORTED and CONFIG_FREERTOS_UNICORE``

Note that the extension sometimes does not correctly handle the case where you exclude a section that is directly followed by a labeled new section. For example::

    .. only:: esp32

        .. _section_1_label:

        Section 1
        ^^^^^^^^^
        Section 1 content

    .. _section_2_label:

    Section 2
    ^^^^^^^^^
    Section 2 content

In the above case, if the label ``section_2_label`` does not correctly link to the section that follows, refer to the temporary workaround below when this cannot be avoided::

    .. only:: esp32

        .. _section_1_label:

        Section 1
        ^^^^^^^^^
        Section 1 content

        .. _section_2_label:

    .. only:: not esp32

        .. _section_2_label:

    Section 2
    ^^^^^^^^^
    Section 2 content

.. _target-specific-bullet-point:

Target-Specific Bullet Point
------------------------------

The ``:TAG:`` role provided by ``ESP-Docs`` comes in handy when you need to define targets for content inside a list of bullet points. To achieve this, simply add the ``:TAG:`` inside the ``.. list::`` directive before the items. For example::

    .. list::

        :esp32: - ESP32-specific content
        :esp32c2 or esp32c3: - Content specific to ESP32-C2 and ESP32-C3
        :SOC_BT_SUPPORTED: - Bluetooth-specific content
        - Common bullet point 1
        - Common bullet point 2

Then Sphinx will only generate the first bullet point for ESP32 documentation, the second bullet point for ESP32-C2 and ESP32-C3 documentations, and the third bullet point for targets that support Bluetooth after you define the ``SOC_BT_SUPPORTED`` tag.

.. _target-specific-doc:

Target-Specific Document
-------------------------

It is also possible to define targets for a whole document using the ``:TAG:`` role in a table of content tree. After you place the ``:TAG:`` role before the toctree item, Sphinx will use the role to include or exclude content based on the target it was called with.

For example, in the following toctree extracted from the index of `api-guides <https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/index.rst>`__ for `esp-idf <https://github.com/espressif/esp-idf>`__, the tags ``SOC_BT_SUPPORTED``, ``SOC_RTC_MEM_SUPPORTED``, and ``SOC_USB_OTG_SUPPORTED`` (defined in the ``\*_caps`` header files) are used::

    .. toctree::
        :maxdepth: 1

        app_trace
        startup
        :SOC_BT_SUPPORTED: blufi
        bootloader
        build-system
        core_dump
        :SOC_RTC_MEM_SUPPORTED: deep-sleep-stub
        error-handling
        :esp32s3: flash_psram_config
        :not esp32c6: RF_calibration

In this way, Sphinx will only link to the documents ``blufi.rst`` and ``deep-sleep-stub.rst`` for targets that support these functions, the document ``flash_psram_config.rst`` for ESP32-S3, and the document ``RF_calibration.rst`` for all the targets except for ESP32-C6.

Note that if you need to exclude an entire document from the toctree based on targets, it is necessary to also update the configuration in ``docs/conf_common.py`` to exclude the file for other targets, or a Sphinx warning "WARNING: document isn't included in any toctree" will be generated.

The recommended way of doing it is adding a ``conditional_include_dict`` list in ``docs/conf_common.py`` and include the document to one of the list that gets included. Examples can be found in `docs/conf_common.py <https://github.com/espressif/esp-idf/blob/master/docs/conf_common.py>`__ in `esp-idf <https://github.com/espressif/esp-idf>`__, where, for instance, a document which should only be shown for Bluetooth-capable targets should be added to ``BT_DOCS``. The ``exclude_docs.py`` will then take care of adding it to ``conditional_include_dict`` if the corresponding tag is not set.

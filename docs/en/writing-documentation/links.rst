Links
=====

This document introduces how to link to different elements of documentation when you write documents with ESP-Docs.

Table of Contents
-----------------

- `Linking to Language Versions`_
- `Linking to Other Sections Within the Document`_
- `Linking to Other Documents`_
- `Linking to a Specific Place of Other Documents in a Same Project`_
- `Linking to Kconfig References`_
- `Linking to Classes, Functions, Enumerations, etc`_
- `Linking to GitHub Files`_
- `Linking to External Pages`_
- `Linking to ESP TRMs and Datasheets`_

  - `Linking to a Whole TRM or Datasheet File`_
  - `Linking to Chapters of a TRM or Datasheet File`_

- `Resources`_

When writing documentation, you often need to link to other language versions of the document, other sections within the document, other documents, GitHub files, etc. An easy way is just to use the raw URL that Sphinx generates for each page or section. This works, but it has some disadvantages:

- Links can change, so they are hard to maintain.
- Links can be verbose and hard to read, so it is unclear what page or section they are linking to.
- There is no easy way to link to specific sections like paragraphs, figures, or code blocks.
- URL links only work for the HTML version of your documentation.

Instead, Sphinx offers a powerful way to link to different elements of the document, called cross-references. Some advantages of using them:

- Use a human-readable name of your choice, instead of a URL.
- Portable between formats: HTML, PDF, ePub.
- Sphinx will warn you of invalid references.
- You can cross-reference more than just pages and section headers.

Linking to Language Versions
----------------------------

Switching between documentation in different languages may be done using the ``:link_to_translation:`` custom role. The role placed on a page of documentation provides a link to the same page in a language specified as a parameter. Examples below show how to enter links to Chinese and English versions of documentation.

Syntax and examples:

.. code-block:: text

    :link_to_translation:`zh_CN:中文版`
    :link_to_translation:`en:English`

The language is specified using standard abbreviations like ``en`` or ``zh_CN``. The text after last semicolon is not standardized and may be entered depending on the context where the link is placed, e.g.:

.. code-block:: text

    :link_to_translation:`en:see description in English`

Linking to Other Sections Within the Document
---------------------------------------------

Syntax and example:

.. code-block:: text

    `Linking to ESP TRMs and Datasheets`_

Rendering result:

`Linking to ESP TRMs and Datasheets`_

Linking to Other Documents
--------------------------

If you want to link to other documents in the same folder, which is the ``docs`` folder here, you can either use the path relative to the root folder or relative to the document you want to link to. In addition, you can also display the document title as the link text or customize the link text. Please note that we recommend using the path relative to the root folder as links will not break when you move the document containing the links.

- You can use the following syntax to display the document title as the link text.

  Syntax:

  .. code-block:: text

      :doc:`relative path to the root folder`
      :doc:`relative path to the document you want to link to`

  Example:

  .. code-block:: text

      :doc:`/introduction/index`
      :doc:`../introduction/index`

  Rendering result:

  :doc:`/introduction/index`

  :doc:`../introduction/index`

- If you want to customize the link text, you can use the following syntax.

  Syntax:

  .. code-block:: text

      :doc:`CustomizedLinkText <path from the documentation root, starting with />`
      :doc:`CustomizedLinkText <relative path to the document you want to link to>`

  Example:

  .. code-block:: text

      :doc:`Another Introduction </introduction/index>` (the documentation root here is esp-docs/docs/en)
      :doc:`Another Introduction <../introduction/index>`

  Rendering result:

  :doc:`Another Introduction </introduction/index>`

  :doc:`Another Introduction <../introduction/index>`

Linking to a Specific Place of Other Documents in a Same Project
----------------------------------------------------------------

To link to a specific place of documents in a same project, you need to first add an anchor in the specific place and then refer it in the document.

- Add an anchor to the specific place where you want to link to with the following syntax.

  Syntax:

  .. code-block:: text

      .. _AnchorName:

  Example:

  .. code-block:: text

      .. _building-documentation-1

- Insert the anchor in your document with the following syntaxes. You can either display the section name after the anchor as the link text or customize the link text.

  * Display the section name after the anchor as the link text

    Syntax:

    .. code-block:: text

        :ref:`AnchorName`

    Example:

    .. code-block:: text

        :ref:`building-documentation-1`

    Rendering result:

    :ref:`building-documentation-1`

  * Customize the link text

    Syntax:

    .. code-block:: text

        :ref:`CustomizedLinkText <AnchorName>`

    Example:

    .. code-block:: text

        :ref:`Building Document <building-documentation-1>`

    Rendering result:

    :ref:`Building Document <building-documentation-1>`

Linking to Kconfig References
-----------------------------

If you need to link to Kconfig references when writing documentation, please refer to the following syntax. The references are generated by :project_file:`kconfig_reference.py <src/esp_docs/idf_extensions/kconfig_reference.py>`. We use the Kconfig files of ESP-IDF as examples to introduce this syntax.

Syntax and examples:

.. code-block:: text

    - :ref:`CONFIG_APP_COMPATIBLE_PRE_V3_1_BOOTLOADERS`
    - :ref:`CONFIG_APP_COMPATIBLE_PRE_V2_1_BOOTLOADERS`
    - :ref:`CONFIG_APP_BUILD_TYPE`
    - :ref:`CONFIG_APP_REPRODUCIBLE_BUILD`
    - :ref:`CONFIG_APP_NO_BLOBS`

If you use ``:ref:`CONFIG_APP_COMPATIBLE_PRE_V3_1_BOOTLOADERS``` in ESP-IDF documents, this can lead you to the `description of this Kconfig reference <https://docs.espressif.com/projects/esp-idf/en/release-v5.0/esp32/api-reference/kconfig.html#config-app-compatible-pre-v3-1-bootloaders>`__.

.. _link-api-member:

Linking to Classes, Functions, Enumerations, etc
------------------------------------------------

For linking to classes, functions, enumerations and other structure types in the doxygen API documentation, please refer to the following syntax. We also use structure types defined in ESP-IDF as examples to introduce this syntax.

Syntax:

.. code-block:: text

    - Class - :cpp:class:`name`
    - Function - :cpp:func:`name`
    - Structure - :cpp:type:`name`
    - Structure Member - :cpp:member:`struct_name::member_name`
    - Enumeration - :cpp:type:`name`
    - Enumeration Value - :cpp:enumerator:`name`
    - Defines - :c:macro:`name`

Examples:

.. code-block:: text

    - Class - :cpp:class:`esp_mqtt_client_config_t`
    - Function - :cpp:func:`esp-gcov_dump`
    - Structure - :cpp:type:`mesh_cfg_t`
    - Structure Member - :cpp:member:`eth_esp32_emac_config_t::clock_config`
    - Enumeration - :cpp:type:`esp_partition_type_t`
    - Enumeration Value - :cpp:enumerator:`WIFI_MODE_APSTA`
    - Defines - :c:macro:`ESP_OK`

Linking to GitHub Files
-----------------------

In addition to linking to documentation in the ``docs`` folder, you may also need to link to other files in the project, for example, the header and program files. You can link to them on GitHub.

When linking to files on GitHub, do not use absolute/hardcoded URLs. We have developed :project_file:`link_roles.py <src/esp_docs/esp_extensions/link_roles.py>`, so that you can use Docutils custom roles to generate links. These auto-generated links point to the tree or blob for the git commit ID (or tag) of the repository. This is needed to ensure that links do not get broken when files in the master branch are moved around or deleted. The roles will transparently handle files that are located in submodules and will link to the submodule’s repository with the correct commit ID.

Syntax and explanation:

.. code-block:: text

    - :project:`path`  - points to directories in the project repository
    - :project_file:`path`  - points to files in the project repository
    - :project_raw:`path`  - points to raw view of files in the project repository
    - :component:`path`  - points to directories in the components directory of the project repository
    - :component_file:`path`  - points to files in the components directory of the project repository
    - :component_raw:`path`  - points to raw view of files in the components directory of the project repository
    - :example:`path`  - points to directories in the examples directory of the project repository
    - :example_file:`path`  - points to files in the examples directory of the project repository
    - :example_raw:`path`  - points to raw view of files in the examples directory of the project repository

Examples:

.. code-block:: text

    - :example:`doxygen/en`
    - :example:`English Version <doxygen/en>`
    - :example_file:`doxygen/en/conf.py`
    - :example_raw:`doxygen/en/conf.py`

Rendering results:

- :example:`doxygen/en`
- :example:`English Version <doxygen/en>`
- :example_file:`doxygen/en/conf.py`
- :example_raw:`doxygen/en/conf.py`

By running ``build-docs gh-linkcheck``, you can search .rst files for presence of hard-coded links (identified by tree/master, blob/master, or raw/master part of the URL). This check is recommended to be added to the CI pipeline.

Linking to External Pages
-------------------------

Generally, you can always use URL to link to external pages. For example, if you want link to Espressif's homepage, you can refer to the following syntax.

Syntax and example:

.. code-block:: text

    Welcome to `Espressif <https://www.espressif.com/>`_!

Rendering result:

Welcome to `Espressif <https://www.espressif.com/>`_!

Please note that if you have several links with the same display text, it will lead to the Sphinx warning ``duplicate explicit target names``. To avoid this issue, you can use two underscores ``__`` at the end of links. For example,

.. code-block:: text

    Welcome to `Espressif <https://www.espressif.com/>`__!

Rendering result:

Welcome to `Espressif <https://www.espressif.com/>`__!

Linking to ESP TRMs and Datasheets
----------------------------------

If you need to link to Espressif's TRMs and datasheets of different targets, you can also use the external links introduced above. However, ESP-Docs offers a simple way by defining the macros {IDF_TARGET_TRM_EN_URL}, {IDF_TARGET_TRM_CN_URL}, {IDF_TARGET_DATASHEET_EN_URL} and {IDF_TARGET_DATASHEET_CN_URL}. You can directly use them to link to related TRMs and datasheets. For details, please refer to :project_file:`format_esp_target.py <src/esp_docs/esp_extensions/format_esp_target.py>`.

Linking to a Whole TRM or Datasheet File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can choose a macro to link to the TRM or datasheet of a specific target in your document.

Syntax and example:

.. code-block:: text

    Please refer to `ESP32-S3 TRM <{IDF_TARGET_TRM_EN_URL}>`__.
    Please refer to `ESP32-S3 Datasheet <{IDF_TARGET_DATASHEET_EN_URL}>`__.

Linking to Chapters of a TRM or Datasheet File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can link to a specific chapter of a TRM or datasheet file by appending #hypertarget-name at the end of the macros. This hypertarget acts like a bookmark.

For example, if you need to refer to Chapter I2C Controller in the ESP32-S3 TRM, use the following link.

Syntax and example:

.. code-block:: text

    For details, please refer to *ESP32-S3 Technical Reference Manual* > *I2C Controller (I2C)* [`PDF <{IDF_TARGET_TRM_EN_URL}#i2c>`__].

For the specific hypertargets of chapters in different ESP TRMs, please go to Documentation Team Site > Section ESP-Docs User Guide > Hypertargets of chapters.

Resources
---------

For more information about links, please refer to `Cross-referencing with Sphinx <https://docs.readthedocs.io/en/stable/guides/cross-referencing-with-sphinx.html>`_.
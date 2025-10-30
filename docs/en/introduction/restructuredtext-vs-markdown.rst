reStructuredText v.s. Markdown
==============================

reStructuredText and Markdown are two markup languages that are easy to read in plain-text format. Comparatively, Markdown is simpler than reStructuredText regarding syntax, formatting, and documentation build system, so many startup project documentation would use Markdown for its simplicity.

If your project is small, with a limited number of documents (for example, less than 5) and subfolders, then Markdown is your go-to language.

As your project evolves and becomes more systematic, you might consider switching to reStructuredText which ESP-Docs uses, given that reStructuredText offers more advanced formatting features and better experience but requires fewer manual edits.

This document compares reStructuredText and Markdown in the following aspects, so that you can better understand why reStructuredText is more suitable for complex projects.

.. contents::
    :local:

Extensibility
-------------

Extensibility is a core design principle for reStructuredText. For this markup language, it is straightforward to add:

- Customized ``roles`` and ``directives``, such as ``:example:`` defined in :project_file:`link_roles.py <src/esp_docs/esp_extensions/link_roles.py>`
- Extensions developed by others, such as ``sphinxcontrib.blockdiag``
- Extensions developed by yourself, such as :project_file:`format_esp_target.py <src/esp_docs/esp_extensions/format_esp_target.py>` (see :doc:`../configuring-esp-docs-projects/adding-extensions`)

In Markdown, there is no such built-in support for extensions, and people might use different extensions in their Markdown editors to do the same thing. For example, to draw a diagram in the same project, one might use `UMLet <https://marketplace.visualstudio.com/items?itemName=TheUMLetTeam.umlet>`_ in VS Code, others might use `UmlSync <https://github.com/umlsynco/umlsync>`_ in MacDown.

Because reStructuredText can be more easily extended, it has more features provided by various extensions as described in the following section.

Features
--------

reStructuredText has more built-in and extended features for generating API reference, tables, links, and table of contents. These features can save your time to do manual edits, and make complex documents fancier.

API Reference
^^^^^^^^^^^^^

In reStructuredText, you can include API references generated from header files into your documentation (see :doc:`../writing-documentation/api-documentation`). The generation process of API references can be integrated into the build process. For example, ESP-Docs has an extension called :project_file:`run_doxygen.py <src/esp_docs/esp_extensions/run_doxygen.py>` to generate API references from header files when building documentation. You may navigate to :example:`doxygen`, and run ``build_example.sh`` to see the results.

In Markdown, generating API documentation is not that easy. You need to either write from scratch as shown below, or leverage some third-party API generators.

.. code-block::

    ### *check_model* method

    ```
    Calibrator.check_model(model_proto)
    ```
    Checks the compatibility of your model.

    **Argument**
    - **model_proto** _(ModelProto)_: An FP32 ONNX model.

    **Return**
    - **-1**: The model is incompatible.

Tables
^^^^^^

Thanks to the various :doc:`table formats <../writing-documentation/tables>` supported by reStructuredText, you can create more complex tables with merged cells, bullet lists, and specified column width, etc.

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Column 1
     - Column 2
   * - + Bullet point 1
       + Bullet point 2
     - Column 2 is set to be wider

+----------+----------+
| Column 1 | Column 2 |
+----------+----------+
| Merged cell         |
+---------------------+

In Markdown, you can only adjust table alignment.

Links
^^^^^

In reStructuredText, there are many ways to avoid using raw URL links (see :doc:`../writing-documentation/links`) when you:

- Link to a specific place of other documents in the same project
- Link to other documents in the same project without specifying document name

With ESP-Docs, you can even extend this functionality when you:

- Link to Kconfig references
- Link to classes, functions, enumerations, etc.
- Link to GitHub files of a certain commit

One advantage of using above link syntax is to avoid manual update when links change.

None of these features are supported in Markdown.

Table of Contents
^^^^^^^^^^^^^^^^^

In reStructuredText, you can use the ``toctree`` directive to generate a Table of Contents at a specified folder depth. Using a file path is sufficient, and when document headings change, the headings in toctree will be updated automatically.

.. code-block::

    .. toctree::
        :maxdepth: 2

        release-5.x/5.0/index
        release-5.x/5.1/index

Moreover, with the help of ``toctree``, you can generate a sidebar that contains the table of contents for easy navigation. For example, see the sidebar of `ESP-Docs User Guide <https://docs.espressif.com/projects/esp-docs/en/latest/index.html>`_.

In Markdown, inserting a table of contents with the same effect is also possible, but you need to manually insert each file's path and name, and specify folder structure when including more than one folder levels.

.. code-block::

    - [Migration from 4.4 to 5.0](./release-5.x/5.0/index)
        - [Bluetooth](./release-5.x/5.0/bluetooth)
        - [Wi-Fi](./release-5.x/5.0/wifi)
        - [Peripherals](./release-5.x/5.0/peripherals)
    - [Migration from 5.0 to 5.1](./release-5.x/5.1/index)
        - [Peripherals](./release-5.x/5.0/peripherals)

Besides, in Markdown there is no sidebar to show the documents in this project and to help readers navigate. Take the ESP-DL repository as example. If you are reading `Get Started <https://github.com/espressif/esp-dl/blob/8bc9a5b01350959819f7e1bf8392b3cb26be066b/docs/en/get_started.md>`_, and want to check `how to deploy a model <https://github.com/espressif/esp-dl/tree/8bc9a5b01350959819f7e1bf8392b3cb26be066b/tutorial/quantization_tool_example>`_, there is no way to know where to find this document until you explore almost every folder. Just imagine what a nightmare it would be if the project has 100 files.

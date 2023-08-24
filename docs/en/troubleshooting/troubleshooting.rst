Troubleshooting Build Errors and Warnings
=========================================

When build fails, a message would pop out to alert you. Such a message has two levels of severity:

- Error, which indicates that the build cannot be completed and no HTML files will be generated.
- Warning, which indicates that the HTML files are generated with errors.

This document provides guidelines on addressing build errors and warnings with the help of messages. Errors and warnings in this document are related to either **the esp-docs package** or the **reStructuredText syntax**.

Message Format
--------------

Messages can help you locate errors and warnings and get a hint of why they occur.

For projects using the esp-docs package, a message usually includes the following parameters in sequence:

- Language
- Target
- [Optional] File path
- [Optional] Line number
- Error or warning type

Example of a package-related error:

.. code-block::

    en/esp32s3: Extension error:
    en/esp32s3: Could not import extension linuxdoc.rstFlatTable (exception: No module named 'linuxdoc')

Example of a syntax-related warning:

.. code-block::

    en/esp32s3: Users/johnlee/esp/esp-idf/docs/en/api-reference/peripherals/ledc.rst:318: WARNING: undefined label: pwm-sheet

Among these parameters, **file path** and **line number** are optional. They will not be provided if an error or warning is general and does not apply to a specific file or line.

Package-Related Errors and Warnings
-----------------------------------

Command not found: build-docs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error occurs when you have not:

* installed the esp-docs package properly;
* or correctly set the environment variable PATH.

To address this error, please go to Section :doc:`Building Documentation locally on Your OS <../building-documentation/building-documentation-locally>`, and make sure you have completed all the steps required.

Application error: Cannot find source directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error occurs when you are not in the right directory.

To address this error, navigate to ``docs`` directory:

.. code-block::

    cd docs

Extension error: Could not import extension
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error occurs when you add a new extension to ``conf_common.py`` (or in some projects ``conf.py``), but forget to install this extension.

To address this error, there are two options:

- Option 1: for an extension specific to your project, add it and its version to ``docs/requirements.txt`` of your project. For example, if the extension is sphinx-design and version is 0.2.0, then add:

    .. code-block::

        sphinx-design==0.2.0

  And run the following command in ``docs`` directory:

    .. code-block::

        pip install -r requirements.txt

- Option 2: for an extension that might be reused in other projects using the esp-docs package, add it and its version to :project_file:`setup.cfg` of the ESP-Docs project, for example:

    .. code-block::

        install_requires =
            sphinx-design==0.2.0

  And run the following command:

    .. code-block::

        pip install esp-docs

SyntaxError: future feature annotations is not defined
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Future feature annotations is available from Python 3.7. This error might occur when Python version is too low.

To address this error, try to upgrade your Python to the required version. The required Python version can be found in :project_file:`setup.cfg`.

exception: No documents to build
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error occurs when you build a single document, but this document cannot be found at the specified path. For example:

.. code-block::

    build-docs -t esp32 -l en -i api-reference/peripherals/can.rst

To address this error, correct the document path:

.. code-block::

    build-docs -t esp32 -l en -i api-reference/peripherals/twai.rst

Syntax-Related Errors and Warnings
----------------------------------

ERROR: Unknown interpreted text role
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error occurs when you use an incorrect role, for example ``docs`` instead of ``doc``.

To address this error, correct the name of the :doc:`role <../writing-documentation/basic-syntax>`.

ERROR: Unknown target name
^^^^^^^^^^^^^^^^^^^^^^^^^^

This error occurs when the reference to a ```target`_`` cannot be found by Sphinx.

For example, the section is named as ``Syntax-Related Errors and Warnings``, but referred to as ``Syntax-Related Errors and Warning`` without **s** at the end:

.. code-block::

    Related resources:

    - `Package-Related Errors and Warnings`_
    - `Syntax-Related Errors and Warning`_

    Package-Related Errors and Warnings
    ----------------------------------

    Syntax-Related Errors and Warnings
    ----------------------------------

To address this error, correct the target name.

ERROR: Unknown directive type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error occurs when you use directives of an extension not covered by your project or by the esp-docs package.

To address this error, add the extension following :doc:`../configuring-esp-docs-projects/adding-extensions`.

WARNING: the underline is too short
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This warning occurs when the section title underline is too short, for example:

.. code-block::

    Getting Started
    ===========

To fix this warning, make the title underline the same length as or longer than the title:

.. code-block::

    Getting Started
    ===============

.. note::

    For Chinese titles, each Chinese character requires two underline markers (e.g. ``=``).

WARNING: image file not readable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This warning occurs when Sphinx cannot find the image at the specified path.

To fix this warning, check if the image path is correct.

WARNING: unknown document
^^^^^^^^^^^^^^^^^^^^^^^^^

This warning occurs when Sphinx cannot find the document at specified path.

To fix this warning:

#. Check if the document path is correct.
#. Check if you have used correct syntax for :doc:`role <../writing-documentation/basic-syntax>`. For instance, ``.rst`` in the following example should be removed (see :doc:`../writing-documentation/links`):

.. code-block::

    :doc:`reStructuredText Syntax <../writing-documentation/basic-syntax.rst>`

WARNING: document isn't included in any toctree
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``toctree`` directive glues all ``.rst`` files together into a table of contents (TOC). Therefore, by default every ``.rst`` file is required to be placed under a toctree, otherwise this warning will occur.

To fix this warning, there are two options:

- Option 1: add the ``.rst`` file to its corresponding ``toctree``, for example:

    .. code-block::

        .. toctree::
            :maxdepth: 2

            user_guide

    Usually the corresponding ``toctree`` is in the ``index.rst`` file of the parent folder, and adding file name without ``.rst`` extension would be sufficient.

    If you have already included the ``.rst`` file in a ``toctree`` and this warning still occur, check whether you have used the ``.. only:: TAG`` directive or the ``:TAG:`` role provided by the :doc:`multiple target <../writing-documentation/writing-for-multiple-targets>` feature of esp-docs. For example:

    .. code-block::

        .. only:: esp32

            .. toctree::
            :maxdepth: 2

            user_guide

    .. code-block::

        .. toctree::
        :maxdepth: 2

        :SOC_BT_SUPPORTED: bluetooth

    If yes, suppress this warning by adding the ``.rst`` file to the list of documents it belongs to in ``docs/conf_common.py`` or. For example:

    .. code-block::

        BT_DOCS = ['api-guides/bluetooth.rst]

- Option 2: add ``:orphan:`` at the beginning of the ``.rst`` file. Note that in this way, this file will not be reachable from any table of contents, but will have a matchable HTML file.

WARNING: undefined label
^^^^^^^^^^^^^^^^^^^^^^^^

This warning occurs when reference ``:ref:`` points to a non-existing label, for example:

.. code-block::

    The pin header names are shown in Figure :ref:`user-guide-c6-devkitc-1-v1-board-front`.

To fix this warning, add the missing label ``.. _user-guide-c6-devkitc-1-v1-board-front:`` before the place you want to link to:

.. code-block::

    .. _user-guide-c6-devkitc-1-v1-board-front:

    .. figure:: ../../../_static/esp32-c6-devkitc-1/esp32-c6-devkitc-1-v1-annotated-photo.png
    :align: center
    :alt: ESP32-C6-DevKitC-1 - front
    :figclass: align-center

    ESP32-C6-DevKitC-1 - front

WARNING: Duplicate label
^^^^^^^^^^^^^^^^^^^^^^^^

This warning occurs when the label is not unique, for example:

.. code-block::

    .. _order:
    Retail orders
    ^^^^^^^^^^^^^

    .. _order:
    Wholesale Orders
    ^^^^^^^^^^^^^^^^

To fix this warning, rename the labels to make them unique.

WARNING: duplicate substitution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This warning occurs when the substitution is defined multiple times, either in the same file, or in different files within the same project. For example, the substitution to ``|placeholder|`` is defined both in ``bluetooth.rst`` and ``wifi.rst``:

.. code-block::

    .. |placeholder| image:: https://dl.espressif.com/public/table-header-placeholder.png

To fix this warning, delete repetitive substitutions.

You might encounter cases that after deleting repetitive substitution in ``bluetooth.rst``, the ``|placeholder|`` in ``bluetooth.rst`` cannot be substituted by its definition in ``wifi.rst`` with the following error message popping out:

.. code-block::

    ERROR: undefined substitution referenced: "placeholder"

If this is the case, you may add this substitution definition to the end of every ``.rst`` file by using ``rst_epilog`` in ``docs/conf_common.py`` (or ``docs/conf.py``):

.. code-block::

    rst_epilog = """
    .. |placeholder| image:: https://dl.espressif.com/public/table-header-placeholder.png
    """

Still Have Troubles?
--------------------

This document is far from comprehensive. If you still have no clue why your build fails, here are a few more support options:

- Contact us by submitting documentation feedback.
- For syntax-related errors and warnings, refer to Chapter :doc:`Writing Documentation <../writing-documentation/index>` for the correct format.

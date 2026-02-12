Adding the Language Link Checker
================================

When maintaining documentation in multiple languages (e.g., English and Chinese), it is important to ensure that all pages have proper translation links. The language link checker automatically verifies that all ``.rst`` files included in ``toctree`` directives have the appropriate ``:link_to_translation:`` role, which allows users to switch between language versions of the documentation.

This document describes how to integrate the language link checker into your project pipeline and how to configure it to handle special cases.

What the Language Link Checker Verifies
---------------------------------------

The language link checker verifies that:

- All ``.rst`` files included in ``toctree`` directives have a ``:link_to_translation:`` role
- The translation link points to the correct target language (e.g., English files should link to Chinese, and Chinese files should link to English)
- Each file has exactly one translation link (not multiple links)

There are cases where files should not be reported as errors even if they don't have translation links:

#. **Translation file doesn't exist**: If a file in one language doesn't have a corresponding translation file, it won't be reported as an error.
#. **Placeholder translation files**: If a translation file only contains an ``.. include::`` directive pointing to the original file, it is considered a placeholder and won't trigger an error. For example:

   .. code-block:: rst

      .. include:: ../en/api-guides/build-system-v2.rst

#. **Files listed in warnings file**: You can specify files to ignore in ``lang-linkcheck-warnings.txt``, similar to how ``sphinx-known-warnings.txt`` works for Sphinx warnings. For more information, refer to `Excluding Files from Check`_.

How to Integrate the Language Link Checker
-------------------------------------------

To integrate the language link checker into your project, add a CI/CD job to the GitLab YAML file of your project, for example ``.gitlab-ci.yml``. Here is an example for your reference.

.. code-block::

    .. code-block::

        check_lang_links:
            rules:
                - if: $CI_PIPELINE_SOURCE == 'merge_request_event'
            stage: check
            image: $ESP_DOCS_ENV_IMAGE
            tags:
                - check_doc_links
            allow_failure: false
            script:
                - pip install esp-docs
                - cd docs
                - build-docs -l $DOCLANG lang-linkcheck
            parallel:
                matrix:
                    - DOCLANG: ["en", "zh_CN"]

- ``script``:

  - ``pip install esp-docs``: installs the esp-docs package. If you have already installed the esp-docs package in the template job, you can extend the template job and skip this step. See `gitlab-ci.yml <../../.gitlab-ci.yml>`_ for reference.
  - ``cd docs``: changes the working directory to docs (where the ``build-docs`` command should be run).
  - ``build-docs -l $DOCLANG lang-linkcheck``: runs the language link checker command. The ``-l $DOCLANG`` flag specifies the language for the documentation, with ``$DOCLANG`` being an environment variable set by the parallel matrix. You can also specify  target using the ``-t`` flag.

For explanations of the other parameters, please refer to :doc:`adding-link-check`.

Understanding the Check Results
--------------------------------

After running the language link checker, a report will be displayed in the console output. The report is organized into sections:

- **[EN] Files missing link to Chinese translation**: Lists English files that are missing or have incorrect translation links
- **[ZH_CN] Files missing link to English translation**: Lists Chinese files that are missing or have incorrect translation links
- **[PASSED] Files with correct translation links**: Lists files that passed the check (shown for debugging purposes)

Each error entry shows the file path and a description of the issue:

- ``Missing :link_to_translation: directive``: The file has no translation link
- ``Incorrect :link_to_translation: directive (found 'X', expected 'Y')``: The file links to the wrong language
- ``Multiple :link_to_translation: directives found (expected exactly one)``: The file has multiple translation links

Example Output
^^^^^^^^^^^^^^

.. code-block::

    ================================================================================
    TRANSLATION LINK CHECK RESULTS
    ================================================================================

    [EN] Files missing link to Chinese translation (2):
      ✗ en/getting-started/index.rst: Missing :link_to_translation: directive
      ✗ en/api-reference/uart.rst: Incorrect :link_to_translation: directive (found 'en', expected 'zh_CN')

    [ZH_CN] Files missing link to English translation (1):
      ✗ zh_CN/getting-started/index.rst: Missing :link_to_translation: directive

    [PASSED] Files with correct translation links (15):
      ✓ en/index.rst
      ✓ en/api-reference/i2c.rst
      ...

    ================================================================================
    ERROR: Found 3 file(s) missing translation links.
    Please add the appropriate :link_to_translation: directive to these files.

    Example:
      For English files: :link_to_translation:`zh_CN:[中文]`
      For Chinese files: :link_to_translation:`en:[English]`
    ================================================================================

Excluding Files from Check
--------------------------

To suppress warnings for specific files, create a ``lang-linkcheck-warnings.txt`` file in your docs directory. This file should contain one file path per line (relative to the docs directory, e.g., ``en/page.rst`` or ``zh_CN/folder/page.rst``). Lines starting with ``#`` are treated as comments and ignored.

You can use **wildcards**: ``*`` matches any string and ``?`` matches any single character. For example, ``en/getting-started/*`` ignores all RST files under ``en/getting-started/``, and ``zh_CN/api-reference/*.rst`` ignores all ``.rst`` files in that folder.

.. code-block:: text

    # Files to ignore in lang-linkcheck
    # One file path per line (relative to docs directory); * and ? are allowed
    en/writing-documentation/links.rst
    en/getting-started/*.rst



Contributing Guide
==================

ESP-Docs is an open and common project and we welcome contributions.

Please contribute via `GitHub Pull Requests <https://github.com/espressif/esp-docs/pulls>`_ or internal GitLab Merge Requests.


Report a Bug
------------

- Before reporting a bug, check :doc:`/troubleshooting/index`. You may find the cause of and the fix to the problem.
- If you just want to report the bug, contact the Documentation Team directly, or fill in the `documentation feedback form <https://www.espressif.com/en/company/documents/documentation_feedback?docId=6391&version=latest%2520(v1.3.0-34-g2aaa84f335)>`_.
- If you want to fix the bug, open a pull/merge request with your fix. In the request, describe the problem and solution clearly.


Add a New Feature
-----------------

- Check :doc:`../introduction/what-is-esp-docs` to ensure the feature to be introduced is not implemented in the esp-docs project.
- Open a pull/merge request with your code. In the request, mention what the feature is about and how it will improve the esp-docs project.
- Self-check if your code conforms to `esp-idf coding style <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/contribute/style-guide.html>`_ to speed up the following review process.


Make Minor Changes
------------------

- If you identify typos, grammar errors, or broken links, or want to make other minor changes, contact the Documentation Team directly, or fill in the `documentation feedback form <https://www.espressif.com/en/company/documents/documentation_feedback?docId=6391&version=latest%2520(v1.3.0-34-g2aaa84f335)>`_.
- The Documentation Team will make bulk changes periodically based on such requests.


Commit Messages
---------------

This project uses `Conventional Commits <https://www.conventionalcommits.org/>`_. A pre-commit hook enforces the format on every commit message. To install the hooks, run:

.. code-block:: bash

   pre-commit install

Each commit message must follow the pattern ``<type>: <description>``, for example:

- ``fix: correct version parsing for tags with prefix``
- ``feat: add support for ESP32-H4 target``
- ``docs: update contributing guide``
- ``ci: add commitizen to pre-commit hooks``

Only ``fix`` and ``feat`` commits trigger a version bump. Other types (``docs``, ``ci``, ``refactor``, ``test``, etc.) are recorded in the changelog but do not change the version.

A commit with a ``BREAKING CHANGE`` footer or a ``!`` after the type (e.g. ``feat!: remove legacy API``) triggers a major version bump.


Release Process
---------------

Releases are managed with `Commitizen <https://commitizen-tools.github.io/commitizen/>`_. To create a new release:

.. code-block:: bash

   cz bump

This command will:

1. Determine the next version based on commits since the last tag.
2. Update the version in ``setup.cfg`` and ``pyproject.toml``.
3. Generate/update ``CHANGELOG.md``.
4. Create a commit and a git tag (e.g. ``v2.1.5``).

To preview what would happen without making changes:

.. code-block:: bash

   cz bump --dry-run


Ask a Question
--------------

- If you have questions regarding the documentation or code here, contact the Documentation Team directly, or fill in the `documentation feedback form <https://www.espressif.com/en/company/documents/documentation_feedback?docId=6391&version=latest%2520(v1.3.0-34-g2aaa84f335)>`_.

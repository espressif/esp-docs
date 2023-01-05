ESP-Docs User Guide
===================

:doc:`ESP-Docs <introduction/what-is-esp-docs>` is a documentation-building system developed by Espressif based on Sphinx and Read the Docs. This guide provides information on how to use it as the documentation-building system in a project and how to write, build, configure, and deploy the documentation under this system.

It is primarily for developers, writers, and translators who work on Espressif software documentation. Others can also use it as a reference, such as for `reStructuredText <https://docutils.sourceforge.io/rst.html>`__ syntax, `Sphinx <https://www.sphinx-doc.org/en/master/>`__ extensions, and customizing your documentation-building system based on Sphinx. Note that some links in this guide point to Espressif's internal documentation, which is thus not accessible to external users.

The guide consists of the following major sections:

+-----------------+-------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| |Introduction|_ | Overview, features, extensions, supported markup language of ESP-Docs.                          | |Writing Doc|_                   | ESP-Docs-specific syntax and generic Sphinx and restructuredText syntax,                                                   |
|                 |                                                                                                 |                                  | including :doc:`basic syntax </writing-documentation/basic-syntax>` and :doc:`link syntax </writing-documentation/links>`. |
| `Introduction`_ |                                                                                                 | `Writing Doc`_                   |                                                                                                                            |
+-----------------+-------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                                                                                                                                                                                   |
+-----------------+-------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| |Building Doc|_ |                                                                                                 | |Configuring ESP-Docs Projects|_ | Configuration to Git projects to use ESP-Docs, adding extensions, etc.                                                     |
|                 | How to preview documentation, build documentation from source to target (HTML, PDF) etc.        |                                  |                                                                                                                            |
| `Building Doc`_ |                                                                                                 | `Configuring ESP-Docs Projects`_ |                                                                                                                            |
+-----------------+-------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------------+

.. |Introduction| image:: ../_static/introduction.png
.. _Introduction: introduction/index.html
.. |Writing Doc| image:: ../_static/writing-documentation.png
.. _Writing Doc: writing-documentation/index.html
.. |Building Doc| image:: ../_static/building-documentation.png
.. _Building Doc: building-documentation/index.html
.. |Configuring ESP-Docs Projects| image:: ../_static/configuring-esp-docs-projects.png
.. _Configuring ESP-Docs Projects: configuring-esp-docs-projects/index.html


.. toctree::
    :hidden:

    introduction/index
    writing-documentation/index
    building-documentation/index
    configuring-esp-docs-projects/index
    troubleshooting/index
    contributing-guide
    related-resources
    glossary
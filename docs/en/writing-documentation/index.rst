Writing Documentation
=====================

.. toctree::
   :maxdepth: 1

   basic-syntax
   figures
   table
   link
   glossary
   writing-for-multiple-targets
   redirecting-documents
   api-documentation
   formatting-documents-for-translation

The purpose of this description is to provide a summary on how to write documentation using ``esp-docs``.

Linking Files
-------------

When linking to code on GitHub, do not use absolute/hardcoded URLs. Instead, use docutils custom roles that will generate links for you. These auto-generated links point to the tree or blob for the git commit ID (or tag) of the repository. This is needed to ensure that links do not get broken when files in master branch are moved around or deleted. The roles will transparently handle files that are located in submodules and will link to the submodule’s repository with the correct commit ID.

The following roles are provided:

-  :literal:`:project:`path\`` - points to directory inside project repository
-  :literal:`:project_file:`path\`` - points to file inside project repository
-  :literal:`:project_raw:`path\`` - points to raw view of the file inside project repository
-  :literal:`:component:`path\`` - points to directory inside project repository components dir
-  :literal:`:component_file:`path\`` - points to file inside project repository components dir
-  :literal:`:component_raw:`path\`` - points to raw view of the file inside project repository components dir
-  :literal:`:example:`path\`` - points to directory inside project repository examples dir
-  :literal:`:example_file:`path\`` - points to file inside project repository examples dir
-  :literal:`:example_raw:`path\`` - points to raw view of the file inside project repository examples dir

Example implementation

::

   * :example:`get-started/hello_world`
   * :example:`Hello World! <get-started/hello_world>`

A check is added to the CI build script, which searches RST files for presence of hard-coded links (identified by tree/master, blob/master, or raw/master part of the URL). This check can be run manually: ``cd docs`` and then ``build-docs gh-linkcheck``.

Linking Language Versions
-------------------------

Switching between documentation in different languages may be done using ``:link_to_translation:`` custom role. The role placed on a page of documentation provides a link to the same page in a language specified as a parameter. Examples below show how to enter links to Chinese and English versions of documentation:

::

   :link_to_translation:`zh_CN:中文版`
   :link_to_translation:`en:English`

The language is specified using standard abbreviations like ``en`` or ``zh_CN``. The text after last semicolon is not standardized and may be entered depending on the context where the link is placed, e.g.:

::

   :link_to_translation:`en:see description in English`

Add Notes
---------

Working on a document, you might need to:

-  Place some suggestions on what should be added or modified in future.
-  Leave a reminder for yourself or somebody else to follow up.

In this case, add a todo note to your reST file using the directive ``.. todo::``. For example:

::

   .. todo::

       Add a package diagram.

If you add ``.. todolist::`` to a reST file, the directive will be replaced by a list of all todo notes from the whole documentation.

By default, the directives ``.. todo::`` and ``.. todolist::`` are ignored by documentation builders. If you want the notes and the list of notes to be visible in your locally built documentation, do the following:

1. Open your local ``conf_common.py`` file.
2. Find the parameter ``todo_include_todos``.
3. Change its value from ``False`` to ``True``.

Before pushing your changes to origin, please set the value of ``todo_include_todos`` back to ``False``.

For more details about the extension, see `sphinx.ext.todo <https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#directive-todolist>`__ documentation.

Related Documents
-----------------

OK, but I am new to Sphinx!

1. No worries. All the software you need is well documented. It is also open source and free. Start by checking `Sphinx <https://www.sphinx-doc.org/>`__ documentation. If you are not clear how to write using rst markup language, see `reStructuredText Primer <https://www.sphinx-doc.org/en/stable/rest.html>`__. You can also use markdown (.md) files, and find out more about the specific markdown syntax that we use on `Recommonmark parser’s documentation page <https://recommonmark.readthedocs.io/en/latest>`__.
2. Check the source files of this documentation to understand what is behind of what you see now on the screen. Sources are maintained on GitHub, e.g. `espressif/esp-idf <https://github.com/espressif/esp-idf>`__ repository in the ``docs`` folder. For example, you may refer to `ESP-IDF api-reference/template <https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/template.rst>`__.
3. You will likely want to see how documentation builds and looks like before posting it on the GitHub. This can be done by installing `Doxygen <http://doxygen.nl/>`__, ``esp-docs`` and all it’s dependencies to build it locally, see :doc:`/building-documentation/index`.
4. To preview documentation before building, use `Sublime Text <https://www.sublimetext.com/>`__ editor together with `OmniMarkupPreviewer <https://github.com/timonwong/OmniMarkupPreviewer>`__ plugin. Note that this will only be able to create previews for common RST functionality. Any ``esp-docs`` specific directives and functionality will not be rendered.

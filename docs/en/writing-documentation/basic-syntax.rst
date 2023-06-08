Basic Syntax
============

This document covers some basic reST syntax used in documentation built with ESP-Docs.

.. contents::
  :local:
  :depth: 2


Paragraphs
----------

The paragraph is the most basic block in a reST document. Paragraphs are simply chunks of text separated by one or more blank lines. As in Python, indentation is significant in reST.


Inline Formatting
-----------------

You can specify inline formatting through special symbols around the text you want to format.


Italic
^^^^^^

Use single asterisks to show text as italic or emphasized.

Syntax:

.. code-block:: rst

  *text*

Rendering result:

*text*


Bold
^^^^

Use double asterisks to show text as bold or strong.

Syntax:

.. code-block:: rst

  **text**

Rendering result:

**text**


Literal
^^^^^^^

Use double backquotes to show text as inline literal, to indicate code snippets, variable names, UI elements, etc.

Syntax:

.. code-block:: rst

  ``code``

Rendering result:

``code``


Titles and Headings
-------------------

Normally, there are no heading levels assigned to certain characters as the structure is determined from the succession of headings. However, it is better to stick to the same convention throughout a project. For instance:

- ``#`` with overline, for parts
- ``*`` with overline, for chapters
- ``=``, for sections
- ``-``, for subsections
- ``^``, for subsubsections
- ``"``, for paragraphs


Section Numbering
-----------------

Section numbering is generally **not recommended**, particularly when done manually. However, if no alternative exists, it is advisable to use automatic methods.

To automatically number sections and subsections **across documents**, see :ref:`index-files` > ``numbered`` option.

.. figure:: ../../_static/numbering-across-documents.png
    :align: center
    :scale: 45%
    :alt: Rendered Result - Numbering Across Documents

    Rendered Result - Numbering Across Documents (Click to Enlarge)

To automatically number sections and subsections **in one document**, use

Syntax:

.. code-block:: rst

  .. sectnum::
    :depth: 3
    :prefix: 3.2.
    :start: 1

.. figure:: ../../_static/numbering-in-one-document.png
    :align: center
    :scale: 45%
    :alt: Rendered Result - Numbering in One Document

    Rendered Result - Numbering in One Document (Click to Enlarge)

You may give the following options to the directive:

- ``:depth:``: The number of section levels that are numbered by this directive. The default depth is unlimited.
- ``:prefix:``: An arbitrary string that is prefixed to the automatically generated section numbers. It may be something like "3.2.", which will produce "3.2.1", "3.2.2", and so on. The default is no prefix.
- ``:start:``: The value that will be used for the first section number. Combined with ``prefix``, this may be used to force the right numbering for a document split over several source files. The default is 1.

However, the ``sectnum`` directive also needlessly numbers the title of the document itself. See `invalid section numbering <https://github.com/sphinx-doc/sphinx/issues/4628#issuecomment-366418186>`_ for reasons.


Lists
-----

You can list items either in an ordered or unordered fashion.


Bulleted Lists
^^^^^^^^^^^^^^

Syntax and example:

.. code-block:: rst

  - Each bullet item starts with a symbol and a space.
  - The symbol can be ``-``, ``*``, ``+``, etc.

Rendering result:

- Each bullet item starts with a symbol and a space.
- The symbol can be ``-``, ``*``, ``+``, etc.


Numbered Lists
^^^^^^^^^^^^^^

1. Common numbered lists

Syntax and example:

.. code-block:: rst

  1. Each numbered list item starts with a symbol, a dot, and a space.
  2. The symbol can be 1, A, i, (1) and so on.

Rendering result:

1. Each numbered list item starts with a symbol, a dot, and a space.
2. The symbol can be 1, A, i, (1) and so on.


2. Automatic numbered lists

Syntax and example:

.. code-block:: rst

  #. Each automatic numbered list item starts with the number sign (#), a dot, and a space.
  #. The number sign is #.

Rendering result:

#. Each automatic numbered list item starts with the number sign (#), a dot, and a space.
#. The number sign is #.


Nested Lists
^^^^^^^^^^^^

Example:

.. code-block:: rst

  - This is the first item of the bulleted list.
  - This is the second item of the bulleted list.

    1. This is the first item of the numbered list.
    2. This is the second item of the numbered list.

  - This is the third item of the bulleted list.

Rendering result:

- This is the first item of the bulleted list.
- This is the second item of the bulleted list.

  1. This is the first item of the numbered list.
  2. This is the second item of the numbered list.

- This is the third item of the bulleted list.

Note:

1. Separate different levels of list items with a line.
2. The same level of list items should have the same indentation.


Code Blocks
-----------

A code block consists of the ``code-block`` directive and the actual code indented by four spaces for consistency with other code bases. For Python, C, Bash, and other programming languages, the keywords are highlighted by default.


Simple Code Blocks
^^^^^^^^^^^^^^^^^^

Syntax and example:

.. code-block:: rst

  ::

      AT+GMR

Rendering result:

::

    AT+GMR


Bash Code Blocks
^^^^^^^^^^^^^^^^

Syntax and example:

.. code-block:: rst

  .. code-block:: bash

      ls
      pwd
      touch a.txt

Rendering result:

.. code-block:: bash

    ls
    pwd
    touch a.txt


Python Code Blocks
^^^^^^^^^^^^^^^^^^

Syntax and example:

.. code-block:: rst

  .. code-block:: python

      for i in range(10):
          print(i)

Rendering result:

.. code-block:: python

    for i in range(10):
        print(i)


none Code Blocks
^^^^^^^^^^^^^^^^

If no other type applies, use “none”. It can be useful for obscure languages or mixtures of languages like this mix of Bash and Python.

Syntax and example:

.. code-block:: rst

  .. code-block:: none

      cat program.py

      for i in range(10):
          print(i)

Rendering result:

.. code-block:: none

    cat program.py

    for i in range(10):
        print(i)

For more types, please refer to `code blocks <https://docs.anaconda.com/restructuredtext/detailed/#code-blocks>`_.


Tables of Contents
------------------

To create a table of contents (TOC), use

Syntax:

.. code-block:: rst

  .. contents::
    :local:
    :depth: 1

You may give the following options to the directive:

- ``:local:``: Generate a local table of contents. Entries will only include subsections of the section in which the directive is given. If no explicit title is given, the table of contents will not be titled.
- ``:depth:``: The number of section levels that are collected in the table of contents. The default depth is unlimited.

To generate a TOC of the whole document, use

Syntax:

.. code-block:: rst

  .. contents::
    :depth: 1

To generate a TOC of a section, use

Syntax:

.. code-block:: rst

  .. contents::
    :local:
    :depth: 1


.. _index-files:

Index Files
-----------

Instead of using the ``contents`` directive to show a table of its own contents, the index file uses the ``toctree`` directive to create a table of contents **across** files.

Syntax and example:

.. code-block:: rst

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

Rendering result:

See :doc:`../index`

You may give the following options to the directive:

- ``:maxdepth:``: The maximum depth of the TOC.
- ``:hidden:``: The toctree is hidden in which case they will be used to build the left navigation column but not appear in the main page text.
- ``:numbered:`` (**not recommended**): Numbering starts from the heading of the top level. Sub-toctrees are also automatically numbered. In the example above, numbering will begin from the heading level of ``introduction``.

For more information, see Sphinx `TOC tree <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree>`__ documentation.


Substitutions
-------------

Use a substitution to reuse short, inline content. Substitution definitions are indicated by an explicit markup start (".. ") followed by a vertical bar, the substitution text, another vertical bar, whitespace, and the definition block. A substitution definition block contains an embedded inline-compatible directive (without the leading ".. "), such as "image" or "replace".

For example, use a substitution for a short list of CPU exceptions. To print the CPU exceptions, enter ``|CPU_EXCEPTIONS_LIST|``.

Syntax and example:

.. code-block:: rst

    CPU exceptions: |CPU_EXCEPTIONS_LIST|

The value of ``|CPU_EXCEPTIONS_LIST|`` is defined in a substitution definition.

Syntax and example:

.. code-block:: rst

    .. |CPU_EXCEPTIONS_LIST| replace:: Illegal instruction, load/store alignment error, load/store prohibited error, double exception.

Rendering result:

CPU Exceptions: |CPU_EXCEPTIONS_LIST|

.. |CPU_EXCEPTIONS_LIST| replace:: Illegal instruction, load/store alignment error, load/store prohibited error, double exception.

If you then change the replace value of the substitution, the new value will be used in all instances when you rebuild the project.

For more information, see Sphinx `substitutions <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#substitutions>`__ documentation.


To-Do Notes
-----------

Working on a document, you might need to:

-  Give some suggestions on what should be added or modified in future.
-  Leave a reminder for yourself or somebody else to follow up.

In this case, add a to-do note to your reST file using the directive ``.. todo::``.

Syntax and example:

::

   .. todo::

       Add a package diagram.

If you add ``.. todolist::`` to a reST file, the directive will be replaced by a list of all to-do notes from the whole documentation.

By default, the directives ``.. todo::`` and ``.. todolist::`` are ignored by documentation builders. If you want the notes and the list of notes to be visible in your locally built documentation, take the following steps:

1. Open your local ``conf_common.py`` file.
2. Find the parameter ``todo_include_todos``.
3. Change its value from ``False`` to ``True``.

.. note::
   Before pushing your changes to origin, please set the value of ``todo_include_todos`` back to ``False``. Otherwise, you will make all the to-do notes visible to customers, too.

For more information, see `sphinx.ext.todo <https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#directive-todolist>`__ documentation.

To learn more about the basic syntax, visit Docutils `Quick reStructuredText <https://docutils.sourceforge.io/docs/user/rst/quickref.html>`__.

Creating a Glossary
========================

A glossary or “glossary of terms” is a collection of words pertaining to a specific topic. Usually, it is a list of all terms you used that may not immediately be obvious to your reader. Your glossary only needs to include terms that your reader may not be familiar with, and is intended to enhance their understanding of your work.

Glossaries are not mandatory, but if you use a lot of technical or field-specific terms, it may improve readability to add one. A good example is :doc:`../glossary` in the ESP-Docs User Guide.

If you are going to create a glossary for your project, then you are the target audience of this document. This document describes how to:

- create a consolidated glossary of terms.
- link terms in other documents to their definitions in the glossary.


Create Glossary of Terms
----------------------------

To create a glossary of terms, you can use the directive ``.. glossary::``. Write each glossary entry as a definition list in the form of a term followed by a single-line indented definition as below:

.. code-block::

    .. glossary::

        Term A
            Definition

        Term B
            Definition

The above content will be rendered in the document in the form of:

.. glossary::

    Term A
        Definition

    Term B
        Definition


You can also give the glossary directive a ``:sorted:`` flag that will automatically sort the entries alphabetically.

.. code-block::

    .. glossary::
        :sorted:

        B-term
            Definition B

        A-term
            Definition A

As you can notice, although we wrote B-term before A-term, after applying ``:sorted:``, the rendered effect would be:

.. glossary::
    :sorted:

    B-term
        Definition B

    A-term
        Definition A


Link a Term to its Glossary Entry
---------------------------------------------------

After a glossary is created with the ``.. glossary::`` directive containing a definition list with terms and definitions, you can link a term to its definition in the glossary by using the ``:term:`` role.

For example the ESP-Docs User Guide has one global :doc:`../glossary`. You can use the the following syntax to link the term add-ons to its definition:

.. code-block::

    Please refer to :term:`add-ons`.

This will be rendered as:

Please refer to :term:`add-ons`.

.. Important::

   - The term specified must exactly match a term in the glossary directive. If you use a term that is not explained in a glossary, you’ll get a warning during the documentation build.

   - The term used in your document can only be linked to its definition in the glossary when your document and the glossary are in the same project. For example, this document, which is in the project of ESP-Docs User Guide, can not be linked to the terms defined in the `ESP-ADF Glossary <https://docs.espressif.com/projects/esp-adf/en/latest/english-chinese-glossary.html>`_.


You can link to a term in the glossary while showing different text in the topic by including the term in angle brackets. For example:

.. code-block::

    This file is written in :term:`rst <reStructuredText>` format.

This will be rendered as:

This file is written in :term:`rst <reStructuredText>` format.

.. Important::
    The term in angle brackets must exactly match a term in the glossary. The text before the angle brackets is what users see on the page.

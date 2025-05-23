Using Spellcheckers in VS Code
==============================

Using spellcheckers in your code editors is recommended to ensure high-quality and error-free documentation. This helps reduce spelling mistakes and grammatical errors, improving readability and professionalism.


Why Use Spellcheckers?
----------------------

Our documentation is collaboratively maintained by multiple contributors, many of whom prioritize technical accuracy over grammatical precision. This is particularly common in documentation embedded in header files, where grammar reviews are often skipped during technical revisions.

As a result, spelling and grammatical errors may go unnoticed until they are reported long after publication. Addressing these issues requires considerable manual effort from the documentation team and may still leave some errors unresolved. This not only undermines the overall clarity and professionalism of the documentation, but also leads to unnecessary resource consumption.


Using Code Spell Checker in VS Code
-----------------------------------

Visual Studio Code (VS Code) provides a wide range of extensions to help detect spelling and grammar issues during documentation writing. These tools make it easier to identify and resolve language problems early in the drafting process, ensuring higher-quality output. One popular lightweight choice is the **Code Spell Checker** extension, which works well with code and documents.

To install and configure Code Spell Checker in VS Code:

1.  Open VS Code.
2.  Go to the ``Extensions`` view by clicking the square icon on the sidebar.
3.  Search for **Code Spell Checker** and click **Install**.

    .. figure:: ../../_static/code-spell-checker.png
        :align: center
        :scale: 40%
        :alt: Install Code Spell Checker

        Install Code Spell Checker (Click to enlarge)

4.  Once installed, the extension will start underlining potential spelling mistakes.

    .. note::

        Code Spell Checker includes a variety of built-in dictionaries covering general English (US and GB), software terminology, multiple programming languages, etc. These dictionaries help reduce false positives when checking technical content. You can also define custom dictionaries to include domain-specific terms or abbreviations. For more features and configuration options, refer to the `official documentation <https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker>`_.

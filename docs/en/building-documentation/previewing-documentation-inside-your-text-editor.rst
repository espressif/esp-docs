Previewing Documentation inside Your Text Editor
================================================

This section describes how to preview your rst documentation inside your text editor on your PC.

reStructuredText documents are text files, and can be edited with any text editor. Inside these text editors, there are plenty of extensions or plugins you can use to achieve a live preview.

This approach is good for achieving a real-time live preview while you write because it's simple and fast, but it will only render "base" rst content without any esp-docs specific features. The styles of rendering really depend on the extensions or plugins you use, and you may face issues such as broken links. If you want to preview your rst documentation rendered in exactly the same style as if it is on-line with all the correct reference, go to Section :doc:`Building Documentation locally on Your OS <../building-documentation/building-documentation-locally>`.

In this section, we will use `Visual Studio Code <https://code.visualstudio.com/>`__ and `Sublime Text <https://www.sublimetext.com/>`__ as examples.

Visual Studio Code
------------------

1. Open your **VS Code** instance, and navigate to ``Extensions``.
2. In the top search bar, type in keywords such as "preview" or "rst preview".
3. Install the previewer extension of your choice (for example, `Preview <https://marketplace.visualstudio.com/items?itemName=searKing.preview-vscode>`__), and follow the instruction inside the extension to enable a live preview.

Sublime Text
------------

1. Open your **Sublime Text** instance, go to ``Tools``, and click ``Install Package Control`` from the drop-down menu.
2. After step 1, go to ``Tools`` again, and click on ``Command Palette...``.
3. In the top search bar, type "Install" and select ``Package Control: Install Package``.
4. In the top search bar, type in keywords such as "preview" or "rst preview".
5. Install the previewer plugin (for example, `OmniMarkupPreviewer <http://timonwong.github.io/OmniMarkupPreviewer/>`__) of your choice, and follow the instruction inside the plugin to enable a live preview.

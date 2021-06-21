# Writing Documentation
The purpose of this description is to provide a summary on how to write documentation using `esp-docs`.

## Linking Files

When linking to code on GitHub, do not use absolute/hardcoded URLs. Instead, use docutils custom roles that will generate links for you. These auto-generated links point to the tree or blob for the git commit ID (or tag) of the repository. This is needed to ensure that links do not get broken when files in master branch are moved around or deleted. The roles will transparently handle files that are located in submodules and will link to the submodule's repository with the correct commit ID.

The following roles are provided:

- ``:project:`path` `` - points to directory inside project repository
- ``:project_file:`path` `` - points to file inside project repository
- ``:project_raw:`path` `` - points to raw view of the file inside project repository
- ``:component:`path` `` - points to directory inside project repository components dir
- ``:component_file:`path` `` - points to file inside project repository components dir
- ``:component_raw:`path` `` - points to raw view of the file inside project repository components dir
- ``:example:`path` `` - points to directory inside project repository examples dir
- ``:example_file:`path` `` - points to file inside project repository examples dir
- ``:example_raw:`path` `` - points to raw view of the file inside project repository examples dir

Example implementation

    * :example:`get-started/hello_world`
    * :example:`Hello World! <get-started/hello_world>`

A check is added to the CI build script, which searches RST files for presence of hard-coded links (identified by tree/master, blob/master, or raw/master part of the URL). This check can be run manually: ``cd docs`` and then ``build-docs gh-linkcheck``.


## Linking Language Versions

Switching between documentation in different languages may be done using `:link_to_translation:` custom role. The role placed on a page of documentation provides a link to the same page in a language specified as a parameter. Examples below show how to enter links to Chinese and English versions of documentation::

    :link_to_translation:`zh_CN:中文版`
    :link_to_translation:`en:English`

The language is specified using standard abbreviations like ``en`` or ``zh_CN``. The text after last semicolon is not standardized and may be entered depending on the context where the link is placed, e.g.::

    :link_to_translation:`en:see description in English`


## Add Illustrations

Consider adding diagrams and pictures to illustrate described concepts.

Sometimes it is better to add an illustration than writing a lengthy paragraph to describe a complex idea, a data structure or an algorithm. This repository is using `blockdiag <http://blockdiag.com/en/index.html>`_ suite of tools to generate diagram images from simple text files.

The following types of diagrams are supported:

* `Block diagram <http://blockdiag.com/en/blockdiag/index.html>`_
* `Sequence diagram <http://blockdiag.com/en/seqdiag/index.html>`_
* `Activity diagram <http://blockdiag.com/en/actdiag/index.html>`_
* `Logical network diagram <http://blockdiag.com/en/nwdiag/index.html>`_

With this suite of tools, it is possible to generate beautiful diagram images from simple text format (similar to graphviz’s DOT format). The diagram elements are laid out automatically. The diagram code is then converted into ".png" graphics and integrated "behind the scenes" into **Sphinx** documents.

For the diagram preparation, you can use an on-line [interactive shell](http://interactive.blockdiag.com/?compression=deflate&src=eJxlUMFOwzAMvecrrO3aITYQQirlAIIzEseJQ5q4TUSIq8TVGIh_J2m7jbKc7Ge_5_dSO1Lv2soWvoVYgieNoMh7VGzJR9FJtugZ7lYQ0UcKEbYNOY36rRQHZHUPT68vV5tceGLbWCUzPfeaFFMoBZzecVc56vWwJFnWMmJ59CCZg617xpOFbTSyw0pmvT_HJ7hxtFNGBr6wvuu5SCkchcrZ1vAeXZomznh5YgTqfcpR02cBO6vZVDeXBRjMjKEcFRbLh8f18-Z2UUBDnqP9wmp9ncRmSSfND2ldGo2h_zse407g0Mxc1q7HzJ3-4jzYYTJjtQH3iSV-fgFzx50J) that instantly shows the rendered image.

Below are couple of diagram examples:

* Simple **block diagram** / ``blockdiag`` - [Wi-Fi Buffer Configuration](http://interactive.blockdiag.com/?compression=deflate&src=eJylUk1rwkAQvfsrBntpIUKiRQqSgK0VSj0EtCi0EjbJxCyuuyG7QW3pf-9m06hJeyg0t33zmHkfCZmItjElGwiLJME8IEwjRFHBA3WAj04H9HcFGyZCwoAoldOwUCgNzkWMwZ7GKgUXnKE9gjOcIt2kSuN39sigMiP8jDqX6GmF_Y3GmJCCqUCmJEM9yEXBY4xDcWjOE8GVpO9oztdaGQmRSRAJlMZysjOCKsVj358Fi_H8GV4Nze2Os4zRyvEbB0XktrseQWVktn_ym-wS-UFb0ilt0pa0N6Vn3i_KUEY5zcqrbXWTx_nDaZHjwYvEHGKiSNeC2q_r3FpQZekObAtMTi4XCi2IBBO5e0Rd5L7ppLG574GvO__PUuO7sXTgweTIyY5GcD1XOtToBhYruDf_VvuUad3tD-0_Xq1TLPPSI84xKvNrF9vzLnrTj1M7rYhrXv24cCPVkZUaOK47n1-lOvbk)
* Slightly more complicated **block diagram** - [Wi-Fi programming model](http://interactive.blockdiag.com/?compression=deflate&src=eJyFk09P40AMxe98CqscIVILq72UIFX8kSoQWy0RHABFTuImFtOZaGYKuyC-O840bagaRI7Pfs7Pz0mmTP5cMJbwynNOa2tKi4sF6zJdmIIUvO_tgTz7UCqToQL03nK29OSCrqUpfeXCVxDD6Gg47tSKuKy8yL9b1dWov1E3E4atWtAcl8qnrsKapGDNUhdUZObfdr2UQp3mRhkrXdpoGq-BGwhQmJFaoSZns_Q2mZxdwUNQ44Eojxqcx_x5cAhzo73jN4pHv55WL7m4u0nSZHLbOeiFtBePR9dvmcxm19sWrGvFOXo2utd4CGH5eHQ8bGfcTy-n6fnfO9jMuOfoksV9bvmFbO-Lr27-JPAQ4oqbGJ62c8iN1pQ3EA4O-lOJTncXDvvupCGdu3vmqFQmSQqm3CIYBx0EWou6pADjQJbw3Bj-h3I4onxpsHrCQLnmoD0yVKgLJXuP1x3GsowPmUpfbay3yH5T7khPoi7NnpU-1nisPdkFyY_gV4x9XB3Y0pHdpfoJ60toURQOtqbYuvpJ1B6zDXYym0qmTVpNnh-fpWcbRA)_
* **Sequence diagram** / ``seqdiag`` - [Scan for a Specific AP in All Channels](http://interactive.blockdiag.com/seqdiag/?compression=deflate&src=eJyVkU1PwzAMhu_7FdburUgQXMomTaPcKIdOIIRQlDVuG1EloUknPsR_J2s2rRsT2nKJ9drvY8ex-C4kr8AWXLFSt8waLBg38D0Cf3jh5Io7qRVMQGmFSS-jqJA1qCpXe51cXwTZGg-pUVa1W8tXQRVY8q5xzNbcoNdb3SmBYqk_9vOlVs7Kr3UJoQmMwgDGMMftWwK4QuU28ZOM7uQm3q_zYTQd5OGl4UtsJmMSE5jCXKtSVl2LUPgpXPvpb4Hj1-RUCPWQ3O_K-wKpX84WMLAcB9B-igCouVLYADnDTA_N9GRzHMdnNMoOG2Vb8-4b4CY6Zr4MT3zOF-k9Sx_TbMHy-Sxjtw9Z-mfRHjEA7hD0X8TPLxU91AQ)
* **Packet diagram** / ``packetdiag`` - [NVS Page Structure](http://interactive.blockdiag.com/packetdiag/?compression=deflate&src=eJxFkMFOwzAQRO_9ij2mh63idRKaSj1V_ACIE6DIxG4StTgh3oCg6r_j2JTs8c3szNqDqk-GdacasJ-uGlRjKsfjVPM0GriswE_dn786zS3sQRJAYLbXprpRkS-sNV3TcrAGqM1RTWeujr1l1_2Y2U6rIKUod_DIis2LTbJ1YBneeWY-Nj5ts-AtkudPdnJGQ0JppLRFKXZweDhIWrySsPDB95bHb3BzPLx1_K4GSCSt_-4vMizzmykNSuBlgWKuioJYBOHLROnbEBGe_ZfEh-7pNcolIdF_raA8rl5_AaqqWyE>)

Try them out by modifying the source code and see the diagram instantly rendering below.

There may be slight differences in rendering of font used by the `interactive shell` compared to the font used in the esp-docs documentation.


## Add Notes
---------

Working on a document, you might need to:

- Place some suggestions on what should be added or modified in future.
- Leave a reminder for yourself or somebody else to follow up.

In this case, add a todo note to your reST file using the directive ``.. todo::``. For example:

    .. todo::

        Add a package diagram.

If you add ``.. todolist::`` to a reST file, the directive will be replaced by a list of all todo notes from the whole documentation.

By default, the directives ``.. todo::`` and ``.. todolist::`` are ignored by documentation builders. If you want the notes and the list of notes to be visible in your locally built documentation, do the following:

1. Open your local ``conf_common.py`` file.
2. Find the parameter ``todo_include_todos``.
3. Change its value from ``False`` to ``True``.

Before pushing your changes to origin, please set the value of ``todo_include_todos`` back to ``False``.

For more details about the extension, see [sphinx.ext.todo](https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#directive-todolist) documentation.

Writing generic documentation for multiple chips
------------------------------------------------

The documentation for all of Espressif's chips is built from the same files. To faciliate the writing of documents that can be re-used for multiple different chips (called below "targets"), we provide you with the following functionality:

Exclusion of content based on chip-target
""""""""""""""""""""""""""""""""""""""""""""

Occasionally there will be content that is only relevant for one of targets. When this is the case, you can exclude that content by using the ''.. only:: TAG'' directive, where you replace 'TAG' with one of the following names:

Chip name:

* esp32
* esp32s2
* esp32c3

Define identifiers from 'sdkconfig.h', generated by the default menuconfig settings for the target, e.g:

* CONFIG_FREERTOS_UNICORE

Define identifiers from the soc '\*_caps' headers, e.g:

* SOC_BT_SUPPORTED
* SOC_CAN_SUPPORTED

Example:

    .. only:: esp32

        ESP32 specific content.

This directive also supports the boolean operators 'and', 'or' and 'not'. Example:

    .. only:: SOC_BT_SUPPORTED and CONFIG_FREERTOS_UNICORE

        BT specific content only relevant for single-core targets.

This functionality is provided by the [Sphinx selective exclude](https://github.com/pfalcon/sphinx_selective_exclude) extension.

A weakness in this extension is that it does not correctly handle the case where you exclude a section, that is directly followed by a labeled new section. In these cases everything will render correctly, but the label will not correctly link to the section that follows. A temporary work-around for the cases where this can't be avoided is the following:

    .. only:: esp32

        .. _section_1_label:

        Section 1
        ^^^^^^^^^

        Section one content

        .. _section_2_label:

    .. only:: not esp32

        .. _section_2_label:

    Section 2
    ^^^^^^^^^
    Section 2 content

The :TAG: role is used for excluding content from a table of content tree. For example:

    .. toctree::
        :maxdepth: 1

        :esp32: configure-wrover
        configure-other-jtag

When building the documents, Sphinx will use the above mentioned directive and role to include or exclude content based on the target tag it was called with.

If excluding an entire document from the toctree based on targets, it's necessary to also update the ``exclude_patterns`` list in `docs/conf_common.py` to exclude the file for other targets, or a Sphinx warning "WARNING: document isn't included in any toctree" will be generated..

The recommended way of doing it is adding the document to one of the list that gets included in ``conditional_include_dict`` in `docs/conf_common.py`, e.g. a document which should only be shown for BT capable targets should be added to ``BT_DOCS``. `docs/idf_extensions/exclude_docs.py` will then take care of adding it to ``exclude_patterns`` if the corresponding tag is not set.

If you need to exclude content inside a list or bullet points, then this should be done by using the '':TAG:'' role inside the ''.. list:: '' directive.

    .. list::

        :esp32: - ESP32 specific content
        :SOC_BT_SUPPORTED: - BT specific content
        - Common bullet point
        - Also common bullet point


## Substitution macros
When you need to refer to the chip's name, toolchain name, path or other common names that depend on the target type you can consider using the substitution macros supplied by `idf_extensions/format_esp_target.py`.

For example, the following reStructuredText content:

    This is a {IDF_TARGET_NAME}, with /{IDF_TARGET_PATH_NAME}/soc.c, compiled with `{IDF_TARGET_TOOLCHAIN_PREFIX}-gcc` with `CONFIG_{IDF_TARGET_CFG_PREFIX}_MULTI_DOC`

Would render in the documentation as:

    This is a ESP32-S2, with /{esp32s2}/soc.c, compiled with `xtensa-esp32s2-elf-gcc` with `CONFIG_ESP32S2_MULTI_DOC`.

This extension also supports markup for defining local (within a single source file) substitutions. Place a definition like the following into a single line of the RST file:

    {IDF_TARGET_SUFFIX:default="DEFAULT_VALUE", esp32="ESP32_VALUE", esp32s2="ESP32S2_VALUE", esp32c3="ESP32C3_VALUE"}

This will define a target-dependent substitution of the tag {IDF_TARGET_SUFFIX} in the current RST file. For example:

    {IDF_TARGET_TX_PIN:default="IO3", esp32="IO4", esp32s2="IO5", esp32c3="IO6"}

Will define a substitution for the tag {IDF_TARGET_TX_PIN}, which would be replaced by the text IO5 if sphinx was called with the tag esp32s2.

These single-file definitions can be placed anywhere in the .rst file (on their own line), but the name of the directive must start with ``IDF_TARGET_``.


OK, but I am new to Sphinx!

1. No worries. All the software you need is well documented. It is also open source and free. Start by checking [Sphinx](https://www.sphinx-doc.org/) documentation. If you are not clear how to write using rst markup language, see [reStructuredText Primer](https://www.sphinx-doc.org/en/stable/rest.html). You can also use markdown (.md) files, and find out more about the specific markdown syntax that we use on [Recommonmark parser's documentation page](https://recommonmark.readthedocs.io/en/latest).

2. Check the source files of this documentation to understand what is behind of what you see now on the screen. Sources are maintained on GitHub, e.g. [espressif/esp-idf](https://github.com/espressif/esp-idf) repository in the `docs` folder.

3. You will likely want to see how documentation builds and looks like before posting it on the GitHub. This can be done by installing [Doxygen](http://doxygen.nl/), `esp-docs` and all it's dependencies to build it locally, see [building-documention](building-documention.md).

4. To preview documentation before building, use [Sublime Text](https://www.sublimetext.com/) editor together with [OmniMarkupPreviewer](https://github.com/timonwong/OmniMarkupPreviewer) plugin. Note that this will only be able to create previews for common RST functionality. Any `esp-docs` specific directives and functionality will not be rendered.


Related Documents
-----------------

* [ESP-IDF api-reference/template](https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/template.rst)
* [add-ons-reference](add-ons-reference)

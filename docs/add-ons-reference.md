Documentation Add-ons and Extensions Reference
==============================================

The documentation is built using [Sphinx](http://www.sphinx-doc.org/) which renders text source files in [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText). For some more details on that process, please refer to section [documenting code](documenting-code.md).

Besides Sphinx, there are several other applications that help to provide nicely formatted and easy to navigate documentation. These applications are listed together with the installed version numbers as dependencies to `esp-docs` in [setup.cfg](../setup.cfg).

We build documentation for two languages (English, Simplified Chinese) and for multiple chips. Therefore we don't run `sphinx` directly, there is a wrapper Python program `build_docs.py` that runs Sphinx.

On top of that, we have created a couple of custom add-ons and extensions to help integrate documentation with underlining Espressif repositories and further improve navigation as well as maintenance of documentation.

The purpose of this section is to provide a quick reference to the add-ons and the extensions.

Documentation Folder Structure of a Project
-------------------------------------------

* The repository contains a dedicated documentation folder `docs` in the root.
* The `docs` folder contains localized documentation in `docs/en` (English) and `docs/zh_CN` (simplified Chinese) subfolders.
* Graphics files and fonts common to localized documentation are contained in `docs/_static` subfolder.
* Remaining files in the root of `docs` as well as `docs/en` and `docs/zh_CN` provide configuration and scripts used to automate documentation processing including the add-ons and extensions.
* A `_build` directory is created in the `docs` folder by `build_docs.py`. This directory is not added to the repository.
* `docs/conf_common.py` contains configuration common to each localized documentation (e.g. English, Chinese). The contents of this file is imported to standard Sphinx configuration file `conf.py` located in respective language folders (e.g. `docs/en`, `docs/zh_CN`) during build for each language.
* There are couple of spurious Sphinx warnings that cannot be resolved without doing update to the Sphinx source code itself. For such specific cases, respective warnings are documented in `docs/sphinx-known-warnings.txt` file, that is checked during documentation build, to ignore the spurious warnings.

## Add-ons and Extensions Reference

### Generic Extensions

These are Sphinx extensions developed for Espressif that don't rely on any Espressif-docs-specific behaviour or configuration:

#### [Toctree Filter](../src/esp_docs/generic_extensions/toctree_filter.py)

Sphinx extensions overrides the `:toctree:` directive to allow filtering entries based on whether a tag is set, as `:tagname: toctree_entry`. See the Python file for a more complete description.

#### [List Filter](../src/esp_docs/generic_extensions/list_filter.py)

Sphinx extensions that provides a `.. list::` directive that allows filtering of entries in lists based on whether a tag is set, as `:tagname: - list content`. See the Python file for a more complete description.

#### [HTML redirect](../src/esp_docs/generic_extensions/html_redirect.py)

During documentation lifetime, some source files are moved between folders or renamed. This Sphinx extension adds a mechanism to redirect documentation pages that have changed URL by generating in the Sphinx output static HTML redirect pages. The script is used together with a redirection list `html_redirect_pages`. `conf_common.py` builds this list from `docs/page_redirects.txt`.


#### [Add warnings](../src/esp_docs/generic_extensions/add_warnings.py)

In some cases it might be useful to be able to add warnings to a list of documents. This is the case in IDF when we introduce a new target, which we build docs for, but not all docs are yet updated with useful information. This extension can then be used to give warnings to readers of documents which are not yet updated.

Configuration values:
 * `add_warnings_content`: content of the warning which will be added to the top of the documents.
 * `add_warnings_pages`: list of the documents which the warning will be added to.

### Third Party Extensions

- `sphinxcontrib` extensions for blockdiag, seqdiag, actdiag, nwdiag, rackdiag & packetdiag diagrams.
- `Sphinx selective exclude`_ `eager_only` extension.


### Espressif-Specific Extensions

#### [Run Doxygen](../src/esp_docs/esp_extensions/run_doxygen.py)

Subscribes to `defines-generated` event and runs Doxygen (`docs/doxygen/Doxyfile`) to generate XML files describing key headers, and then runs Breathe to convert these to `.inc` files which can be included directly into API reference pages.

Pushes a number of target-specific custom environment variables into Doxygen, including all macros defined in the project's default `sdkconfig.h` file and all macros defined in all `soc` component `xxx_caps.h` headers. This means that public API headers can depend on target-specific configuration options or `soc` capabilities headers options as `#ifdef` & `#if` preprocessor selections in the header.

This means we can generate different Doxygen files, depending on the target we are building docs for.

#### [Exclude Docs](../src/esp_docs/esp_extensions/exclude_docs.py)
Sphinx extension that updates the excluded documents according to the conditional_include_dict {tag:documents}. If the tag is set, then the list of documents will be included.

Also responsible for excluding documents when building with the config value `docs_to_build` set. In these cases all documents not listed in `docs_to_build` will be excluded.

Subscribes to `defines-generated` as it relies on the sphinx tags to determine which documents to exclude

#### [Format ESP Target](../src/esp_docs/esp_extensions/format_esp_target.py)

An extension for replacing generic target related names with the idf_target passed to the Sphinx command line.

This is a {\IDF_TARGET_NAME}, with /{\IDF_TARGET_PATH_NAME}/soc.c, compiled with `{\IDF_TARGET_TOOLCHAIN_PREFIX}-gcc`
with `CONFIG_{\IDF_TARGET_CFG_PREFIX}_MULTI_DOC`
will, if the backspaces are removed, render as
This is a {IDF_TARGET_NAME}, with /{IDF_TARGET_PATH_NAME}/soc.c, compiled with `{IDF_TARGET_TOOLCHAIN_PREFIX}-gcc` with `CONFIG_{IDF_TARGET_CFG_PREFIX}_MULTI_DOC`.


Also supports markup for defining local (single .rst-file) substitions with the following syntax:
{\IDF_TARGET_TX_PIN:default="IO3",esp32="IO4",esp32s2="IO5"}

This will define a replacement of the tag {\IDF_TARGET_TX_PIN} in the current rst-file.

The extension also overrides the default `.. include::` directive in order to format any included content using the same rules.

These replacements cannot be used inside markup that rely on alignment of characters, e.g. tables.

#### [Link Roles](../src/esp_docs/esp_extensions/link_roles.py)

This is an implementation of a custom `Sphinx Roles <https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html>`_ to help linking from documentation to specific files and folders in project repositories. For description of implemented roles, please see [documenting-code](documenting-code.rst).

#### [Latex Builder](../src/esp_docs/esp_extensions/latex_builder.py)

An extension for adding ESP-Docs specific functionality to the latex builder. Overrides the default Sphinx latex builder.

Creates and adds the espidf.sty latex package to the output directory, which contains some macros for run-time variables such as IDF-Target.


#### [Include Build File](../src/esp_docs/esp_extensions/include_build_file.py)

The `include-build-file` directive is like the built-in `include-file` directive, but file path is evaluated relative to `build_dir`.

### IDF-Specific Extensions

#### [Build System Integration](../src/esp_docs/idf_extensions/build_system/__init__.py)

Python package implementing a Sphinx extension to pull IDF build system information into the docs build.

* Creates a dummy CMake IDF project and runs CMake to generate metadata.
* Registers some new configuration variables and emits a new Sphinx event, both for use by other extensions.

#### Configuration Variables

* `docs_root` - The absolute path of the $IDF_PATH/docs directory
* `idf_path` - The value of IDF_PATH variable, or the absolute path of IDF_PATH if environment unset
* `build_dir` - The build directory passed in by `build_docs.py`, default will be like `_build/<lang>/<target>`
* `idf_target` - The IDF_TARGET value. Expected that `build_docs.py` set this on the Sphinx command line

#### New Event

`project-build-info` event is emitted early in the build, after the dummy project CMake run is complete.

Arguments are `(app, project_description)`, where `project_description` is a dict containing the values parsed from `project_description.json` in the CMake build directory.

Other IDF-specific extensions subscribe to this event and use it to set up some docs parameters based on build system info.

#### [KConfig Reference](../src/esp_docs/idf_extensions/kconfig_reference.py)

Subscribes to `project-build-info` event and uses confgen to generate `kconfig.inc` from the components included in the default project build. This file is then included into `/api-reference/kconfig`

#### [Error to Name](../src/esp_docs/idf_extensions/esp_err_definitions.py)

Small wrapper extension that calls `gen_esp_err_to_name.py` and updates the included .rst file if it has changed.

#### [Generate Toolchain Links](../src/esp_docs/idf_extensions/gen_toolchain_links.py)

There couple of places in documentation that provide links to download the toolchain. To provide one source of this information and reduce effort to manually update several files, this script generates toolchain download links and toolchain unpacking code snippets based on information found in `tools/toolchain_versions.mk`.

#### [Generate Toolchain Links](../src/esp_docs/idf_extensions/gen_version_specific_includes.py)

Another extension to automatically generate reStructuredText Text `.inc` snippets with version-based content for this ESP-IDF version.

#### [Generate Defines](../src/esp_docs/idf_extensions/gen_defines.py)

Sphinx extension to integrate defines from IDF into the Sphinx build, runs after the IDF dummy project has been built.

Parses defines and adds them as sphinx tags.

Emits the new 'defines-generated' event which has a dictionary of raw text define values that other extensions can use to generate relevant data.

### Sphinx-IDF-Theme

HTML/CSS theme for Sphinx based on read the docs's Sphinx theme. For more information see the [Sphinx-IDF-theme repository](https://github.com/espressif/sphinx_idf_theme).

Related Documents
-------------------

  * [Sphinx selective exclude](https://github.com/pfalcon/sphinx_selective_exclude)

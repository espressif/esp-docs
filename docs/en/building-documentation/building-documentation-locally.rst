Building Documentation Locally
==============================

The purpose of this description is to provide a summary on how to build documentation locally using ESP-Docs.


.. _building-documentation-1:

Building HTML Locally on Your PC
--------------------------------

ESP-Docs allows you to build your rst documentation into HTML pages on you local computer with the same `style <https://github.com/espressif/sphinx_idf_theme>`__ exactly as how it will be rendered on the server. In this way, you can:

* Catch and fix any potential build errors (due to markup syntax, incorrect links, labels, missing images, etc.) early, instead of waiting on CI errors.
* Of course, have a peek of your final documentation early.

If you just want to roughly preview your rst files while your write and don't care too much about styles and broken links at this moment, then go to Section :doc:`Previewing Documentation inside Your Text Editor <../building-documentation/previewing-documentation-inside-your-text-editor>`.

Installing Dependencies
^^^^^^^^^^^^^^^^^^^^^^^
In order to build documentation locally on your PC, you need to install the following prerequisites:

1. ESP-Docs - https://github.com/espressif/esp-docs
2. CairoSVG - https://cairosvg.org/documentation/
3. Doxygen (only needed when generating API documentation from header files)- http://doxygen.nl

For building the ESP-IDF documentation, see its own `Building Documentation <https://docs.espressif.com/projects/esp-idf/en/stable/contribute/documenting-code.html#building-documentation>`_ section instead.

.. note::
   Docs building now supports Python 3 only. Python 2 installations will not work.

.. note::
   If you are a Windows user or simply want to use a Docker container, then go directly to :ref:`Using a Docker Container <using-a-docker-container>` at the end of this section.

ESP-Docs
""""""""

All applications needed are `Python <https://www.python.org/>`__ packages, and you can install them in one step as follows:

::

   pip install --user esp-docs

This will pull in all the necessary dependencies such as Sphinx, Breathe, etc.

.. note::
   The installed esp-docs may not be added to your PATH environment variable yet at this moment. To make this tool usable from the command line, add the bin folder where it is installed to your PATH variable by running ``export PATH=path_to_bin_folder:$PATH`` in your terminal.

   To get this ``path_to_bin_folder``, try entering ``pip uninstall esp-docs``, you will see something like:
   ::

      Found existing installation: esp-docs 1.3.0
      Uninstalling esp-docs-1.3.0:
      Would remove:
      /Users/dummy/Library/Python/3.10/bin/build-docs
      /Users/dummy/Library/Python/3.10/bin/deploy-docs
      /Users/dummy/Library/Python/3.10/lib/python/site-packages/esp_docs-1.3.0.dist-info/*
      /Users/dummy/Library/Python/3.10/lib/python/site-packages/esp_docs/*

   The path before ``build-docs`` is your bin path. However, this configuration is only effective in the current terminal session. You need to add PATH again once you reopen your terminal.

   Therefore, if you plan to use esp-docs frequently, consider adding ``export PATH="path_to_bin_folder:$PATH"`` to your shell profile files, such as ``.zprofile``, then refresh the configuration by restarting your terminal or by running ``source [path_to_profile_file]``, for example ``source ~/.zprofile``. Afterwards, you can use esp-docs in any terminal session anytime.

CairoSVG
""""""""

CairoSVG is an SVG 1.1 to PNG, PDF, PS and SVG converter. You can install it as follows:

::

   pip3 install cairosvg

If you have issues, please check out `CairoSVG documentation <https://cairosvg.org/documentation/>`__.

Doxygen
"""""""

Installation of Doxygen is OS dependent:

**Linux**

::

   sudo apt-get install doxygen

**MacOS**

::

   brew install doxygen

.. _building-html-pages:

After these steps, you should be able to build HTML pages on your PC already. To see the details, go to :ref:`Building HTML Pages <building-html-pages>`.

Building HTML Pages
^^^^^^^^^^^^^^^^^^^

After completing the above-mentioned preparation, you can navigate to your docs folders (``cd ~/$PROJECT_PATH/docs``), then build HTML pages locally with the `build-docs` command.

.. note::
   If ``$PROJECT_PATH`` is not the parent to the ``docs`` folder, then please specify the project path with ``--project-path`` option. This is only required when you want to build API documentation.

* Build HTML pages in projects that do not support targets
   ::

      build-docs build

* Build HTML pages for a single language
   ::

      build-docs -l en

   Choices for language (``-l``) are ``en`` and ``zh_CN``.

* Build HTML pages for a single target
   ::

      build-docs -t esp32

   Choices for target (``-t``) are any supported chip targets (for example ``esp32`` and ``esp32s2``).

* Build HTML pages for a single language and target combination only
   ::

      build-docs -t esp32 -l en

   Choices for language (``-l``) are ``en`` and ``zh_CN``, and for target (``-t``) are any supported chip targets (for example ``esp32`` and ``esp32s2``).

* Build HTML pages excluding Doxygen-generated API documentation, which drastically reduces build time
   ::

      build-docs -f

   or by setting the environment variable ``DOCS_FAST_BUILD``. To set an environment variable, go to your project's **Settings** > **CI/CD** and expand the **Variables** section. Select **Add variable** and fill in the details for your variables. For more information on how to add a variable to a project, see the `GitLab documentation <https://docs.gitlab.com/ee/ci/variables/#add-a-cicd-variable-to-a-project>`__.

   .. note::
      To set an environment variable, you need to be a project admin or contact the project admin for help.

   .. note::
      The time it takes to build is mainly determined by the amount of Doxygen API included. This is the reason why build with option `-f` for fast build is much faster.

   .. todo::
      It seems "setting the environment variable ``DOCS_FAST_BUILD``" is not related to building documentation locally? or this is not an CI environment variable? To be verified.

* Build HTML pages for a single document or a subset of documentation
   For a single document
   ::

      build-docs -t esp32 -l en -i api-reference/peripherals/can.rst

   For a subset of documentation by listing all of them
   ::

      build-docs -t esp32 -l en -i api-reference/peripherals/can.rst api-reference/peripherals/adc.rst

   For a subset of documentation by using wildcards:
   ::

      build-docs -l en -t esp32 -i api-reference/peripherals/* build

   .. note::
      Note that when you only build a single document or a subset of documentation. The HTML output won't be perfect, i.e. it will not build a proper index that lists all the documents, and any references to documents that are not built will result in warnings.

* To see the complete list of options:
   ::

      build-docs --help

Checking Output
^^^^^^^^^^^^^^^

The built HTML pages will be placed in ``_build/<language>/<target>/html`` folder.

.. note::
   There are a couple of spurious warnings that cannot be resolved without doing updates to the Sphinx or Doxygen source code. For such specific cases, respective warnings can be documented in ``docs/sphinx-known-warnings.txt`` and ``docs/doxygen-known-warnings.txt`` files, which are checked during the build process to ignore these spurious warnings.

Building PDF Documentation Locally on Your PC
---------------------------------------------

ESP-Docs also allows you to build your rst files into PDF files on your local PC. To do this, on top of all the packages and steps described in :ref:`building-documentation-1`, you also need to complete some additional steps.

Installing Dependencies
^^^^^^^^^^^^^^^^^^^^^^^

1. Install the following LaTeX packages:

   * latexmk
   * texlive-latex-recommended
   * texlive-fonts-recommended
   * texlive-xetex

2. Install the following fonts:

   * Freefont Serif, Sans and Mono OpenType fonts, available as the package ``fonts-freefont-otf`` on Ubuntu
   * Lmodern, available as the package ``fonts-lmodern`` on Ubuntu
   * Fandol, can be downloaded from `ctan.org <https://ctan.org/tex-archive/fonts/fandol>`__ archive

.. note::
   Another alternative is to simply install `TeX Live <https://www.tug.org/texlive/>`__, which contains all LaTeX packages and fonts required to build PDF files. However, it may take you hours to install.

.. note::
   If you are a Windows user or simply want to use a Docker container, then go directly to :ref:`Using a Docker Container <using-a-docker-container>` at the end of this section.

After these steps, you should be able to build PDF files on your PC already. To see the details, go to :ref:`Building PDF Documents <building-pdf-documents>`.

.. _building-pdf-documents:

Building PDF Documents
^^^^^^^^^^^^^^^^^^^^^^
Now you can navigate to your docs folders (``cd ~/$PROJECT_PATH/docs``), then build PDF documents with the same `build-docs` command, but with the ``-bs latex`` option.

* Build PDF for "generic" documentation that doesn't contain a target
   ::

    build-docs -bs latex

* Build PDF for a single language and target combination only
   ::

     build-docs -bs latex -t esp32 -l en

   Choices for language (``-l``) are ``en`` and ``zh_CN``, and for target (``-t``) are any supported chip targets (for example ``esp32`` and ``esp32s2``).

* Or alternatively build both HTML and PDF:
   ::

    build-docs -bs html latex -l en -t esp32

Checking Output
^^^^^^^^^^^^^^^

The built LaTeX and PDF files will be placed in ``_build/<language>/<target>/latex/build`` folder.

.. note::
   There are a couple of spurious warnings that cannot be resolved without doing updates to the Sphinx or Doxygen source code. For such specific cases, respective warnings can be documented in ``docs/sphinx-known-warnings.txt`` and ``docs/doxygen-known-warnings.txt`` files, which are checked during the build process to ignore these spurious warnings.


.. _using-a-docker-container:

Using a Docker Container
------------------------

A Docker container image is a lightweight, standalone, executable package of software that can be prepared to include everything needed to run an application: code, runtime, system tools, system libraries, and in our case, to build the documentation locally. This approach saves you the trouble to configure your PC.

To build documentation locally in a Docker container, complete the steps below:

1. Navigate to your project folder. For example ``cd esp/esp-docs``.
2. Create a container for your project using the image provided by Espressif.
   ::

    docker run -v $PWD:/esp-docs -w /esp-docs -it ciregistry.espressif.cn:8443/esp-idf-doc-env-v5.0

3. Configure your container by running ``pip install -U esp-docs``.

After these steps, you can build docs following the instructions described in Sections :ref:`Building HTML Pages <building-html-pages>` and :ref:`Building PDF Documents <building-pdf-documents>`.

Troubleshooting
---------------

If you experience any warning or error when building documentation locally:

* Check :doc:`Troubleshooting Build Errors and Warnings <../troubleshooting/troubleshooting>`;
* Or contact us by submitting a documentation feedback.

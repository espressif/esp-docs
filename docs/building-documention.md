# Building Documentation
The purpose of this description is to provide a summary on how to build documentation using `esp-docs`.


## Install Dependencies


You can setup environment to build documentation locally on your PC by installing:

1. Doxygen - http://doxygen.nl/
2. Esp-docs - https://github.com/espressif/esp-docs

Docs building now supports Python 3 only. Python 2 installations will not work.

### Doxygen

Installation of Doxygen is OS dependent:

**Linux**

	sudo apt-get install doxygen

**Windows** - install in MSYS2 console

	pacman -S doxygen

**MacOS**

	brew install doxygen


If you are installing on Windows MSYS2 system (Linux and MacOS users should skip this note, Windows users who don't use MSYS2 will need to find other alternatives), **before** going further, execute two extra steps below. These steps are required to install dependencies of "blockdiag" discussed under :ref:`add-illustrations`.

1.  Update all the system packages:

        $ pacman -Syu

    This process will likely require restarting of the MSYS2 MINGW32 console and repeating above commands, until update is complete.

2.  Install *pillow*, that is one of dependences of the *blockdiag*:

        $ pacman -S mingw32/mingw-w64-i686-python-pillow

    Check the log on the screen that ``mingw-w64-i686-python-pillow-4.3.0-1`` or newer is installed. Previous versions of *pillow* will not work.

A downside of Windows installation is that fonts of the `blockdiag pictures` do not render correctly, you will see some random characters instead. Until this issue is fixed, you can use the [interactive shell](http://interactive.blockdiag.com/?compression=deflate&src=eJxlUMFOwzAMvecrrO3aITYQQirlAIIzEseJQ5q4TUSIq8TVGIh_J2m7jbKc7Ge_5_dSO1Lv2soWvoVYgieNoMh7VGzJR9FJtugZ7lYQ0UcKEbYNOY36rRQHZHUPT68vV5tceGLbWCUzPfeaFFMoBZzecVc56vWwJFnWMmJ59CCZg617xpOFbTSyw0pmvT_HJ7hxtFNGBr6wvuu5SCkchcrZ1vAeXZomznh5YgTqfcpR02cBO6vZVDeXBRjMjKEcFRbLh8f18-Z2UUBDnqP9wmp9ncRmSSfND2ldGo2h_zse407g0Mxc1q7HzJ3-4jzYYTJjtQH3iSV-fgFzx50J) to see how the complete picture looks like.


### ESP-Docs


All remaining applications are [Python](https://www.python.org/) packages and you can install them in one step as follows:

	pip install --user esp-docs

This will pull in all the necessary dependencies such as Sphinx, Breathe etc.

## Building Documentation


    cd ~/$PROJECT_PATH/docs

Now you should be ready to build documentation by invoking::

    build-docs build

This will build docs for all supported languages & targets. This can take some time, although jobs will run in parallel up to the number of CPU cores you have (can modify this with the ``--sphinx-parallel-builds`` option, see ``build-docs --help`` for details). The `build` argument is optional, if no subcommand it specified `build-docs` defaults to `build`

To build for a single language and target combination only::

    build-docs -t esp32 -l en

Choices for language (``-l``) are ``en`` and ``zh_CN``. Choices for target (``-t``) are any supported chip targets (for example ``esp32`` and ``esp32s2``).

Build documentation will be placed in ``_build/<language>/<target>/html`` folder. To see it, open the ``index.html`` inside this directory in a web browser.

### Fast build
A trick to speed up building is to skip including doxygen generated API documention into the Sphinx build process, skipping this drastically reduces build time.

This can be achieved by adding the fast-build argument::

    build-docs -f

or by setting the environment variable `DOCS_FAST_BUILD`.

### Building a subset of the documentation
Since building the full documentation can be quite slow, it might be useful to just build just the subset of the documentation you are interested in.

This can be achieved by listing the document you want to build::

    build-docs -t esp32 -l en -i api-reference/peripherals/can.rst

Building multiple documents is also possible::

    build-docs -t esp32 -l en -i api-reference/peripherals/can.rst api-reference/peripherals/adc.rst

As well as wildcards::

    build-docs -l en -t esp32 -i api-reference/peripherals/* build

Note that this is a feature intended to simply testing and debugging during writing of documentation. The HTML output won't be perfect, i.e. it will not build a proper index that lists all the documents, and any references to documents that are not built will result in warnings.

### Building PDF
It is also possible to build latex files and a PDF of the documentation using ``build-docs``. To do this the following Latex packages are required to be installed:

 * latexmk
 * texlive-latex-recommended
 * texlive-fonts-recommended
 * texlive-xetex

The following fonts are also required to be installed:

 * Freefont Serif, Sans and Mono OpenType fonts, available as the package ``fonts-freefont-otf`` on Ubuntu
 * Lmodern, available as the package ``fonts-lmodern`` on Ubuntu
 * Fandol, can be downloaded from [here](https://ctan.org/tex-archive/fonts/fandol)

Now you can build the PDF for a target by invoking::

    build-docs -bs latex -l en -t esp32

Or alternatively build both html and PDF::

    build-docs -bs html latex -l en -t esp32

Latex files and the PDF will be placed in ``_build/<language>/<target>/latex`` folder.

## Deploy Docs

ESP-Docs comes with a helper script for deploying docs to the Espressif webserver:

    deploy-docs

See `deploy_docs_template` in [.gitlab-ci.yml](../.gitlab-ci.yml) for an example on how to define the variables required.

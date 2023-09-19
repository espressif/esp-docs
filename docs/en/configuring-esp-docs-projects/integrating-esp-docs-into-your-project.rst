Integrating ESP-Docs into Your Project
======================================

This document describes how to integrate :doc:`ESP-Docs <../introduction/what-is-esp-docs>` into your project to continuously build and deploy your documentation to a server, such as Espressif's server ``docs.espressif.com`` (recommended for Espressif software documentation).

While performing the steps in this document, you can always refer to the documentation that has already been deployed to Espressif's server as examples, such as `ESP-IDF Programming Guide <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/>`__, `ESP-AT User Guide <https://docs.espressif.com/projects/esp-at/en/latest/esp32/>`__, `esptool.py Documentation <https://docs.espressif.com/projects/esptool/en/latest/esp32/>`__, and `ESP-Docs User Guide <https://docs.espressif.com/projects/esp-docs/en/latest/index.html>`__.

The process to integrate ESP-Docs can be broken down into the following steps:

.. contents::
  :local:
  :depth: 1

.. _get-familiar-doc-folder:

Get Familiar with the Documentation Folder
------------------------------------------

The contents of the :example:`basic` documentation folder are described below to provide more details about the folder structure and the function of each file. Your folder might look slightly different, but being familiar with these building blocks will help you better understand the following steps in this document.

- ``_static``: contains graphics files, sources of diagrams, attachments not shown directly in the documentation (e.g., schematics) as well as other resources, such as font files.

  - ``docs_version.js``: configures target and version information displayed in HTML layout, such as the target and language selector in the top-left corner of `ESP-IDF Programming Guide <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/>`__.
  - ``periph_timing.json``: sample figure in JSON format.
- ``en``: English language folder that contains English documents and a build configuration file.

  - ``conf.py``: build configuration file that contains configuration information specific to the English documents, such as the English copyright information.
  - ``index.rst``: English homepage that defines documentation structure with a table of contents tree (toctree). See `Defining document structure <https://www.sphinx-doc.org/en/master/usage/quickstart.html#defining-document-structure>`__ for more information.
  - ``subpage.rst``: sample subpage of ``index.rst``.
- ``zh_CN``: the same as ``en`` but for the Simplified Chinese language.

  - ``conf.py``: the same as ``en/conf.py`` but for the Chinese documents.
  - ``index.rst``: the same as ``en/index.rst`` but for the Chinese documents.
  - ``subpage.rst``: the same as ``en/subpage.rst`` but in Chinese.
- ``README.md``: introduction to the ``docs`` folder.
- ``build_example.sh``: contains the command to simplify building this sample documentation.
- ``conf_common.py``: contains the build configuration information common to both English and Chinese documents. The contents of this file are imported during the building process for each language to the standard Sphinx configuration file ``conf.py`` located in respective language folders (e.g. ``docs/en``, ``docs/zh_CN``). See `Sphinx Configuration <https://www.sphinx-doc.org/en/master/usage/configuration.html>`__ for more information.
- ``requirements.txt``: package dependencies and their versions for building documentation, such as ESP-Docs.


Prepare a Documentation Folder
------------------------------

1. Copy one of the following sample documentation folders to the root directory of your project depending on whether the project needs support for target, version, or building API documentation from header files:

  .. list-table::
     :header-rows: 1
     :widths: 25 20 20 20

     * - Doc Folder
       - Target
       - Version
       - API Doc
     * - :example:`basic`
       - Y
       - Y
       - –
     * - :example:`doxygen`
       - Y
       - Y
       - Y
     * - :project:`test/build_tests/no_target`
       - –
       - Y
       - Y
     * - :project:`test/build_tests/no_version_info`
       - –
       - –
       - Y
     * - :project:`test/build_tests/target_only`
       - Y
       - –
       - Y

2. Rename the folder to ``docs``.
3. Delete the ``build_example.sh`` file (if there is one).
4. (Optional) Go to ``docs/requirements.txt`` and change the ESP-Docs version as needed. ESP-Docs follows the semantic versioning scheme. For features supported by each release, please see `release history <https://github.com/espressif/esp-docs/releases>`__.


Update Build Configuration Files
--------------------------------

Build configuration files are where you set the variables that are affecting the final documentation output built with ESP-Docs. As mentioned in :ref:`get-familiar-doc-folder`, there should be two types of configuration files in each project:

- ``conf_common.py``
- ``en/conf.py`` and ``zh_CN/conf.py``

The configuration files in the sample documentation folder configure how to build the **sample** documentation instead of your documentation, so you need to reconfigure a few variables for your documentation.

1. In ``conf_common.py``, reconfigure some of the following variables based on your needs:

  - ``languages``: supported languages, such as ``en`` and ``zh_CN``. It must be set to at least one language element, namely the current project's language.
  - ``idf_targets``: project target used as a URL slug, such as ``esp32`` in ``https://docs.espressif.com/projects/esp-idf/en/latest/esp32/``. The variable is optional, but you should set either both this variable and ``idf_target`` or neither. For more information about ``idf_target``, see :ref:`build_system_integration`.
  - ``extensions``: extensions that add more functionalities to ESP-Docs, such as ``sphinx_copybutton`` and ``sphinxcontrib.wavedrom``.
  - ``github_repo``: GitHub repository to which the links generated by :project_file:`link_roles.py <src/esp_docs/esp_extensions/link_roles.py>` point.
  - ``html_context['github_user']``: GitHub user name used by `sphinx_idf_theme <https://github.com/espressif/sphinx_idf_theme>`__.
  - ``html_context['github_repo']``: GitHub repo name used by `sphinx_idf_theme <https://github.com/espressif/sphinx_idf_theme>`__.
  - ``html_static_path``: path to the ``_static`` folder.
  - ``project_slug``: short name of the project as a URL slug, such as ``esp-docs``.
  - ``versions_url``: URL from which to download the ``versions.js`` file. If it is specified as a relative URL, such as ``_static/docs_version.js``, the file will be downloaded relative to the ``HTML`` root folder.
  - ``pdf_file_prefix``: PDF filename prefix used for generating the link to download the PDF together with the target and version name.

2. In ``en/conf.py`` and ``zh_CN/conf.py``, reconfigure some of the following variables based on your needs:

  - ``project``: name of your documentation in HTML, such as ESP-IDF Programming Guide, ESP-AT User Guide.
  - ``copyright``: copyright statement.
  - ``pdf_title``: name of your documentation in PDF.
  - ``language``: language for content autogenerated by ESP-Docs.

.. _update-ci-conf-file:

Update CI Configuration File
----------------------------

.. note::
  The following descriptions assume you are using Gitlab CI for building documentation and deploying it to ``www.espressif.com``, and will have to be tweaked if you are running something else for CI/CD.

The GitLab CI configuration file, ``.gitlab-ci.yml``, is where you add jobs to enable the automatic and continuous building and deploying of your documentation to the ``www.espressif.com`` server.

In the ``.gitlab-ci.yml`` of your project, do the steps given below. For examples, please refer to `esp-docs/.gitlab-ci.yml <https://github.com/espressif/esp-docs/blob/master/.gitlab-ci.yml>`__ and `esp-idf/.gitlab/ci/docs.yml <https://github.com/espressif/esp-idf/blob/master/.gitlab/ci/docs.yml>`__.

1. Use an appropriate docker image to build the documentation. For convenience, you can reuse the image used by ESP-IDF, ``$CI_DOCKER_REGISTRY/esp-idf-doc-env-v5.0:2-3``. For the latest version of this image, go to Documentation Team Site > Section ESP-Docs User Guide > esp-idf-doc-env image.
2. Add the jobs to build documentation in HTML and PDF. For examples, please refer to the ``build_esp_docs_html`` and ``build_esp_docs_pdf`` jobs in :project_file:`.gitlab-ci.yml`.
3. In the above building documentation jobs, add ``pip install -r requirements.txt`` to install package dependencies.
4. Add the jobs to deploy the built documentation to the server:

  a. Copy and paste the ``.deploy_docs_template`` and ``deploy_docs_esp_docs`` jobs from :project_file:`.gitlab-ci.yml` to your ``.gitlab-ci.yml``.
  b. Write the job for deploying your documentation based on the ``deploy_docs_esp_docs`` job.

.. note::
  
  If your project is hosted on GitLab and the updates made in GitLab later are synchronized to GitHub, in such case, please only run ``deploy_docs`` job after the job that synchronizes your repository to GitHub. This is crucial because if synchronization to GitHub fails, the links within your documentation that refer to the GitHub project may not function correctly.

5. Configure the required environment variables depending on your project:

  a: ``ESP_DOCS_LATEST_BRANCH_NAME``: decides which git branch will be built and deployed as ``latest``. Defaults to ``master`` and should therefore be changed to e.g. ``main`` if that is the naming scheme of your master branch in your git repo.

6. Configure the variables mentioned in the jobs that deploy documentation:

  a. Find out who the server's admin is. To know who this person is and more information about the variables, please go to Documentation Team Site > Section ESP-Docs User Guide > Deploying documentation to docs.espressif.com.
  b. Ask the admin to create an SSH key for you and a directory for your documentation on the server.
  c. Go to your project's **Settings** > **CI/CD** and expand the **Variables** section. Select **Add variable** and fill in the details for your variables. For more information on how to add a variable to a project, see the `GitLab documentation <https://docs.gitlab.com/ee/ci/variables/#add-a-cicd-variable-to-a-project>`__.


What's Next?
------------

#. Push your changes to GitLab and check if the pipeline passes.
#. If yes, you can check the **Artifacts** to see what the built sample documentation looks like.
#. Now it is time to put your reST source files into the respective language folder and have them built and deployed!

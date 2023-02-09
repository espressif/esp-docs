Adding Extensions
=================

Sometimes your project might need features that the ESP-Docs package does not support yet. In this case, you may add extensions either to ESP-Docs or to your project.

This document describes how to add third-party extensions and self-developed extensions to ESP-Docs or your project.

Where to Add?
-------------

An extension can be added either to ESP-Docs or to your project depending on the range of use.

If the extension might be used later in other projects integrating ESP-Docs, then add it to ESP-Docs. Otherwise, add it to your own project.

Third-Party Extensions
----------------------

Third-party extensions are those extensions contributed by other users, for example extensions in `LinuxDoc <https://return42.github.io/linuxdoc/>`_ and `sphinx-contrib <https://github.com/sphinx-contrib>`_ libraries.

- To add a third-party extension to **ESP-Docs**, you should:

    #. Add the extension to :project_file:`src/esp_docs/conf_docs.py` of ESP-Docs.

        .. code-block::

            extensions = ['breathe',
                        'sphinx.ext.todo',
                        'sphinx_idf_theme',
                        ]

    #. Add the extension and its version to :project_file:`setup.cfg` of ESP-Docs.

        .. code-block::
            :emphasize-lines: 2, 3

            install_requires =
                    sphinx==4.5.0
                    breathe==4.33.1

- To add a third-party extension to **your project**, you should:

    #. Add the extension to ``docs/conf_common.py`` of your project, or to the language specific configuration file ``docs/$lang$/conf.py`` of your project.

        .. code-block::

            extensions = ['sphinx_copybutton',
                        'sphinxcontrib.wavedrom',
                        'linuxdoc.rstFlatTable',
                        ]

    #. Add the extension and its version to ``docs/requirements.txt`` of your project.

        .. code-block::

            linuxdoc==20210324
            sphinx-design==0.2.0

Self-Developed Extensions
-------------------------

Self-developed extensions are those local extensions created by you and not provided as a package.

- To add a self-developed extension to **ESP-Docs**, you should:

    #. Place the extension in one of the following three folders of ESP-Docs:

        - :project:`src/esp_docs/generic_extensions`, for extensions that do not rely on any Espressif-docs-specific behavior or configuration. 
        - :project:`src/esp_docs/esp_extensions`, for extensions that rely on any Espressif-docs-specific behavior or configuration.
        - :project:`src/esp_docs/idf_extensions`, for extensions that rely on ESP-IDF-docs-specific behavior or configuration.

        For more information about self-developed extension types, you may refer to :ref:`esp-docs-self-developed-extensions`.

    #. Add the extension to :project_file:`src/esp_docs/conf_docs.py` of ESP-Docs:

        .. code-block::

            extensions = ['esp_docs.generic_extensions.html_redirects',
                        'esp_docs.esp_extensions.include_build_file',
                        ]

- To add a self-developed extension to **your project**, you should:

    #. Place the extension in a proper folder of your project.

        For example, in the `esp-iot-solution <https://github.com/espressif/esp-iot-solution>`_ repository, the self-developed extension `link-roles.py <https://github.com/espressif/esp-iot-solution/blob/master/docs/link-roles.py>`_ is placed in the `docs <https://github.com/espressif/esp-iot-solution/tree/master/docs>`_ folder.

    #. Add the extension to ``docs/conf_common.py`` of your project, or to the language specific configuration file ``docs/$lang$/conf.py`` of your project.

        .. code-block::

            extensions = ['link-roles',
                        ]

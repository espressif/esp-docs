Figures
=======

This document will briefly introduce the common image formats used in Espressif software documentation built with ESP-Docs, describe their usage, and provide corresponding examples for writers' reference.


Why Add Figures?
----------------

Figures serve an essential role in conveying complex technical information. If you are writing some technical text and feel like expressing your ideas is getting increasingly harder (for example, while describing logical connections), consider using a diagram. Even the most complex ideas that are hard to understand when written as text can be quickly understood with the simplest of diagrams. The key to success is to choose the right diagram type for your case.

Luckily, diagrams in Espressif software documentation built with ESP-Docs already have more or less established styles.


Adding Figures in ESP-Docs
--------------------------

There are different ways of rendering images in documentation:
- Directives to include ready-to-use pictures created by graphic editors.
- Diagram as Code to create diagrams based on textual descriptions for documents based on markup languages.

Using Directives
^^^^^^^^^^^^^^^^

Pictures could be built in documentation using directives and options. Writers can include a ready-to-use figure with the following source code::

    .. figure:: ../../_static/figure-raster-image-usage.png
        :align: center
        :scale: 90%
        :alt: Development of Applications

        This is the caption of the figure (optional)

Below is the image in PNG format added through the above directives and options:

    .. figure:: ../../_static/figure-raster-image-usage.png
        :align: center
        :scale: 90%
        :alt: Development of Applications

        This is the caption of the figure (optional)

For detailed information about how to use these directives, please refer to Section `Figure <https://docutils.sourceforge.io/docs/ref/rst/directives.html#figure>`_ in the reStructuredText documentation. Below are some notes for writers when using the directives in our documentation.

    - For the ``.. figure::`` directive, the path followed can either be a URL, or a relative path to your figures in the current project. For example, to link the specific figure under the ``_static`` folder, it can be written as::

            .. figure:: ../../_static/doc-format1-recommend.png

        or to access the separate server through the URL::

            .. figure:: https://dl.espressif.com/dl/sche,atocs/pictures/esp32-s2-kaluga-1-kit-v1.0-3d.png

        Note that, for the relative path, if you are not sure about it, please check in the terminal using ``cd ..``. For the URL, if the figures are too large, upload it to a separate server, then provide the URL.

        Generally, for each repo, figures are stored in the ``_static`` folder. Below are some of the paths for your information:

            - ESP-IDF: `esp-idf/docs/_static <https://github.com/espressif/esp-idf/tree/master/docs/_static>`_
            - ESP-ADF: `esp-adf-internal/docs/_static <https://github.com/espressif/esp-adf/tree/master/docs/_static>`_
            - ESP-AT: `esp-at/docs/_static <https://github.com/espressif/esp-at/tree/master/docs/_static>`_
            - ESP-Docs: `esp-docs/docs/_static <https://github.com/espressif/esp-docs/tree/master/docs/_static>`_
            - esp-dev-kits: `esp-dev-kits/docs/_static <https://github.com/espressif/esp-dev-kits/tree/master/docs/_static>`_

        Note that if you use the ``... figure::`` directive to upload the non-editable diagrams (PNG, JPG, etc.), please remember to also upload the editable copy (SVG, ODG, etc.) with the same name as the non-editable diagrams uploaded to the internal image-storing GitLab repository corresponding to the current repository. It is also recommended to add a commented-out link to the editable copy in the figure directive for easier search. The reason why we are doing this is that while the editable copy could be too large to make the repository hard to pull, storing them in another repository could always be a fortune when the content of the document has changed and writers are able to find the original images and edit them at any time.

    - For the ``align:`` option, while another option, ``figclass: align-`` is sometimes used together in ESP-IDF, the priorities are listed below:

        - If the alignments are the same, such as ``:align: left`` and ``:figclass: align-left`` are used, then the figure will be aligned left.
        - If different alignments are defined, such as ``:align: center`` and ``:figclass: align-left`` are used, then the figure will be aligned center (top priority) > left > right (the lowest priority), as ``align:`` has a higher priority than ``figclass: align-``.

        Thus, it is recommended to use ``align:`` instead of ``figclass: align-`` in the documentation.

    - For the ``:scale:`` option, the default is "100%", i.e. no scaling. As on the RTD page, only **700 px** can fit into the page, figures should be scaled to get properly presented on HTML pages. To figure out the percentage of scaling that should be used, please check the width and height of the original figure. For example, if the dimension of the original figure is 3452*1590, then ``:scale:20%`` (which results in 690*318, smaller than 700 px) should be adopted to keep the right proportion presented on the page.

        If a URL is provided as the figure path, and meanwhile the “scale” option is used, an error ``Could not obtain image size. :scale: option is ignored.`` might occur. At this time, you need to provide the image's original width and height explicitly using ``:width:`` and ``:height:`` like below::

            .. figure:: https://dl.espressif.com/dl/schematics/pictures/esp-lyrap-lcd32-v1.1-3d.png
                :align: center
                :width: 2243px
                :height: 1534px
                :scale: 30%
                :alt: EESP-LyraP-LCD32

    - For the ``:alt:`` option, it shows the alternate description of figures. This description will be displayed when the figure is shown not properly on display. Normally, the caption of the figure would be placed here. If the figure is scaled, then the writer should also add **(Click to enlarge)** after the caption.

Using Diagram as Code
^^^^^^^^^^^^^^^^^^^^^

For adding graphics using Diagram as Code, several Sphinx extensions are provided to generate diagram images from simple text files:

- `sphinx.ext.graphviz <https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html>`__: Sphinx extension to generate diagrams from `Graphviz DOT code <https://graphviz.org/doc/info/lang.html>`__, including directed graphs, undirected graphs, and so on.
- Sphinx extensions in the `blockdiag suite <http://blockdiag.com/en/>`__ that generate diagrams from a common DOT-like `blockdiag` syntax:

  * `sphinxcontrib-blockdiag <https://pypi.org/project/sphinxcontrib-blockdiag/>`__: generates `block diagrams <http://blockdiag.com/en/blockdiag/index.html>`__.
  * `sphinxcontrib-seqdiag <https://pypi.org/project/sphinxcontrib-seqdiag/>`__: generates `sequence diagrams <http://blockdiag.com/en/seqdiag/index.html>`__.
  * `sphinxcontrib-actdiag <https://pypi.org/project/sphinxcontrib-actdiag/>`__: generates `activity diagrams <http://blockdiag.com/en/actdiag/index.html>`__.
  * `sphinxcontrib-nwdiag <https://pypi.org/project/sphinxcontrib-nwdiag/>`__: generates `logical network diagrams, rack-structure diagrams, and packet header diagrams <http://blockdiag.com/en/nwdiag/index.html>`__.

- `sphinxcontrib-wavedrom <https://pypi.org/project/sphinxcontrib-wavedrom/>`__: independent extension to generate `digital timing diagrams <https://wavedrom.com>`__ from WaveJSON code.

With these extensions, diagram images are generated from simple text descriptions. The diagram elements are laid out automatically. The diagram code is then typically rendered as raster images (often PNG) and integrated "behind the scenes" into **Sphinx** documents. Choose the one that best fits your diagram type.


Using sphinx.ext.graphviz
~~~~~~~~~~~~~~~~~~~~~~~~~

`sphinx.ext.graphviz <https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html>`__ supports various diagram types, including:

- `Directed graphs <https://graphviz.org/Gallery/directed/>`__, such as flowcharts
- `Undirected graphs <https://graphviz.org/Gallery/undirected/>`__, such as data packet structure diagrams

To use this extension, follow the steps below:

1. **Install the Graphviz package.**

   Before building documentation with this extension, install the Graphviz binaries on your system. Installers for all major platforms are available at https://graphviz.org/download/.

2. **Add** ``sphinx.ext.graphviz`` **to the** ``extensions`` **list in** ``conf.py``::

      extensions += [
          'sphinx.ext.graphviz',
      ]

3. **Create a diagram.**

   Below is an example and its source code:

   .. graphviz::
       :caption: ESP-IDF Development Workflow
       :align: center

       digraph esp_idf_develop {
           graph [rankdir=TB fontname="Helvetica" fontsize=13
                  splines=ortho nodesep=0.5 ranksep=0.6 pad=0.4]
           node  [fontname="Helvetica" fontsize=11 style="filled"
                  fillcolor="white" color="#333333" shape=box margin="0.2,0.12"]
           edge  [fontname="Helvetica" fontsize=10 arrowsize=0.8 color="#333333"]

           start_project   [label="Start a project\nCreate or copy an example" style="filled,dashed"]
           connect_device  [label="Connect your device"]
           configure       [label="Configure project"]
           build           [label="Build project\nCompile firmware"]
           flash           [label="Flash onto device"]
           monitor         [label="Monitor output" shape=oval]

           start_project -> connect_device -> configure -> build -> flash -> monitor
       }

   Source code::

       .. graphviz::
           :caption: ESP-IDF Development Workflow
           :align: center

           digraph esp_idf_develop {
               graph [rankdir=TB fontname="Helvetica" fontsize=13
                      splines=ortho nodesep=0.5 ranksep=0.6 pad=0.4]
               node  [fontname="Helvetica" fontsize=11 style="filled"
                      fillcolor="white" color="#333333" shape=box margin="0.2,0.12"]
               edge  [fontname="Helvetica" fontsize=10 arrowsize=0.8 color="#333333"]

               start_project   [label="Start a project\nCreate or copy an example" style="filled,dashed"]
               connect_device  [label="Connect your device"]
               configure       [label="Configure project"]
               build           [label="Build project\nCompile firmware"]
               flash           [label="Flash onto device"]
               monitor         [label="Monitor output" shape=oval]

               start_project -> connect_device -> configure -> build -> flash -> monitor
           }

   For diagrams with lengthy DOT source, save the code in a ``.dot`` file and reference it
   by path::

       .. graphviz:: ../../../_static/diagrams/development_workflow.dot
           :caption: ESP-IDF Development Workflow
           :align: center

4. **Preview the diagram.**

   To quickly preview the diagram, you can:

   - Use the `Graphviz Online <https://dreampuf.github.io/GraphvizOnline/>`__ tool.
   - Use a Graphviz extension in your IDE, such as `Graphviz Preview <https://marketplace.visualstudio.com/items?itemName=EFanZh.graphviz-preview>`__ for VS Code.
   - :doc:`Build documentation locally <../building-documentation/building-documentation-locally>` and preview the diagram in your browser.

For the full DOT language reference and additional layout options, see the
`Graphviz documentation <https://graphviz.org/documentation/>`__ and the
`sphinx.ext.graphviz extension documentation <https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html>`__.


Using the blockdiag suite
~~~~~~~~~~~~~~~~~~~~~~~~~

The blockdiag suite supports the following diagram types, each handled by a separate extension:

- `sphinxcontrib-blockdiag <https://pypi.org/project/sphinxcontrib-blockdiag/>`__: block diagrams
- `sphinxcontrib-seqdiag <https://pypi.org/project/sphinxcontrib-seqdiag/>`__: sequence diagrams
- `sphinxcontrib-actdiag <https://pypi.org/project/sphinxcontrib-actdiag/>`__: activity diagrams
- `sphinxcontrib-nwdiag <https://pypi.org/project/sphinxcontrib-nwdiag/>`__: logical network diagrams, rack-structure diagrams, and packet header diagrams

All four extensions are enabled in esp-docs by default. They share the same DOT-like syntax. Using ``sphinxcontrib-blockdiag`` as an example:

1. **Create a diagram.**

   Below is an example and its source code:

    .. blockdiag::
        :caption: Wi-Fi Programming Model
        :align: center

        blockdiag wifi-programming-model {

            # global attributes
            node_height = 60;
            node_width = 100;
            span_width = 100;
            span_height = 60;
            default_shape = roundedbox;
            default_group_color = none;

            # node labels
            TCP_STACK [label="TCP\n stack", fontsize=12];
            EVNT_TASK [label="Event\n task", fontsize=12];
            APPL_TASK [label="Application\n task", width = 120, fontsize=12];
            WIFI_DRV  [label="Wi-Fi\n Driver", width = 120, fontsize=12];
            KNOT [shape=none];

            # node connections + labels
            TCP_STACK -> EVNT_TASK [label=event];
            EVNT_TASK -> APPL_TASK [label="callback\n or event"];

            # arrange nodes vertically
            group {
            label = "default handler";
            orientation = portrait;
            EVNT_TASK <- WIFI_DRV [label=event];
            }

            # intermediate node
            group {
                label = "user handler";
                orientation = portrait;
                APPL_TASK -- KNOT;
            }
            WIFI_DRV <- KNOT [label="API\n call"];
        }

    Source code::

        .. blockdiag::
            :caption: Wi-Fi Programming Model
            :align: center

            blockdiag wifi-programming-model {

                # global attributes
                node_height = 60;
                node_width = 100;
                span_width = 100;
                span_height = 60;
                default_shape = roundedbox;
                default_group_color = none;

                # node labels
                TCP_STACK [label="TCP\n stack", fontsize=12];
                EVNT_TASK [label="Event\n task", fontsize=12];
                APPL_TASK [label="Application\n task", width = 120, fontsize=12];
                WIFI_DRV  [label="Wi-Fi\n Driver", width = 120, fontsize=12];
                KNOT [shape=none];

                # node connections + labels
                TCP_STACK -> EVNT_TASK [label=event];
                EVNT_TASK -> APPL_TASK [label="callback\n or event"];

                # arrange nodes vertically
                group {
                label = "default handler";
                orientation = portrait;
                EVNT_TASK <- WIFI_DRV [label=event];
                }

                # intermediate node
                group {
                    label = "user handler";
                    orientation = portrait;
                    APPL_TASK -- KNOT;
                }
                WIFI_DRV <- KNOT [label="API\n call"];
            }

    For diagrams with lengthy source, save the code in a ``.diag`` file and reference it by path::

       .. blockdiag:: ../../../_static/diagrams/twai/state_transition.diag
           :caption: State transition diagram of the TWAI driver (see table below)
           :align: center

2. **Preview the diagram.**

   To quickly preview the diagram, you can:

   - Use the `Kroki online editor <https://kroki.io/>`__.
   - :doc:`Build documentation locally <../building-documentation/building-documentation-locally>` and preview the diagram in your browser.

The following examples from ESP-IDF are available for reference:

-  Simple **block diagram** / ``blockdiag`` - `Wi-Fi TX buffer allocation <https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32/api-guides/wifi-driver/overview.html#id10>`__
-  Slightly more complicated **block diagram** - `Wi-Fi programming model <https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32/api-guides/wifi-driver/overview.html#id9>`__
-  **Sequence diagram** / ``seqdiag`` - `Foreground scan of all Wi-Fi channels <https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32/api-guides/wifi-driver/station-scenarios.html#id2>`__
-  **Rack-structure diagram** / ``rackdiag`` - `Ethernet Data Frame Format <https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32/api-reference/network/esp_eth.html#id41>`__
-  **Packet diagram** / ``packetdiag`` - `Structure of RMT symbols <https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32/api-reference/peripherals/rmt.html#id18>`__

For more details, see the `blockdiag online documentation <http://blockdiag.com/en/blockdiag/sphinxcontrib.html>`__.


Using sphinxcontrib-wavedrom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`sphinxcontrib-wavedrom <https://pypi.org/project/sphinxcontrib-wavedrom/>`__ generates signal waveforms from WaveJSON code.

To use this extension, follow the steps below:

1. **Add the extension to the** ``extensions`` **list in** ``conf.py``::

      extensions += [
          'sphinxcontrib.wavedrom',
      ]

2. **Create a diagram.**

   Below is an example and its source code:

    .. wavedrom::
        :caption: I2C Transmission Waveform
        :align: center

        {
            "head": {
                "text": "Standard I2C Transaction Timing Diagram"
            },
            "signal": [
            {
                "node":"A.....B...................C..D.E...............F...G",
                "period": 0.5},
            {
                "name": "SDA",
                "wave": "1.0...3...3.|.3...4...5...1..0.6...6.|.6...7...10..1", "data": "A6 . A0 R/W ACK D7 . D0 ACK",
                "period": 0.5},
            {
                "name": "SCL",
                "wave": "1...0..1.0.1|0.1.0.1.0.1.0......1.0.1|0.1.0.1.0..1..",
                "period": 0.5}
            ],
            "config":
            {
                "skin": "narrow"
            },
            "edge": [
                "B<->C Write address",
                "E<->F Write data"
            ]
        }

    Source code::

        .. wavedrom::
            :caption: I2C Transmission Waveform
            :align: center

            {
                "head": {
                    "text": "Standard I2C Transaction Timing Diagram"
                },
                "signal": [
                    {
                        "node":"A.....B...................C..D.E...............F...G",
                        "period": 0.5},
                    {
                        "name": "SDA",
                        "wave": "1.0...3...3.|.3...4...5...1..0.6...6.|.6...7...10..1", "data": "A6 . A0 R/W ACK D7 . D0 ACK",
                        "period": 0.5},
                    {
                        "name": "SCL",
                        "wave": "1...0..1.0.1|0.1.0.1.0.1.0......1.0.1|0.1.0.1.0..1..",
                        "period": 0.5}
                    ],
                "config":
                {
                    "skin": "narrow"
                },
                "edge": [
                    "B<->C Write address",
                    "E<->F Write data"
                ]
            }

3. **Preview the diagram.**

   To quickly preview the diagram, you can:

   - Use the `WaveDrom online editor <https://wavedrom.com/editor.html>`__.
   - Use a WaveDrom extension in your IDE, such as `Waveform Render <https://marketplace.visualstudio.com/items?itemName=bmpenuelas.waveform-render>`__ for VS Code.
   - :doc:`Build documentation locally <../building-documentation/building-documentation-locally>` and preview the diagram in your browser.

For the WaveJSON language reference and additional options such as bitfield diagrams,
see the `WaveDrom tutorial <https://wavedrom.com/tutorial.html>`__ and the
`sphinxcontrib-wavedrom documentation <https://github.com/bavovanachte/sphinx-wavedrom>`__.


Summary
~~~~~~~

To conclude, while ready-to-use images drawn in graphic editors might be easier to handle for writers with little experience in creating diagrams, they have rather larger size based on their resolution. As for text-based Diagram as Code graphics, it would undoubtedly cost writers some time to get started and master, but they are smaller in size and easier to version with Git. Thus, it is recommended to use Diagram as Code to present pictures in your files.

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

For adding graphics using Diagram as Code, several sphinx extensions are provided to generate diagram images from simple text files:

- `sphinxcontrib-blockdiag <https://pypi.org/project/sphinxcontrib-blockdiag/>`__: Sphinx extension to generate block diagrams from plaintext.
- `sphinxcontrib-seqdiag <https://pypi.org/project/sphinxcontrib-seqdiag/>`__: Sphinx extension to generate sequence diagrams from plaintext.
- `sphinxcontrib-actdiag <https://pypi.org/project/sphinxcontrib-actdiag/>`__: Sphinx extension to generate activity diagrams from plaintext.
- `sphinxcontrib-nwdiag <https://pypi.org/project/sphinxcontrib-nwdiag/>`__: Sphinx extension to generate network-related diagrams from plaintext.
- `sphinxcontrib-wavedrom <https://pypi.org/project/sphinxcontrib-wavedrom/>`__: Sphinx extension to generate wavedrom diagrams from plaintext.


The following types of diagrams are supported:

-  `Block diagram <http://blockdiag.com/en/blockdiag/index.html>`__
-  `Sequence diagram <http://blockdiag.com/en/seqdiag/index.html>`__
-  `Activity diagram <http://blockdiag.com/en/actdiag/index.html>`__
-  `Logical network diagram <http://blockdiag.com/en/nwdiag/index.html>`__
-  Digital timing diagram provided by `WaveDrom <https://wavedrom.com>`__

.. _blockdiag: http://bitbucket.org/blockdiag/blockdiag/

With this suite of tools, it is possible to generate beautiful diagram images from simple text format (similar to graphviz’s DOT format). The diagram elements are laid out automatically. The diagram code is then converted into “.png” graphics and integrated “behind the scenes” into **Sphinx** documents. Below is an example of Diagram as Code graphics in Espressif software documentation built by ESP-Docs:

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

Here is the source code::

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

If a blockdiag has lengthy code, it is suggested to save the code in a .diag file and provide the path to the file like in Section `Driver Operation <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/twai.html?highlight=can%20protocol#driver-operation>`__ in ESP-IDF, which would reach exactly the same effects as well::

    .. blockdiag:: ../../../_static/diagrams/twai/state_transition.diag
        :caption: State transition diagram of the TWAI driver (see table below)
        :align: center

For the diagram preparation, you can use an online `interactive shell <http://interactive.blockdiag.com/?compression=deflate&src=eJxlUMFOwzAMvecrrO3aITYQQirlAIIzEseJQ5q4TUSIq8TVGIh_J2m7jbKc7Ge_5_dSO1Lv2soWvoVYgieNoMh7VGzJR9FJtugZ7lYQ0UcKEbYNOY36rRQHZHUPT68vV5tceGLbWCUzPfeaFFMoBZzecVc56vWwJFnWMmJ59CCZg617xpOFbTSyw0pmvT_HJ7hxtFNGBr6wvuu5SCkchcrZ1vAeXZomznh5YgTqfcpR02cBO6vZVDeXBRjMjKEcFRbLh8f18-Z2UUBDnqP9wmp9ncRmSSfND2ldGo2h_zse407g0Mxc1q7HzJ3-4jzYYTJjtQH3iSV-fgFzx50J>`__ that instantly shows the rendered image.

There are also a couple of diagram examples provided in the live editor for your reference:

-  Simple **block diagram** / ``blockdiag`` - `Wi-Fi Buffer Configuration <http://interactive.blockdiag.com/?compression=deflate&src=eJylUk1rwkAQvfsrBntpIUKiRQqSgK0VSj0EtCi0EjbJxCyuuyG7QW3pf-9m06hJeyg0t33zmHkfCZmItjElGwiLJME8IEwjRFHBA3WAj04H9HcFGyZCwoAoldOwUCgNzkWMwZ7GKgUXnKE9gjOcIt2kSuN39sigMiP8jDqX6GmF_Y3GmJCCqUCmJEM9yEXBY4xDcWjOE8GVpO9oztdaGQmRSRAJlMZysjOCKsVj358Fi_H8GV4Nze2Os4zRyvEbB0XktrseQWVktn_ym-wS-UFb0ilt0pa0N6Vn3i_KUEY5zcqrbXWTx_nDaZHjwYvEHGKiSNeC2q_r3FpQZekObAtMTi4XCi2IBBO5e0Rd5L7ppLG574GvO__PUuO7sXTgweTIyY5GcD1XOtToBhYruDf_VvuUad3tD-0_Xq1TLPPSI84xKvNrF9vzLnrTj1M7rYhrXv24cCPVkZUaOK47n1-lOvbk>`__
-  Slightly more complicated **block diagram** - `Wi-Fi programming model <http://interactive.blockdiag.com/?compression=deflate&src=eJyFk09P40AMxe98CqscIVILq72UIFX8kSoQWy0RHABFTuImFtOZaGYKuyC-O840bagaRI7Pfs7Pz0mmTP5cMJbwynNOa2tKi4sF6zJdmIIUvO_tgTz7UCqToQL03nK29OSCrqUpfeXCVxDD6Gg47tSKuKy8yL9b1dWov1E3E4atWtAcl8qnrsKapGDNUhdUZObfdr2UQp3mRhkrXdpoGq-BGwhQmJFaoSZns_Q2mZxdwUNQ44Eojxqcx_x5cAhzo73jN4pHv55WL7m4u0nSZHLbOeiFtBePR9dvmcxm19sWrGvFOXo2utd4CGH5eHQ8bGfcTy-n6fnfO9jMuOfoksV9bvmFbO-Lr27-JPAQ4oqbGJ62c8iN1pQ3EA4O-lOJTncXDvvupCGdu3vmqFQmSQqm3CIYBx0EWou6pADjQJbw3Bj-h3I4onxpsHrCQLnmoD0yVKgLJXuP1x3GsowPmUpfbay3yH5T7khPoi7NnpU-1nisPdkFyY_gV4x9XB3Y0pHdpfoJ60toURQOtqbYuvpJ1B6zDXYym0qmTVpNnh-fpWcbRA>`__
-  **Sequence diagram** / ``seqdiag`` - `Scan for a Specific AP in All Channels <http://interactive.blockdiag.com/seqdiag/?compression=deflate&src=eJyVkU1PwzAMhu_7FdburUgQXMomTaPcKIdOIIRQlDVuG1EloUknPsR_J2s2rRsT2nKJ9drvY8ex-C4kr8AWXLFSt8waLBg38D0Cf3jh5Io7qRVMQGmFSS-jqJA1qCpXe51cXwTZGg-pUVa1W8tXQRVY8q5xzNbcoNdb3SmBYqk_9vOlVs7Kr3UJoQmMwgDGMMftWwK4QuU28ZOM7uQm3q_zYTQd5OGl4UtsJmMSE5jCXKtSVl2LUPgpXPvpb4Hj1-RUCPWQ3O_K-wKpX84WMLAcB9B-igCouVLYADnDTA_N9GRzHMdnNMoOG2Vb8-4b4CY6Zr4MT3zOF-k9Sx_TbMHy-Sxjtw9Z-mfRHjEA7hD0X8TPLxU91AQ>`__
-  **Packet diagram** / ``packetdiag`` - `NVS Page Structure <http://interactive.blockdiag.com/packetdiag/?compression=deflate&src=eJxFkMFOwzAQRO_9ij2mh63idRKaSj1V_ACIE6DIxG4StTgh3oCg6r_j2JTs8c3szNqDqk-GdacasJ-uGlRjKsfjVPM0GriswE_dn786zS3sQRJAYLbXprpRkS-sNV3TcrAGqM1RTWeujr1l1_2Y2U6rIKUod_DIis2LTbJ1YBneeWY-Nj5ts-AtkudPdnJGQ0JppLRFKXZweDhIWrySsPDB95bHb3BzPLx1_K4GSCSt_-4vMizzmykNSuBlgWKuioJYBOHLROnbEBGe_ZfEh-7pNcolIdF_raA8rl5_AaqqWyE%3E>`__

Try them out by modifying the source code and see the diagram instantly rendering below.

There may be slight differences in rendering of font used by the ``interactive shell`` compared to the font used in the esp-docs documentation.

For more details, see `online documentation`_ at http://blockdiag.com/.

.. _online documentation: http://blockdiag.com/en/blockdiag/sphinxcontrib.html


To conclude, while ready-to-use images drawn in graphic editors might be easier to handle for writers with little experience in creating diagrams, they have rather larger size based on their resolution. As for text-based Diagram as Code graphics, it would undoubtedly cost writers some time to get started and master, but they are smaller in size and easier to version with Git. Thus, it is recommended to use Diagram as Code to present pictures in your files.

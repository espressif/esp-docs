Writing Documentation
=====================

.. toctree::
    :maxdepth: 1

     Basic Syntax <basic-syntax>
     Figures <figures>
     Table <table>
     Link <link>
     Glossary <glossary>
     Writing for Multiple Targets <writing-for-multiple-targets>
     Redirecting Documents <redirecting-documents>
     API documentation <api-documentation>
     Formatting Documents for Translation <formatting-documents-for-translation>

The purpose of this description is to provide a summary on how to write documentation using ``esp-docs``.

Linking Files
-------------

When linking to code on GitHub, do not use absolute/hardcoded URLs. Instead, use docutils custom roles that will generate links for you. These auto-generated links point to the tree or blob for the git commit ID (or tag) of the repository. This is needed to ensure that links do not get broken when files in master branch are moved around or deleted. The roles will transparently handle files that are located in submodules and will link to the submodule’s repository with the correct commit ID.

The following roles are provided:

-  :literal:`:project:`path\`` - points to directory inside project repository
-  :literal:`:project_file:`path\`` - points to file inside project repository
-  :literal:`:project_raw:`path\`` - points to raw view of the file inside project repository
-  :literal:`:component:`path\`` - points to directory inside project repository components dir
-  :literal:`:component_file:`path\`` - points to file inside project repository components dir
-  :literal:`:component_raw:`path\`` - points to raw view of the file inside project repository components dir
-  :literal:`:example:`path\`` - points to directory inside project repository examples dir
-  :literal:`:example_file:`path\`` - points to file inside project repository examples dir
-  :literal:`:example_raw:`path\`` - points to raw view of the file inside project repository examples dir

Example implementation

::

   * :example:`get-started/hello_world`
   * :example:`Hello World! <get-started/hello_world>`

A check is added to the CI build script, which searches RST files for presence of hard-coded links (identified by tree/master, blob/master, or raw/master part of the URL). This check can be run manually: ``cd docs`` and then ``build-docs gh-linkcheck``.

Linking Language Versions
-------------------------

Switching between documentation in different languages may be done using ``:link_to_translation:`` custom role. The role placed on a page of documentation provides a link to the same page in a language specified as a parameter. Examples below show how to enter links to Chinese and English versions of documentation:

::

   :link_to_translation:`zh_CN:中文版`
   :link_to_translation:`en:English`

The language is specified using standard abbreviations like ``en`` or ``zh_CN``. The text after last semicolon is not standardized and may be entered depending on the context where the link is placed, e.g.:

::

   :link_to_translation:`en:see description in English`

Adding Illustrations
--------------------

Consider adding diagrams and pictures to illustrate described concepts.

Sometimes it is better to add an illustration than writing a lengthy paragraph to describe a complex idea, a data structure or an algorithm. This repository is using `blockdiag <http://blockdiag.com/en/index.html>`__ suite of tools to generate diagram images from simple text files.

The following types of diagrams are supported:

-  `Block diagram <http://blockdiag.com/en/blockdiag/index.html>`__
-  `Sequence diagram <http://blockdiag.com/en/seqdiag/index.html>`__
-  `Activity diagram <http://blockdiag.com/en/actdiag/index.html>`__
-  `Logical network diagram <http://blockdiag.com/en/nwdiag/index.html>`__
-  Digital timing diagram provided by `WaveDrom <https://wavedrom.com>`__

With this suite of tools, it is possible to generate beautiful diagram images from simple text format (similar to graphviz’s DOT format). The diagram elements are laid out automatically. The diagram code is then converted into “.png” graphics and integrated “behind the scenes” into **Sphinx** documents.

For the diagram preparation, you can use an on-line `interactive shell <http://interactive.blockdiag.com/?compression=deflate&src=eJxlUMFOwzAMvecrrO3aITYQQirlAIIzEseJQ5q4TUSIq8TVGIh_J2m7jbKc7Ge_5_dSO1Lv2soWvoVYgieNoMh7VGzJR9FJtugZ7lYQ0UcKEbYNOY36rRQHZHUPT68vV5tceGLbWCUzPfeaFFMoBZzecVc56vWwJFnWMmJ59CCZg617xpOFbTSyw0pmvT_HJ7hxtFNGBr6wvuu5SCkchcrZ1vAeXZomznh5YgTqfcpR02cBO6vZVDeXBRjMjKEcFRbLh8f18-Z2UUBDnqP9wmp9ncRmSSfND2ldGo2h_zse407g0Mxc1q7HzJ3-4jzYYTJjtQH3iSV-fgFzx50J>`__ that instantly shows the rendered image.

Below are couple of diagram examples:

-  Simple **block diagram** / ``blockdiag`` - `Wi-Fi Buffer Configuration <http://interactive.blockdiag.com/?compression=deflate&src=eJylUk1rwkAQvfsrBntpIUKiRQqSgK0VSj0EtCi0EjbJxCyuuyG7QW3pf-9m06hJeyg0t33zmHkfCZmItjElGwiLJME8IEwjRFHBA3WAj04H9HcFGyZCwoAoldOwUCgNzkWMwZ7GKgUXnKE9gjOcIt2kSuN39sigMiP8jDqX6GmF_Y3GmJCCqUCmJEM9yEXBY4xDcWjOE8GVpO9oztdaGQmRSRAJlMZysjOCKsVj358Fi_H8GV4Nze2Os4zRyvEbB0XktrseQWVktn_ym-wS-UFb0ilt0pa0N6Vn3i_KUEY5zcqrbXWTx_nDaZHjwYvEHGKiSNeC2q_r3FpQZekObAtMTi4XCi2IBBO5e0Rd5L7ppLG574GvO__PUuO7sXTgweTIyY5GcD1XOtToBhYruDf_VvuUad3tD-0_Xq1TLPPSI84xKvNrF9vzLnrTj1M7rYhrXv24cCPVkZUaOK47n1-lOvbk>`__
-  Slightly more complicated **block diagram** - `Wi-Fi programming model <http://interactive.blockdiag.com/?compression=deflate&src=eJyFk09P40AMxe98CqscIVILq72UIFX8kSoQWy0RHABFTuImFtOZaGYKuyC-O840bagaRI7Pfs7Pz0mmTP5cMJbwynNOa2tKi4sF6zJdmIIUvO_tgTz7UCqToQL03nK29OSCrqUpfeXCVxDD6Gg47tSKuKy8yL9b1dWov1E3E4atWtAcl8qnrsKapGDNUhdUZObfdr2UQp3mRhkrXdpoGq-BGwhQmJFaoSZns_Q2mZxdwUNQ44Eojxqcx_x5cAhzo73jN4pHv55WL7m4u0nSZHLbOeiFtBePR9dvmcxm19sWrGvFOXo2utd4CGH5eHQ8bGfcTy-n6fnfO9jMuOfoksV9bvmFbO-Lr27-JPAQ4oqbGJ62c8iN1pQ3EA4O-lOJTncXDvvupCGdu3vmqFQmSQqm3CIYBx0EWou6pADjQJbw3Bj-h3I4onxpsHrCQLnmoD0yVKgLJXuP1x3GsowPmUpfbay3yH5T7khPoi7NnpU-1nisPdkFyY_gV4x9XB3Y0pHdpfoJ60toURQOtqbYuvpJ1B6zDXYym0qmTVpNnh-fpWcbRA>`__\ \_
-  **Sequence diagram** / ``seqdiag`` - `Scan for a Specific AP in All Channels <http://interactive.blockdiag.com/seqdiag/?compression=deflate&src=eJyVkU1PwzAMhu_7FdburUgQXMomTaPcKIdOIIRQlDVuG1EloUknPsR_J2s2rRsT2nKJ9drvY8ex-C4kr8AWXLFSt8waLBg38D0Cf3jh5Io7qRVMQGmFSS-jqJA1qCpXe51cXwTZGg-pUVa1W8tXQRVY8q5xzNbcoNdb3SmBYqk_9vOlVs7Kr3UJoQmMwgDGMMftWwK4QuU28ZOM7uQm3q_zYTQd5OGl4UtsJmMSE5jCXKtSVl2LUPgpXPvpb4Hj1-RUCPWQ3O_K-wKpX84WMLAcB9B-igCouVLYADnDTA_N9GRzHMdnNMoOG2Vb8-4b4CY6Zr4MT3zOF-k9Sx_TbMHy-Sxjtw9Z-mfRHjEA7hD0X8TPLxU91AQ>`__
-  **Packet diagram** / ``packetdiag`` - `NVS Page Structure <http://interactive.blockdiag.com/packetdiag/?compression=deflate&src=eJxFkMFOwzAQRO_9ij2mh63idRKaSj1V_ACIE6DIxG4StTgh3oCg6r_j2JTs8c3szNqDqk-GdacasJ-uGlRjKsfjVPM0GriswE_dn786zS3sQRJAYLbXprpRkS-sNV3TcrAGqM1RTWeujr1l1_2Y2U6rIKUod_DIis2LTbJ1YBneeWY-Nj5ts-AtkudPdnJGQ0JppLRFKXZweDhIWrySsPDB95bHb3BzPLx1_K4GSCSt_-4vMizzmykNSuBlgWKuioJYBOHLROnbEBGe_ZfEh-7pNcolIdF_raA8rl5_AaqqWyE%3E>`__

Try them out by modifying the source code and see the diagram instantly rendering below.

There may be slight differences in rendering of font used by the ``interactive shell`` compared to the font used in the esp-docs documentation.

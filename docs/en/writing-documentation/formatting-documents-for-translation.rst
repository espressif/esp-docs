Formatting Documents for Translation
============================================

Espressif aims to provide well-formatted and up-to-date English and Chinese documents for customers. To keep English and Chinese versions always in sync, writers are encouraged to update both versions at the same time. However, the documents of one language version may lag behind the other sometimes since some writers, who are non-bilingual, can only update one language version. Therefore, the Documentation Team will provide translation for these documents as soon as possible as the lag-behind documents will be misleading for customers.

To make it easier to update both versions for writers and facilitate the translation process for the Documentation Team, writers and translators should follow the guidelines below when writing and updating documentation.

One Line per Paragraph
-----------------------------------

One paragraph should be written in one line. Breaking lines to enhance readability is only suitable for writing codes. In the documentation, please do not break lines like the below:

    .. figure:: ../../_static/doc-format2-notrecommend.png
        :align: center
        :scale: 27%
        :alt: Line breaks within the same paragraph - not recommended (click to enlarge)

        Line breaks within the same paragraph - not recommended (click to enlarge)

To make the document easier to read, it is recommended to place an empty line to separate the paragraph.

    .. figure:: ../../_static/doc-format1-recommend.png
        :align: center
        :scale: 22%
        :alt: One line per paragraph - recommended (click to enlarge)

        One line per paragraph - recommended (click to enlarge)


Line Number Consistency
----------------------------------

Make the line numbers of English and Chinese documents consistent. For example, as shown below, the title of the 9th line in the English version should also be placed on the 9th line in the Chinese version. Other lines follow the same rule.

    .. figure:: ../../_static/doc-format3-recommend.png
        :align: center
        :scale: 45%
        :alt: Keep the line number for English and Chinese files consistent (click to enlarge)

        Keep the line number for English and Chinese documents consistent (click to enlarge)

This approach could be beneficial in the following ways:

- For non-bilingual writers, they only need to update the same line in the corresponding Chinese or English document when updating documents.

- For translators, if documents are updated in English, then translators can quickly locate where to update in the corresponding Chinese document later.

- By comparing the total number of lines in English and Chinese documents, Documentation Team can quickly find out which document lags behind the other version and provide translation soon.


.. note::

    This document only describes formatting rules that facilitate translation. For other formatting rules, see Espressif Manual of Style.

#
#  SPDX-FileCopyrightText: 2021-2021 Espressif Systems (Shanghai) CO LTD
#
#  SPDX-License-Identifier: Apache-2.0
#

# In some cases it might be useful to be able to add warnings to a list of documents.
# This is the case in IDF when we introduce a new target, which we build docs for,
# but not all docs are yet updated with useful information.
# This extension can then be used to give warnings to readers of documents which are not yet updated.

# Configuration values:
#  * `add_warnings_content`: content of the warning which will be added to the top of the documents.
#  * `add_warnings_pages`: list of the documents which the warning will be added to.

import inspect
import os
from string import Template


def add_warning(app, docname, source):
    if not app.config.add_warnings_pages:
        return

    add_warning_pages_no_file_ext = [os.path.splitext(page)[0] for page in app.config.add_warnings_pages]

    if docname not in add_warning_pages_no_file_ext:
        return

    WARNING_TEMPLATE = Template(
        inspect.cleandoc('''
            .. warning::

                $warning

                This warning was automatically inserted due to the source file being in the `add_warnings_pages` list.
            '''))

    # Special case for :orphan: directive, as this must be the first line in the doc
    # if :orphan: append the warning after it, if not prepend it to the source
    source_partition = source[0].partition('\n')
    if source_partition[0] == ':orphan:':
        source[0] = source_partition[0] + '\n\n' + WARNING_TEMPLATE.substitute(warning=app.config.add_warnings_content) + '\n\n' + source_partition[2]
    else:
        source[0] = WARNING_TEMPLATE.substitute(warning=app.config.add_warnings_content) + '\n' + '\n' + source[0]


def setup(app):
    app.add_config_value('add_warnings_pages', [], 'env')
    app.add_config_value('add_warnings_content', None, 'env')

    app.connect('source-read', add_warning)

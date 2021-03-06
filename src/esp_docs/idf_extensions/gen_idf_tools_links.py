# Generate toolchain download links from toolchain info makefile
from __future__ import print_function

import os.path

from ..util.util import call_with_python, copy_if_modified


def setup(app):
    # we don't actually need project-build-info, just a convenient event to trigger this on
    app.connect('project-build-info', generate_idf_tools_links)

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.1'}


def generate_idf_tools_links(app, project_description):
    print('Generating IDF Tools list')
    os.environ['IDF_MAINTAINER'] = '1'
    tools_rst = os.path.join(app.config.build_dir, 'inc', 'idf-tools-inc.rst')
    tools_rst_tmp = os.path.join(app.config.build_dir, 'idf-tools-inc.rst')
    call_with_python('{}/tools/idf_tools.py gen-doc --output {}'.format(app.config.project_path, tools_rst_tmp))
    copy_if_modified(tools_rst_tmp, tools_rst)

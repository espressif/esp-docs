# -*- coding: utf-8 -*-
#
# Common (non-language-specific) configuration for Read The Docs & Sphinx
#
# Based on a Read the Docs Template documentation build configuration file,
# created by sphinx-quickstart on Tue Aug 26 14:19:49 2014.
#
# This file is imported from a language-specific conf.py (ie en/conf.py or
# zh_CN/conf.py)
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

from __future__ import print_function, unicode_literals

import os
import os.path
import re
import subprocess
import sys

from .get_github_rev import get_github_rev
from .sanitize_version import sanitize_version

esp_docs_dir = os.path.abspath(os.path.dirname(__file__))

# build_docs on the CI server sometimes fails under Python3. This is a workaround:
sys.setrecursionlimit(3500)

# http://stackoverflow.com/questions/12772927/specifying-an-online-image-in-sphinx-restructuredtext-format
#
suppress_warnings = ['image.nonlocal_uri']

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# This is the full exact version, canonical git version description
# visible when you open index.html.
try:
    version = subprocess.check_output(['git', 'describe']).strip().decode('utf-8')
except subprocess.CalledProcessError:
    version = 'master'

# The 'release' version is the same as version for non-CI builds, but for CI
# builds on a branch then it's replaced with the branch name
release = sanitize_version(version)

html_redirect_file_path = 'html_redirect.txt'

print('Version: {0}  Release: {1}'.format(version, release))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['breathe',

              'sphinx.ext.todo',
              'sphinx_idf_theme',
              'sphinxcontrib.blockdiag',
              'sphinxcontrib.seqdiag',
              'sphinxcontrib.actdiag',
              'sphinxcontrib.nwdiag',
              'sphinxcontrib.rackdiag',
              'sphinxcontrib.packetdiag',
              'sphinxcontrib.cairosvgconverter',

              'esp_docs.generic_extensions.html_redirects',
              'esp_docs.generic_extensions.toctree_filter',
              'esp_docs.generic_extensions.list_filter',
              'esp_docs.generic_extensions.google_analytics',

              'esp_docs.esp_extensions.format_esp_target',
              'esp_docs.esp_extensions.include_build_file',
              'esp_docs.esp_extensions.latex_builder',
              'esp_docs.esp_extensions.link_roles',
              'esp_docs.esp_extensions.exclude_docs',

              # from https://github.com/pfalcon/sphinx_selective_exclude
              'sphinx_selective_exclude.eager_only',
              # TODO: determine if we need search_auto_exclude
              # 'sphinx_selective_exclude.search_auto_exclude',
              ]

# sphinx.ext.todo extension parameters
# If the below parameter is True, the extension
# produces output, else it produces nothing.
todo_include_todos = False

# Enabling this fixes cropping of blockdiag edge labels
seqdiag_antialias = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = ['.rst', '.md']

source_parsers = {'.md': 'recommonmark.parser.CommonMarkParser',
                  }

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'


# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['**/inc/**', '_static/', '_build/**']

conditional_include_dict = {}

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# Custom added feature to allow redirecting old URLs
#
# Redirects should be listed in html_redirect_file_path
#
html_redirect_file_path = ''

try:
    with open(html_redirect_file_path) as f:
        lines = [re.sub(' +', ' ', line.strip()) for line in f.readlines() if line.strip() != '' and not line.startswith('#')]
        for line in lines:  # check for well-formed entries
            if len(line.split(' ')) != 2:
                raise RuntimeError('Invalid line in page_redirects.txt: %s' % line)
    html_redirect_pages = [tuple(line.split(' ')) for line in lines]
except FileNotFoundError:
    pass

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = 'sphinx_idf_theme'

# context used by sphinx_idf_theme
html_context = {
    'display_github': True,  # Add 'Edit on Github' link instead of 'View page source'
    'github_version': get_github_rev(),
}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'ReadtheDocsTemplatedoc'


# If true, show URL addresses after external links.
# man_show_urls = False

# -- Options for LaTeX output ---------------------------------------------

latex_template_dir = os.path.join(esp_docs_dir, 'latex_templates')

preamble = ''
with open(os.path.join(latex_template_dir, 'preamble.tex')) as f:
    preamble = f.read()

titlepage = ''
with open(os.path.join(latex_template_dir, 'titlepage.tex')) as f:
    titlepage = f.read()


latex_elements = {
    'papersize': 'a4paper',

    # Latex figure (float) alignment
    'figure_align': 'htbp',

    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'fncychap': '\\usepackage[Sonny]{fncychap}',

    'preamble': preamble,

    'maketitle': titlepage,
}

# The name of an image file (relative to this directory) to place at the bottom of
# the title page.
latex_logo = os.path.join(esp_docs_dir, '_static', 'espressif2.pdf')
latex_engine = 'xelatex'
latex_use_xindy = False

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'ReadtheDocsTemplate', u'Read the Docs Template Documentation',
     u'Read the Docs', 'ReadtheDocsTemplate', 'One line description of project.',
     'Miscellaneous'),
]


# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False


# Override RTD CSS theme to introduce the theme corrections
# https://github.com/rtfd/sphinx_rtd_theme/pull/432
def setup(app):
    app.add_stylesheet('theme_overrides.css')

    # config values that are pushed in by build_docs,py
    if 'idf_target' not in app.config:
        app.add_config_value('idf_target', None, 'env')
        app.add_config_value('idf_targets', None, 'env')
    app.add_config_value('config_dir', None, 'env')
    app.add_config_value('doxyfile_dir', None, 'env')
    app.add_config_value('project_path', None, 'env')

    app.add_config_value('conditional_include_dict', None, 'env')
    app.add_config_value('docs_to_build', None, 'env')

    # Breathe extension variables (depend on build_dir)
    # note: we generate into xml_in and then copy_if_modified to xml dir
    app.add_config_value('build_dir', os.environ['BUILDDIR'], 'env')

    app.add_config_value('latex_template_dir', os.path.join(esp_docs_dir, 'latex_templates'), 'env')

    app.config.breathe_projects = {'esp-docs': os.path.join(app.config.build_dir, 'xml_in/')}
    app.config.breathe_default_project = 'esp-docs'

    # Config values pushed by -D using the cmdline is not available when setup is called
    app.connect('config-inited',  setup_config_values)
    app.connect('config-inited',  setup_html_context)
    app.connect('config-inited',  setup_diag_font)
    app.connect('config-inited',  setup_html)


def setup_config_values(app, config):
    # Sets up global config values needed by other extensions
    idf_target_title_dict = {
        'esp8266': 'ESP8266',
        'esp32': 'ESP32',
        'esp32s2': 'ESP32-S2',
        'esp32s3': 'ESP32-S3',
        'esp32c3': 'ESP32-C3',
        'esp32h2': 'ESP32-H2',
        'esp8684': 'ESP8684',
    }

    app.add_config_value('idf_target_title_dict', idf_target_title_dict, 'env')


def setup_html_context(app, config):
    # Setup path for 'edit on github'-link
    config.html_context['conf_py_path'] = '/docs/{}/'.format(app.config.language)


def setup_diag_font(app, config):
    # blockdiag and other tools require a font which supports their character set
    # the font file is stored on the download server to save repo size
    font_name = {
        'en': 'DejaVuSans.ttf',
        'zh_CN': 'NotoSansSC-Regular.otf',
    }[app.config.language]

    font_dir = os.path.join(config.config_dir, 'fonts')
    assert os.path.exists(font_dir)

    font_path = os.path.abspath(os.path.join(font_dir, font_name))
    assert os.path.exists(font_path)

    app.config.blockdiag_fontpath = font_path
    app.config.seqdiag_fontpath = font_path
    app.config.actdiag_fontpath = font_path
    app.config.nwdiag_fontpath = font_path
    app.config.rackdiag_fontpath = font_path
    app.config.packetdiag_fontpath = font_path


def setup_html(app, config):
    # Add any paths that contain custom static files (such as style sheets) here,
    # relative to this directory. They are copied after the builtin static files,
    # so a file named "default.css" will overwrite the builtin "default.css".
    esp_docs_static_path = os.path.join(config.config_dir, '_static')
    app.config.html_static_path.append(esp_docs_static_path)

    # The name of an image file (relative to this directory) to place at the top
    # of the sidebar.
    app.config.html_logo = os.path.join(esp_docs_static_path, 'espressif-logo.svg')
from esp_docs.conf_docs import *  # noqa: F403,F401

languages = ['en']

extensions += ['sphinx_copybutton',
               'sphinxcontrib.wavedrom',
               ]

# Disable format_esp_target
extensions.remove('esp_docs.esp_extensions.format_esp_target')

# Use wavedrompy as backend, instead of wavedrom-cli
render_using_wavedrompy = True

# link roles config
github_repo = 'espressif/esp-docs'

# Context used by sphinx_idf_theme
html_context['github_user'] = 'espressif'
html_context['github_repo'] = 'esp-docs'

html_static_path = ['../_static']

# Extra options required by sphinx_idf_theme
project_slug = 'esp-docs'

# Final PDF filename will contains target and version
pdf_file_prefix = u'esp-docs'

linkcheck_exclude_documents = ['index',  # several false positives due to the way we link to different sections
                               ]
# Measurement ID for Google Analytics

google_analytics_id = 'G-F3R0PHFSWL'

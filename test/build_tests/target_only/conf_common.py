from esp_docs.conf_docs import *  # noqa: F403,F401

extensions += [  # Needed as a trigger for running doxygen
               'esp_docs.esp_extensions.dummy_build_system',
               'esp_docs.esp_extensions.run_doxygen',
               ]

languages = ['en', 'zh_CN']

# link roles config
github_repo = 'espressif/esp-docs'

# context used by sphinx_idf_theme
html_context['github_user'] = 'espressif'
html_context['github_repo'] = 'esp-docs'

html_static_path = ['../_static']

# Extra options required by sphinx_idf_theme
project_slug = 'esp-docs'

# Contains info used for constructing target and version selector
# Can also be hosted externally, see esp-idf for example
versions_url = './_static/targets.js'

# Final PDF filename will contains target and version
pdf_file_prefix = u'esp-docs'

idf_targets = ['esp32', 'esp32s2']

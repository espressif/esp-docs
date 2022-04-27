from esp_docs.conf_docs import *  # noqa: F403,F401

languages = ['en']

# link roles config
github_repo = 'espressif/esp-docs'

# context used by sphinx_idf_theme
html_context['github_user'] = 'espressif'
html_context['github_repo'] = 'esp-docs'

# Extra options required by sphinx_idf_theme
project_slug = 'esp-docs'

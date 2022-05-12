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

# Extra options required by sphinx_idf_theme
project_slug = 'esp-docs'

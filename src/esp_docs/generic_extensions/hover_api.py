# Adds hover tooltips for API reference links when esp_hover_api_enable is True


def setup(app):
    app.add_config_value('esp_hover_api_enable', False, 'html')
    app.connect('config-inited', _add_assets)

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.1'}


def _add_assets(app, config):
    if config.esp_hover_api_enable:
        app.add_js_file('hover_api.js')
        app.add_css_file('hover_api.css')

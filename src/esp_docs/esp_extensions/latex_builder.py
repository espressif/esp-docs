import os

from sphinx.builders.latex import LaTeXBuilder


# Overrides the default Sphinx latex build
class IdfLatexBuilder(LaTeXBuilder):

    def __init__(self, app):

        # Sets up the latex_documents config value, done here instead of conf.py since it depends on the runtime value 'idf_target'
        self.init_latex_documents(app)

        super().__init__(app)

    def init_latex_documents(self, app):

        if app.config.pdf_title is None:
            raise ValueError('PDF title not configured, configure the value "pdf_title" in your Sphinx config file to build PDFs')

        if app.config.pdf_file_prefix is None:
            raise ValueError('PDF file name prefix not configured, configure the value "pdf_file_prefix" in your Sphinx config file to build PDFs')

        title = app.config.pdf_title

        if app.config.language == 'zh_CN':
            latex_documents = [('index', app.config.pdf_file + '.tex', title, u'乐鑫信息科技', 'manual')]
        else:
            # Default to english naming
            latex_documents = [('index', app.config.pdf_file + '.tex', title, u'Espressif Systems', 'manual')]

        app.config.latex_documents = latex_documents

    def prepare_latex_macros(self, package_path, config):

        PACKAGE_NAME = 'espidf.sty'
        latex_package = ''
        if config.doc_id is None:
            if config.project_slug == 'esp-idf':
                doc_id = '4287'
            # If doc_id is not provided, leave it empty. Then users can select corresponding Document Title from dropdown list.
            else:
                doc_id = ''
        else:
            doc_id = config.doc_id[config.idf_target]
        doc_language = config.language
        with open(os.path.join(package_path, PACKAGE_NAME), 'r') as template:

            latex_package = template.read()

        idf_target_title = config.idf_target_title_dict.get(config.idf_target, "")
        latex_package = latex_package.replace('<idf_target_title>', idf_target_title)

        # Release name for the PDF front page, remove '_' as this is used for subscript in Latex
        idf_release_name = 'Release {}'.format(config.version.replace('_', '-'))
        latex_package = latex_package.replace('<idf_release_name>', idf_release_name)

        # Retrieve docid and language for feedback link
        latex_package = latex_package.replace('<doc_id>', doc_id)
        # Change doc language from zh_CN to zh-hans which is used in espressif.com
        if doc_language == 'zh_CN':
            doc_language = 'zh-hans'
        latex_package = latex_package.replace('<doc_language>', doc_language)

        with open(os.path.join(self.outdir, PACKAGE_NAME), 'w') as package_file:
            package_file.write(latex_package)

    def finish(self):
        super().finish()

        TEMPLATE_PATH = self.config.latex_template_dir
        self.prepare_latex_macros(TEMPLATE_PATH, self.config)


def config_init_callback(app, config):
    # Keep backwards compatibilty with IDF,
    # which previously didnt specify these configs
    if config.project_slug == 'esp-idf':
        if not config.pdf_file_prefix:
            config.pdf_file_prefix = 'esp-idf'
        if not config.pdf_title:
            config.pdf_title = 'ESP-IDF Programming Guide'

    if config.pdf_file_prefix:
        config.pdf_file = '{}-{}-{}'.format(config.pdf_file_prefix, config.language, config.version)

        if config.idf_target:
            config.pdf_file += '-{}'.format(config.idf_target)


def setup(app):
    app.add_builder(IdfLatexBuilder, override=True)

    app.add_config_value('pdf_file_prefix', None, 'env')
    app.add_config_value('pdf_file', None, 'env')
    app.add_config_value('pdf_title', None, 'env')

    # Config values that depends on target which is not available when setup is called
    app.connect('config-inited',  config_init_callback)

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.1'}

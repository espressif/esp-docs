import shutil
from pathlib import Path

# Extension to create a zip file of the HTML directory
# Filename is decided by config.html_zip
# Output file is placed in the HTML directory


def add_zip(app, exception):
    html_dir = Path(app.outdir)

    if not app.config.html_zip:
        raise RuntimeError('Config value html_zip should be set when using add_html_zip extension')

    zip_output_file = html_dir.parent / app.config.html_zip

    print(f'Creating a zip of the HTML archieve: {html_dir} at {zip_output_file}')
    archive = shutil.make_archive(zip_output_file, 'zip', html_dir)
    shutil.move(archive, html_dir / Path(archive).name)


def setup(app):

    app.connect('build-finished', add_zip)

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.1'}

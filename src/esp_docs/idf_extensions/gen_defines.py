# Sphinx extension to integrate defines into the Sphinx Build
#
# Runs after the IDF dummy project has been built
#
# Then emits the new 'defines-generated' event which has a dictionary of raw text define values
# that other extensions can use to generate relevant data.

import glob
import os
import pprint
import re
import subprocess


def generate_defines(app, project_description):
    sdk_config_path = os.path.join(project_description['build_dir'], 'config')
    compiler = project_description['monitor_toolprefix'] + 'gcc'
    # Parse kconfig macros to pass into doxygen
    #
    # TODO: this should use the set of "config which can't be changed" eventually,
    # not the header
    defines = get_defines(os.path.join(project_description['build_dir'],
                                       'config', 'sdkconfig.h'), sdk_config_path, compiler)

    # Add all SOC _caps.h headers and kconfig macros to the defines
    #
    # kind of a hack, be nicer to add a component info dict in project_description.json
    soc_path = [p for p in project_description['build_component_paths'] if p.endswith('/soc')][0]
    soc_headers = glob.glob(os.path.join(soc_path, project_description['target'],
                                         'include', 'soc', '*_caps.h'))
    assert len(soc_headers) > 0

    rom_path = [p for p in project_description['build_component_paths'] if p.endswith('/esp_rom')][0]
    rom_headers = [os.path.join(rom_path, project_description['target'], 'esp_rom_caps.h')]

    for header in (soc_headers + rom_headers):
        defines.update(get_defines(header, sdk_config_path, compiler))

    # write a list of definitions to make debugging easier
    with open(os.path.join(app.config.build_dir, 'macro-definitions.txt'), 'w') as f:
        pprint.pprint(defines, f)
        print('Saved macro list to %s' % f.name)

    add_tags(app, defines)

    app.emit('defines-generated', defines)
    app.emit('format-esp-target-add-sub', defines)


def get_defines(header_path, sdk_config_path, compiler):
    defines = {}
    # Note: we run C preprocessor here without any -I arguments (except "sdkconfig.h"), so assumption is
    # that these headers are all self-contained and don't include any other headers
    # not in the same directory
    print('Reading macros from %s...' % (header_path))
    processed_output = subprocess.check_output([compiler, '-I', sdk_config_path,
                                                '-dM', '-E', header_path]).decode()
    for line in processed_output.split('\n'):
        line = line.strip()
        m = re.search('#define ([^ ]+) ?(.*)', line)
        if m:
            name = m.group(1)
            value = m.group(2)
            if name.startswith('_'):
                continue  # toolchain macro
            if (' ' in value) or ('=' in value):
                value = ''  # macros that expand to multiple tokens (ie function macros) cause doxygen errors, so just mark as 'defined'
            defines[name] = value

    return defines


def add_tags(app, defines):
    # try to parse define values as ints and add to tags
    for name, value in defines.items():
        try:
            define_value = int(value.strip('()'))
            if define_value > 0:
                app.tags.add(name)
        except ValueError:
            continue


def setup(app):
    app.connect('project-build-info', generate_defines)

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.2'}

# Template Sphinx extension to integrate build system information
# into the Sphinx Build
#
# Runs early in the Sphinx process, runs make/CMake to generate the dummy project
# in this directory - including resolving paths, etc.
#
# Then emits the new 'project-info' event which has information read from
# build system, that other extensions can use to generate relevant data.

def setup(app):
    app.add_event('project-build-info')

    # we want this to run early in the docs build but unclear exactly when
    app.connect('config-inited', generate_build_info)

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.1'}


def generate_build_info(app, config):
    # Run any project specfic build commands here

    # Emit signal with project specific data, can be used as a trigger
    # for various project specific extensions
    # See idf-extensions for examples
    project_description = {}
    app.emit('project-build-info', project_description)

    # Emit signal with a dictionary of defines from the project source
    # e.g. {SOC_BT_SUPPORT: 1}
    # Used both by run_doxygen and exclude_docs
    defines = {}
    app.emit('defines-generated', defines)

    return []

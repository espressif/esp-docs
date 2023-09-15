# Extension to generate Doxygen XML include files, with IDF config & soc macros included
from __future__ import print_function, unicode_literals

import os
import os.path
import re
import subprocess
from io import open
from collections import defaultdict
from dataclasses import dataclass

from ..util.util import copy_if_modified

ALL_KINDS = [
    ('function', 'Functions'),
    ('union', 'Unions'),
    ('struct', 'Structures'),
    ('define', 'Macros'),
    ('typedef', 'Type Definitions'),
    ('enum', 'Enumerations'),
    ('class', 'Classes'),
]
"""list of items that will be generated for a single API file
"""


@dataclass
class ApiPath:
    header_path: str = ''
    api_name: str = ''
    xml_file_path: str = ''
    inc_file_path: str = ''


def setup(app):
    app.add_config_value('run_doxygen_header_edit_callback', None, '')

    # The idf_build_system extension will emit this event once it has generated documentation macro definitions
    app.connect('defines-generated', generate_doxygen)
    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.2'}


# Heuristics for finding the doxygen files, even when user specifies the wrong path
def find_doxygen_dir(doxyfile_dir):
    if os.path.isfile(os.path.join(doxyfile_dir, 'Doxyfile')):
        # Doxyfile found in path specified by user
        return doxyfile_dir
    elif os.path.isfile(os.path.join(doxyfile_dir, 'doxygen', 'Doxyfile')):
        # Doxyfile found in subfolder 'doxygen'
        return os.path.join(doxyfile_dir, 'doxygen')
    else:
        return doxyfile_dir


def generate_doxygen(app, defines):

    build_dir = app.config.build_dir

    # Call Doxygen to get XML files from the header files
    print('Calling Doxygen to generate latest XML files')
    doxy_env = os.environ
    doxy_env.update({
        'ENV_DOXYGEN_DEFINES': ' '.join('{}={}'.format(key, value) for key, value in defines.items()),
        'PROJECT_PATH': app.config.project_path,
        'IDF_TARGET': app.config.idf_target if app.config.idf_target else "",
    })

    doxyfile_dir = find_doxygen_dir(app.config.doxyfile_dir)
    doxyfile_main = os.path.join(doxyfile_dir, 'Doxyfile')

    if not os.path.isfile(doxyfile_main):
        print("No doxyfile found at {}. Either specify directory for Doxyfile with -d or disable the run_doxygen plugin".format(doxyfile_main))
        raise RuntimeError("{} do not exist".format(doxyfile_main))

    doxygen_paths = [doxyfile_main]

    if app.config.idf_target:
        doxyfile_target = os.path.join(doxyfile_dir, 'Doxyfile_' + app.config.idf_target)
        if os.path.isfile(doxyfile_target):
            doxygen_paths.append(doxyfile_target)

    print('Running doxygen with doxyfiles {}'.format(doxygen_paths))

    # It's possible to have doxygen log warnings to a file using WARN_LOGFILE directive,
    # but in some cases it will still log an error to stderr and return success!
    #
    # So take all of stderr and redirect it to a logfile (will contain warnings and errors)
    logfile = os.path.join(build_dir, 'doxygen-warning-log.txt')

    with open(logfile, 'w') as f:
        # note: run Doxygen in the build directory, so the xml & xml_in files end up in there
        subprocess.check_call(['doxygen', doxyfile_main], env=doxy_env, cwd=build_dir, stderr=f)

    # Doxygen has generated XML files in 'xml' directory.
    # Copy them to 'xml_in', only touching the files which have changed.
    copy_if_modified(os.path.join(build_dir, 'xml/'), os.path.join(build_dir, 'xml_in/'))

    # Generate 'api_name.inc' files from the Doxygen XML files
    convert_api_xml_to_inc(app, doxygen_paths)


def get_header_paths(app, doxyfiles, inc_directory_path, xml_directory_path):
    header_paths = [p for d in doxyfiles for p in get_doxyfile_input_paths(app, d)]

    duplicate_dict = defaultdict(list)
    api_path_list = []

    # Detect headers with the same name, as Doxygen threats these differently
    for header_path in header_paths:
        name = get_api_name(header_path)

        if header_path in duplicate_dict[name]:
            # Dont allow identical headers to be added to the Doxyfile
            raise RuntimeError('Doxyfile contains duplicate header: {}'.format(header_path))

        duplicate_dict[name].append(header_path)

    for header_path in header_paths:
        api_path = ApiPath()

        api_path.api_name = get_api_name(header_path)
        api_path.header_path = header_path

        # If header name is unique then the file name is simply the header name
        if len(duplicate_dict[api_path.api_name]) == 1:
            api_path.xml_file_path = header_to_xml_path(api_path.api_name, xml_directory_path)
            api_path.inc_file_path = os.path.join(inc_directory_path, os.path.splitext(api_path.api_name)[0] + '.inc')
        # If not unique then doxygen will use the shortest unique path as the file name
        else:
            common_path = os.path.commonpath(duplicate_dict[api_path.api_name])
            shortest_unique_path = os.path.relpath(header_path, common_path)
            api_path.xml_file_path = header_to_xml_path(shortest_unique_path, xml_directory_path)
            # For non-unique header names include path will be the full header path
            api_path.inc_file_path = os.path.join(inc_directory_path, os.path.splitext(header_path)[0] + '.inc')

        api_path_list.append(api_path)

    return api_path_list


def convert_api_xml_to_inc(app, doxyfiles):
    """ Generate header_file.inc files
    with API reference made of doxygen directives
    for each header file
    specified in the 'INPUT' statement of the Doxyfile.
    """
    build_dir = app.config.build_dir

    xml_directory_path = '{}/xml'.format(build_dir)
    inc_directory_path = '{}/inc'.format(build_dir)

    fast_build = os.environ.get('DOCS_FAST_BUILD', None)

    if not os.path.isdir(xml_directory_path):
        raise RuntimeError('Directory {} does not exist!'.format(xml_directory_path))

    if not os.path.exists(inc_directory_path):
        os.makedirs(inc_directory_path)

    api_paths = get_header_paths(app, doxyfiles, inc_directory_path, xml_directory_path)

    print("Generating 'api_name.inc' files with Doxygen directives")
    for api_path in api_paths:
        rst_output = generate_directives(app, api_path.header_path, api_path.xml_file_path)

        # Create subfolders if needed
        dir_name = os.path.dirname(api_path.inc_file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        previous_rst_output = ''
        if os.path.isfile(api_path.inc_file_path):
            with open(api_path.inc_file_path, 'r', encoding='utf-8') as inc_file_old:
                previous_rst_output = inc_file_old.read()

        if previous_rst_output != rst_output:
            with open(api_path.inc_file_path, 'w', encoding='utf-8') as inc_file:
                inc_file.write(rst_output)

        # For fast builds we wipe the doxygen api documention.
        # Parsing this output during the sphinx build process is
        # what takes 95% of the build time
        if fast_build:
            with open(api_path.inc_file_path, 'w', encoding='utf-8') as inc_file:
                inc_file.write('')


def get_doxyfile_input_paths(app, doxyfile_path):
    """Get contents of Doxyfile's INPUT statement.

    Returns:
        Contents of Doxyfile's INPUT.

    """
    if not os.path.isfile(doxyfile_path):
        raise RuntimeError("Doxyfile '{}' does not exist!".format(doxyfile_path))

    print("Getting Doxyfile's INPUT from {}".format(doxyfile_path))

    with open(doxyfile_path, 'r', encoding='utf-8') as input_file:
        line = input_file.readline()
        # read contents of Doxyfile until 'INPUT' statement
        while line:
            if line.find('INPUT') == 0:
                break
            line = input_file.readline()

        doxyfile_INPUT = []
        line = input_file.readline()
        # skip input_file contents until end of 'INPUT' statement
        while line:
            if line.isspace():
                # we have reached the end of 'INPUT' statement
                break
            # process only lines that are not comments
            if line.find('#') == -1:
                # extract header file path inside project folder
                m = re.search('\(PROJECT_PATH\)/(.*\.hp*)', line)  # noqa: W605 - regular expression
                if m is None:
                    raise ValueError("Doxygen input statements should be specified using $(PROJECT_PATH) env variable, instead got {}".format(line))
                header_file_path = m.group(1)
                # Replace env variable used for multi target header
                if app.config.idf_target:
                    header_file_path = header_file_path.replace('$(IDF_TARGET)', app.config.idf_target)

                doxyfile_INPUT.append(header_file_path)

            # proceed reading next line
            line = input_file.readline()
    return doxyfile_INPUT


def get_api_name(header_file_path):
    """Get name of API and extension from header file path.

    Args:
        header_file_path: path to the header file.

    Returns:
        API name with the file extension

    """
    regex = r'.*/(.*)\.(hp*)'
    m = re.search(regex, header_file_path)
    if m:
        return m.group(1) + "." + m.group(2)

    return ''


def header_to_xml_path(header_file, xml_directory_path):
    # in XLT file name each "_" in the api name is expanded by Doxygen to "__"
    xlt_api_name = header_file.replace('_', '__')
    # in XLT file name each "/" in the api name is expanded by Doxygen to "_2"
    xlt_api_name = xlt_api_name.replace('/', '_2')
    xlt_api_name, ext = os.path.splitext(xlt_api_name)

    xml_file_path = '%s/%s_8%s.xml' % (xml_directory_path, xlt_api_name, ext[1:])  # extension without "."
    return xml_file_path


def generate_directives(app, header_file_path, xml_file_path):
    """Generate API reference with Doxygen directives for a header file.

    Args:
        header_file_path: a path to the header file with API.

    Returns:
        Doxygen directives for the header file.

    """

    rst_output = ''
    rst_output = ".. File automatically generated by 'gen-dxd.py'\n"
    rst_output += '\n'
    rst_output += get_rst_header('Header File')
    rst_output += '* :project_file:`' + header_file_path + '`\n'
    rst_output += '\n'

    if (app.config.run_doxygen_header_edit_callback):
        rst_output = app.config.run_doxygen_header_edit_callback(rst_output, header_file_path)

    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET

    tree = ET.ElementTree(file=xml_file_path)
    for kind, label in ALL_KINDS:
        rst_output += get_directives(tree, kind)

    return rst_output


def get_rst_header(header_name):
    """Get rst formatted code with a header.

    Args:
        header_name: name of header.

    Returns:
        Formatted rst code with the header.

    """

    rst_output = ''
    rst_output += header_name + '\n'
    rst_output += '^' * len(header_name) + '\n'
    rst_output += '\n'

    return rst_output


def select_container(innerclass_list, container):
    """Select container (struct, union, class) type from innerclass list.

    Args:
        innerclass_list: raw list with structs, unions or classes
                         extracted from Dogygen's xml file.

    Returns:
        Doxygen directives with containers (structs, unions, classes) selected from the list.
        Note: some structs are excluded as described on code below.

    """

    rst_output = ''
    for line in innerclass_list.splitlines():
        # container is denoted by the keyword "struct", "union" or "class" at the beginning of line
        if line.startswith(container):
            # skip structures that are part of union
            # they are documented by 'doxygenunion' directive
            if container == "struct" and line.find('::') > 0:
                continue
            _, name = re.split(r'\t+', line)

            rst_output += '.. doxygen%s:: ' % (container)
            rst_output += name
            rst_output += '\n'
            if container in ["struct", "class"]:
                rst_output += '    :members:\n'
                rst_output += '\n'

    return rst_output


def get_directives(tree, kind):
    """Get directives for specific 'kind'.

    Args:
        tree: the ElementTree 'tree' of XML by Doxygen
        kind: name of API "kind" to be generated

    Returns:
        Doxygen directives for selected 'kind'.
        Note: the header with "kind" name is included.

    """

    rst_output = ''
    if kind in ['union', 'struct', 'class']:
        innerclass_list = ''
        for elem in tree.iterfind('compounddef/innerclass'):
            innerclass_list += elem.attrib['refid'] + '\t' + elem.text + '\n'
        rst_output += select_container(innerclass_list, kind)
    else:
        for elem in tree.iterfind(
                'compounddef/sectiondef/memberdef[@kind="%s"]' % kind):
            name = elem.find('name')

            if name.text:
                rst_output += '.. doxygen%s:: ' % kind
                rst_output += name.text + '\n'

    if rst_output:
        all_kinds_dict = dict(ALL_KINDS)
        rst_output = get_rst_header(all_kinds_dict[kind]) + rst_output + '\n'

    return rst_output

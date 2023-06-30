#!/usr/bin/env python3
# coding=utf-8
#
# Top-level docs builder
#
# This is just a front-end to sphinx-build that can call it multiple times for different language/target combinations
#
# Will build out to _build/LANG/TARGET by default
#
# Specific custom docs functionality should be added in conf_common.py or in a Sphinx extension, not here.
#
# Copyright 2020 Espressif Systems (Shanghai) PTE LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import print_function

import argparse
import locale
import math
import multiprocessing
import os
import os.path
import re
import subprocess
import sys
from .check_docs import check_docs
import pkg_resources


LANGUAGES = ['en', 'zh_CN']
TARGETS = ['esp8266', 'esp32', 'esp32s2', 'esp32s3', 'esp32c3',  'esp32h2', 'esp32c2', 'esp32c6']

SPHINX_WARN_LOG = 'sphinx-warning-log.txt'
SPHINX_SANITIZED_LOG = 'sphinx-warning-log-sanitized.txt'
SPHINX_KNOWN_WARNINGS = 'sphinx-known-warnings.txt'


DXG_WARN_LOG = 'doxygen-warning-log.txt'
DXG_SANITIZED_LOG = 'doxygen-warning-log-sanitized.txt'
DXG_KNOWN_WARNINGS = 'doxygen-known-warnings.txt'


languages = LANGUAGES
targets = TARGETS


def check_python_requirements(requirements_path):
    try:
        with open(requirements_path) as f:
            not_satisfied = []

            for line in f:
                line = line.strip()
                # pkg_resources.require() cannot handle the full requirements file syntax so we need to make
                # adjustments for options which we use.
                if line.startswith('file://'):
                    line = os.path.basename(line)
                if line.startswith('-e') and '#egg=' in line:  # version control URLs, take the egg= part at the end only
                    line = re.search(r'#egg=([^\s]+)', line).group(1)
                try:
                    pkg_resources.require(line)
                except Exception:
                    not_satisfied.append(line)

            if len(not_satisfied) > 0:
                print('The following Python requirements from the current directory\'s requirements.txt are not satisfied:')
                for requirement in not_satisfied:
                    print(requirement)
                print('This check can be skipped by running with --skip-reqs-check')
                sys.exit(1)

    except FileNotFoundError:
        # If there isnt any requirements.txt in the current directory then we just skip the check
        pass


def main():
    # This is not the only way to make sure that all files opened by Python are treated as UTF-8, but the other way is passing encoding='utf-8' to all open()
    # functions and this way makes Python 2 compatibility really tough if there is any code that assumes text files contain strings (kconfiglib assumes this).
    # The reason for that is that you need to import io.open() to support the encoding argument on Python 2, and this function always uses Py2's unicode
    # type not the str type.
    if ('UTF-8' not in locale.getlocale()) and ('utf8' not in locale.getlocale()):
        raise RuntimeError("build_docs.py requires the default locale's encoding to be UTF-8.\n" +
                           ' - Linux. Setting environment variable LC_ALL=C.UTF-8 when running build_docs.py may be ' +
                           'enough to fix this.\n'
                           ' - Windows. Possible solution for the Windows 10 starting version 1803. Go to ' +
                           'Control Panel->Clock and Region->Region->Administrative->Change system locale...; ' +
                           'Check `Beta: Use Unicode UTF-8 for worldwide language support` and reboot')

    parser = argparse.ArgumentParser(description='build_docs.py: Build espressif docs', prog='build_docs.py')

    common_args = argparse.ArgumentParser(add_help=False)
    common_args.add_argument('--language', '-l', choices=LANGUAGES, required=False)
    common_args.add_argument('--target', '-t', choices=TARGETS, nargs='+', required=True)
    common_args.add_argument('--project-path', '-pp', type=str, default='../',
                        help='Path to project we are building docs for')
    common_args.add_argument('--build-dir', '-b', type=str, default='_build')
    common_args.add_argument('--source-dir', '-s', type=str, default='')
    common_args.add_argument('--doxyfile_dir', '-d', type=str, default='.')
    common_args.add_argument('--builders', '-bs', nargs='+', type=str, default=['html'],
                        help='List of builders for Sphinx, e.g. html or latex, for latex a PDF is also generated')
    common_args.add_argument('--sphinx-parallel-builds', '-p', choices=['auto'] + [str(x) for x in range(8)],
                        help='Parallel Sphinx builds - number of independent Sphinx builds to run', default='auto')
    common_args.add_argument('--sphinx-parallel-jobs', '-j', choices=['auto'] + [str(x) for x in range(8)],
                        help='Sphinx parallel jobs argument - number of threads for each Sphinx build to use', default='1')
    common_args.add_argument('--input-docs', '-i', nargs='+', default=[''],
                        help='List of documents to build relative to the doc base folder, i.e. the language folder. Defaults to all documents')
    common_args.add_argument('--fast-build', '-f', action='store_true', help='Skips including doxygen generated APIs into the Sphinx build')
    common_args.add_argument('--skip-reqs-check', action='store_true', help='Skips checking python requirements.txt found in the current directory')

    action_parsers = parser.add_subparsers(dest='action')

    build_parser = action_parsers.add_parser('build', parents=[common_args], help='Build documentation')
    build_parser.add_argument('--check-warnings-only', '-w', action='store_true')

    action_parsers.add_parser('linkcheck', parents=[common_args], help='Check links (a current IDF revision should be uploaded to GitHub)')

    action_parsers.add_parser('gh-linkcheck', parents=[common_args], help='Checking for hardcoded GitHub links')

    args = parser.parse_args()

    if not args.skip_reqs_check:
        check_python_requirements('requirements.txt')

    global languages
    if args.language is None:
        print('Building all languages')
        languages = LANGUAGES
    else:
        languages = [args.language]

    global targets
    if args.target is None:
        print('Building without a target')
        targets = ['generic']
    else:
        targets = args.target

    if args.fast_build:
        os.environ['DOCS_FAST_BUILD'] = 'y'

    if args.action == 'build' or args.action is None:
        if args.action is None:
            args.check_warnings_only = False

        sys.exit(action_build(args))

    if args.action == 'linkcheck':
        sys.exit(action_linkcheck(args))

    if args.action == 'gh-linkcheck':
        sys.exit(action_gh_linkcheck(args))


def parallel_call(args, callback):
    num_sphinx_builds = len(languages) * len(targets)
    num_cpus = multiprocessing.cpu_count()

    if args.sphinx_parallel_builds == 'auto':
        # at most one sphinx build per CPU, up to the number of CPUs
        args.sphinx_parallel_builds = min(num_sphinx_builds, num_cpus)
    else:
        args.sphinx_parallel_builds = int(args.sphinx_parallel_builds)

    # Force -j1 because sphinx works incorrectly
    args.sphinx_parallel_jobs = 1
    if args.sphinx_parallel_jobs == 'auto':
        # N CPUs per build job, rounded up - (maybe smarter to round down to avoid contention, idk)
        args.sphinx_parallel_jobs = int(math.ceil(num_cpus / args.sphinx_parallel_builds))
    else:
        args.sphinx_parallel_jobs = int(args.sphinx_parallel_jobs)

    print('Will use %d parallel builds and %d jobs per build' % (args.sphinx_parallel_builds, args.sphinx_parallel_jobs))
    pool = multiprocessing.Pool(args.sphinx_parallel_builds)

    if args.sphinx_parallel_jobs > 1:
        print('WARNING: Sphinx parallel jobs currently produce incorrect docs output with Sphinx 1.8.5')

    # make a list of all combinations of build_docs() args as tuples
    #
    # there's probably a fancy way to do this with itertools but this way is actually readable

    entries = []
    for target in targets:
        for language in languages:
            build_info = {}
            build_info['build_dir'] = os.path.realpath(os.path.join(args.build_dir, language, target))
            build_info['source_dir'] = os.path.realpath(os.path.join(args.source_dir, language))

            build_info['language'] = language
            build_info['target'] = target
            build_info['sphinx_parallel_jobs'] = args.sphinx_parallel_jobs
            build_info['builders'] = args.builders
            build_info['input_docs'] = args.input_docs
            build_info['doxyfile_dir'] = args.doxyfile_dir
            build_info['project_path'] = args.project_path

            entries.append(build_info)

    print(entries)
    errcodes = pool.map(callback, entries)
    print(errcodes)

    is_error = False
    for ret in errcodes:
        if ret != 0:
            print('\nThe following language/target combinations failed to build:')
            is_error = True
            break
    if is_error:
        for ret, build_info in zip(errcodes, entries):
            if ret != 0:
                print('language: %s, target: %s, errcode: %d' % (build_info['language'], build_info['target'], ret))
        # Don't re-throw real error code from each parallel process
        return 1
    else:
        return 0


def sphinx_call(build_info, builder):
    # Note: because this runs in a multiprocessing Process, everything which happens here should be isolated to a single process
    # (ie it doesn't matter if Sphinx is using global variables, as they're it's own copy of the global variables)

    # wrap stdout & stderr in a way that lets us see which build_docs instance they come from
    #
    # this doesn't apply to subprocesses, they write to OS stdout & stderr so no prefix appears
    prefix = '%s/%s: ' % (build_info['language'], build_info['target'])

    print('Building in build_dir: %s' % (build_info['build_dir']))
    try:
        os.makedirs(build_info['build_dir'])
    except OSError:
        pass

    environ = {}
    environ.update(os.environ)
    environ['BUILDDIR'] = build_info['build_dir']

    args = [sys.executable, '-u', '-m', 'sphinx.cmd.build',
            '-j', str(build_info['sphinx_parallel_jobs']),
            '-b', builder,
            '-d', os.path.join(build_info['build_dir'], 'doctrees'),
            '-w', SPHINX_WARN_LOG
            ]

    if build_info['target'] != 'generic':
        args += ['-t', build_info['target'], '-D', 'idf_target={}'.format(build_info['target'])]

    args += ['-D', 'docs_to_build={}'.format(','. join(build_info['input_docs'])),
             '-D', 'config_dir={}'.format(os.path.abspath(os.path.dirname(__file__))),
             '-D', 'doxyfile_dir={}'.format(os.path.abspath(build_info['doxyfile_dir'])),
             '-D', 'project_path={}'.format(os.path.abspath(build_info['project_path'])),
             build_info['source_dir'],
             os.path.join(build_info['build_dir'], builder)                    # build directory
             ]

    saved_cwd = os.getcwd()
    os.chdir(build_info['build_dir'])  # also run sphinx in the build directory
    print("Running '%s'" % (' '.join(args)))

    ret = 1
    try:
        # Note: we can't call sphinx.cmd.build.main() here as multiprocessing doesn't est >1 layer deep
        # and sphinx.cmd.build() also does a lot of work in the calling thread, especially for j ==1,
        # so using a Pyhthon thread for this part is  a poor option (GIL)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=environ)
        for c in iter(lambda: p.stdout.readline(), b''):
            sys.stdout.write(prefix)
            sys.stdout.write(c.decode('utf-8'))
        ret = p.wait()
        assert (ret is not None)
        sys.stdout.flush()
    except KeyboardInterrupt:  # this seems to be the only way to get Ctrl-C to kill everything?
        p.kill()
        os.chdir(saved_cwd)
        return 130  # FIXME It doesn't return this errorcode, why? Just prints stacktrace
    os.chdir(saved_cwd)
    return ret


def action_build(args):
    if not args.check_warnings_only:
        ret = parallel_call(args, call_build_docs)
        if ret != 0:
            return ret


def call_build_docs(build_info):

    for buildername in build_info['builders']:
        ret = sphinx_call(build_info, buildername)

        # Warnings are checked after each builder as logs are overwritten
        # check Doxygen warnings only if we actually have a doxyfile:
        def has_doxyfile(doxyfile_dir):
            if os.path.isfile(os.path.join(doxyfile_dir, 'Doxyfile')):
                return True
            elif os.path.isfile(os.path.join('doxygen', 'Doxyfile')):  # kept for backwards compatibility
                return True
            else:
                return False

        if has_doxyfile(build_info['doxyfile_dir']):
            ret += check_docs(build_info['language'], build_info['target'],
                              log_file=os.path.join(build_info['build_dir'], DXG_WARN_LOG),
                              known_warnings_file=DXG_KNOWN_WARNINGS,
                              out_sanitized_log_file=os.path.join(build_info['build_dir'], DXG_SANITIZED_LOG))
        else:
            print('No Doxyfile found, skipping check of doxygen errors')

        # check Sphinx warnings:
        ret += check_docs(build_info['language'], build_info['target'],
                          log_file=os.path.join(build_info['build_dir'], SPHINX_WARN_LOG),
                          known_warnings_file=SPHINX_KNOWN_WARNINGS,
                          out_sanitized_log_file=os.path.join(build_info['build_dir'], SPHINX_SANITIZED_LOG))

        if ret != 0:
            return ret

    # Build PDF from tex
    if 'latex' in build_info['builders']:
        latex_dir = os.path.join(build_info['build_dir'], 'latex')
        ret = build_pdf(build_info['language'], build_info['target'], latex_dir)

    return ret


def build_pdf(language, target, latex_dir):
    # Note: because this runs in a multiprocessing Process, everything which happens here should be isolated to a single process

    # wrap stdout & stderr in a way that lets us see which build_docs instance they come from
    #
    # this doesn't apply to subprocesses, they write to OS stdout & stderr so no prefix appears
    prefix = '%s/%s: ' % (language, target)

    print('Building PDF in latex_dir: %s' % (latex_dir))

    saved_cwd = os.getcwd()
    os.chdir(latex_dir)

    # Based on read the docs PDFBuilder
    rcfile = 'latexmkrc'

    cmd = [
        'latexmk',
        '-r',
        rcfile,
        '-pdf',
        # When ``-f`` is used, latexmk will continue building if it
        # encounters errors. We still receive a failure exit code in this
        # case, but the correct steps should run.
        '-f',
        '-dvi-',    # dont generate dvi
        '-ps-',     # dont generate ps
        '-interaction=nonstopmode',
        '-quiet',
        '-outdir=build',
    ]

    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for c in iter(lambda: p.stdout.readline(), b''):
            sys.stdout.write(prefix)
            sys.stdout.write(c.decode('utf-8'))
        ret = p.wait()
        assert (ret is not None)
        sys.stdout.flush()
    except KeyboardInterrupt:  # this seems to be the only way to get Ctrl-C to kill everything?
        p.kill()
        os.chdir(saved_cwd)
        return 130  # FIXME It doesn't return this errorcode, why? Just prints stacktrace
    os.chdir(saved_cwd)

    return ret


def action_linkcheck(args):
    return parallel_call(args, call_linkcheck)


def call_linkcheck(build_info):
    return sphinx_call(build_info, 'linkcheck')


# https://github.com/espressif/esp-idf/tree/
# https://github.com/espressif/esp-idf/blob/
# https://github.com/espressif/esp-idf/raw/
GH_LINK_RE = r'https://github.com/espressif/esp-idf/(?:tree|blob|raw)/[^\s]+'

# we allow this one doc, because we always want users to see the latest support policy
GH_LINK_ALLOWED = ['https://github.com/espressif/esp-idf/blob/master/SUPPORT_POLICY.md',
                   'https://github.com/espressif/esp-idf/blob/master/SUPPORT_POLICY_CN.md']


def action_gh_linkcheck(args):
    print('Checking for hardcoded GitHub links\n')

    github_links = []

    docs_dir = os.path.relpath(os.path.dirname(__file__))
    for root, _, files in os.walk(docs_dir):
        if '_build' in root:
            continue
        files = [os.path.join(root, f) for f in files if f.endswith('.rst')]
        for path in files:
            with open(path, 'r') as f:
                for link in re.findall(GH_LINK_RE, f.read()):
                    if link not in GH_LINK_ALLOWED:
                        github_links.append((path, link))

    if github_links:
        for path, link in github_links:
            print('%s: %s' % (path, link))
        print('WARNING: Some .rst files contain hardcoded Github links.')
        print('Please check above output and replace links with one of the following:')
        print('- :idf:`dir` - points to directory inside ESP-IDF')
        print('- :idf_file:`file` - points to file inside ESP-IDF')
        print('- :idf_raw:`file` - points to raw view of the file inside ESP-IDF')
        print('- :component:`dir` - points to directory inside ESP-IDF components dir')
        print('- :component_file:`file` - points to file inside ESP-IDF components dir')
        print('- :component_raw:`file` - points to raw view of the file inside ESP-IDF components dir')
        print('- :example:`dir` - points to directory inside ESP-IDF examples dir')
        print('- :example_file:`file` - points to file inside ESP-IDF examples dir')
        print('- :example_raw:`file` - points to raw view of the file inside ESP-IDF examples dir')
        print('These link types will point to the correct GitHub version automatically')
        return 1
    else:
        print('No hardcoded links found')
        return 0


if __name__ == '__main__':
    main()

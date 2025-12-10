#!/usr/bin/env python3
#
# CI script to deploy docs to a webserver. Not useful outside of CI environment
#
#
# Copyright 2025 Espressif Systems (Shanghai) PTE LTD
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
"""Upload built documentation artifacts to an S3-compatible bucket.

This module is intended to run in CI.

How it works
1. Reads the git version string from `GIT_VER` (typically `git describe --always`) and
   converts it into a deployable version via `sanitize_version`.
2. Collects documentation artifacts under `DOCS_BUILD_DIR`:
   - HTML: all directories matching `**/html/`
   - PDFs: all files matching `**/latex/build/*.pdf`
3. Copies artifacts into a temporary staging directory at `DOCS_BUILD_DIR/tmp_deploy`
   using the deployed layout:
   - `language/<version>/<target>/...` (the `<target>` component is omitted when the
     target name is `generic`)
4. Uploads the staged directory to S3 under the prefix:
   - `<CI_COMMIT_SHA>/<DOCS_S3_DEPLOY_PATH>/...`
   This commit-scoped prefix is used as a staging location.
5. If `DEPLOY_STABLE` is set (to a truthy value) and `is_stable_version(version)` is
   true, repeats the staging+upload step using `<version> = stable`.

Required environment variables
- `DOCS_S3_ACCESS_KEY_ID`: S3 access key.
- `DOCS_S3_SECRET_ACCESS_KEY`: S3 secret key.
- `DOCS_S3_BUCKET_NAME`: Destination bucket (typically the staging bucket in CI).
- `DOCS_S3_ENDPOINT`: S3 endpoint URL.
- `DOCS_S3_DEPLOY_PATH`: Remote base path (for example: `/project/<project-name>`).
- `GIT_VER`: Git version string to derive the deploy version from.
- `DOCS_BUILD_DIR`: Local directory where docs have already been built.
- `CI_COMMIT_SHA`: Commit SHA used to namespace uploads in the staging prefix.

Optional environment variables
- `DEPLOY_STABLE`: If set and the derived version is stable, also deploy under
  `language/stable/...`.
"""

import glob
import mimetypes
import os
import os.path
import shutil

import boto3
from botocore.config import Config

from .util.util import is_stable_version, env
from .sanitize_version import sanitize_version  # noqa


class S3Config:
    alias = 'deploy-docs-s3'
    access_key: str = env('DOCS_S3_ACCESS_KEY_ID')
    secret_key: str = env('DOCS_S3_SECRET_ACCESS_KEY')
    bucket_name: str = env('DOCS_S3_BUCKET_NAME')
    endpoint: str = env('DOCS_S3_ENDPOINT')
    docs_path: str = env('DOCS_S3_DEPLOY_PATH')  # /project/{project-name}

    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint,
        config=Config(s3={'addressing_style': 'path'}),
    )


def main():
    # if you get KeyErrors on the following lines, it's probably because you're not running in Gitlab CI
    git_ver = env('GIT_VER')  # output of git describe --always
    version = sanitize_version(
        git_ver
    )  # branch or tag we're building for (used for 'release' & URL)
    print(f'Git version: {git_ver}')
    print(f'Deployment version: {version}')

    if not version:
        raise RuntimeError('A version is needed to deploy')

    build_dir = env(
        'DOCS_BUILD_DIR'
    )  # top-level local build dir, where docs have already been built

    commit_sha = env('CI_COMMIT_SHA')
    docs_path = f'{commit_sha}/{S3Config.docs_path}'

    tmp_path = copy_docs_to_tmp_folder(version, build_dir)
    upload(tmp_path, docs_path)

    # note: it would be neater to use symlinks for stable, but because of the directory order
    # (language first) it's kind of a pain to do on a remote server, so we just repeat the
    # process but call the version 'stable' this time
    do_deploy_stable = os.getenv('DEPLOY_STABLE')
    if is_stable_version(version) and do_deploy_stable:
        print('Deploying again as stable version...')
        tmp_path = copy_docs_to_tmp_folder('stable', build_dir)
        upload(tmp_path, docs_path)


def _upload_one(local_path, key_name):
    content_type, encoding = mimetypes.guess_type(local_path)

    extra_args = {}
    if content_type:
        extra_args['ContentType'] = content_type

    S3Config.s3.upload_file(
        local_path,
        S3Config.bucket_name,
        key_name,
        ExtraArgs=extra_args if extra_args else None,
    )


def upload(source_dir, remote_dir):
    prefix = remote_dir.strip('/')
    for root, _, files in os.walk(source_dir):
        for filename in files:
            local_path = str(os.path.join(root, filename))
            rel_path = os.path.relpath(local_path, source_dir).replace(os.sep, '/')
            key_name = f'{prefix}/{rel_path}'
            _upload_one(local_path, key_name)


def copy_docs_to_tmp_folder(version, build_dir):
    """Copy all docs to a tmp folder, maintaining the directory structure used to deploy as
    the given version"""

    # Create a tmp folder in the build_dir
    tmp_folder = os.path.join(build_dir, 'tmp_deploy')

    # Remove tmp folder if it already exists
    if os.path.exists(tmp_folder):
        shutil.rmtree(tmp_folder)

    # Create the tmp folder
    os.makedirs(tmp_folder)
    print(f'Created tmp folder at: {tmp_folder}')

    # find all the 'html/' directories under build_dir
    html_dirs = glob.glob(f'{build_dir}/**/html/', recursive=True)
    print('Found %d html directories' % len(html_dirs))

    pdfs = glob.glob(f'{build_dir}/**/latex/build/*.pdf', recursive=True)
    print('Found %d PDFs in latex directories' % len(pdfs))

    def should_skip_sources(src, names):
        """Filter to skip _sources directories during copy"""
        return ['_sources'] if '_sources' in names else []

    for html_dir in html_dirs:
        # html_dir has the form '<ignored>/<language>/<target>/html/'
        target_dirname = os.path.dirname(os.path.dirname(html_dir))
        target = os.path.basename(target_dirname)
        language = os.path.basename(os.path.dirname(target_dirname))

        # when deploying, we want the top-level directory layout 'language/version/target'
        dest_path = os.path.join(tmp_folder, language, version)

        if target != 'generic':
            dest_path = os.path.join(dest_path, target)

        print(f"Copying '{html_dir}' to '{dest_path}'...")

        # Copy the html directory to the destination, excluding _sources
        shutil.copytree(
            html_dir, dest_path, ignore=should_skip_sources, dirs_exist_ok=True
        )

    for pdf_path in pdfs:
        # pdf_path has the form '<ignored>/<language>/<target>/latex/build'
        latex_dirname = os.path.dirname(pdf_path)
        pdf_filename = os.path.basename(pdf_path)
        target_dirname = os.path.dirname(os.path.dirname(latex_dirname))
        target = os.path.basename(target_dirname)
        language = os.path.basename(os.path.dirname(target_dirname))

        # when deploying, we want the layout 'language/version/target/pdf'
        dest_path = os.path.join(tmp_folder, language, version)

        if target != 'generic':
            dest_path = os.path.join(dest_path, target)

        # Create the destination directory if it doesn't exist
        os.makedirs(dest_path, exist_ok=True)

        dest_file = os.path.join(dest_path, pdf_filename)

        print(f"Copying '{pdf_path}' to '{dest_file}'...")
        shutil.copy2(pdf_path, dest_file)

    return os.path.abspath(tmp_folder)


if __name__ == '__main__':
    main()

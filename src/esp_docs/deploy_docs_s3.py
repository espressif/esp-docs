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
"""Promote previously uploaded docs from a staging S3 bucket to production.

This module is intended to run in CI after `upload_docs_s3.py` has uploaded docs to a
commit-scoped staging prefix.

How it works
1. Reads `CI_COMMIT_SHA` and constructs a staging prefix:
   - `<CI_COMMIT_SHA>/<DOCS_S3_DEPLOY_PATH>/...`
2. Lists all objects under that prefix in the staging bucket.
3. Copies each object to the production bucket under the final prefix:
   - `<DOCS_S3_DEPLOY_PATH>/...`

Required environment variables
- `DOCS_S3_ACCESS_KEY_ID`: S3 access key.
- `DOCS_S3_SECRET_ACCESS_KEY`: S3 secret key.
- `DOCS_S3_ENDPOINT`: S3 endpoint URL.
- `DOCS_S3_STAGING_BUCKET_NAME`: Bucket holding commit-scoped uploads.
- `DOCS_S3_PRODUCTION_BUCKET_NAME`: Bucket used to serve docs.
- `DOCS_S3_DEPLOY_PATH`: Remote base path (for example: `/project/<project-name>`).
- `CI_COMMIT_SHA`: Commit SHA used to locate the staged objects.
"""

import boto3
from botocore.config import Config

from .sanitize_version import sanitize_version  # noqa
from .util.util import env


class S3Config:
    alias = 'deploy-docs-s3'
    access_key: str = env('DOCS_S3_ACCESS_KEY_ID')
    secret_key: str = env('DOCS_S3_SECRET_ACCESS_KEY')
    stage_bucket_name: str = env('DOCS_S3_STAGING_BUCKET_NAME')
    prod_bucket_name: str = env('DOCS_S3_PRODUCTION_BUCKET_NAME')
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
    commit_sha = env('CI_COMMIT_SHA')
    mv(commit_sha)


def _mv_one(key_name, new_key_name):
    S3Config.s3.copy_object(
        Bucket=S3Config.prod_bucket_name,
        Key=new_key_name,
        CopySource={'Bucket': S3Config.stage_bucket_name, 'Key': key_name},
    )


def mv(commit_sha):
    from_prefix = f'{commit_sha}/{S3Config.docs_path}'.strip('/')
    to_prefix = S3Config.docs_path.strip('/')

    paginator = S3Config.s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(
        Bucket=S3Config.stage_bucket_name, Prefix=from_prefix
    ):
        for obj in page.get('Contents', []):
            key_name = obj['Key']

            # Skip S3 folder markers
            if key_name.endswith('/'):
                continue

            suffix = key_name[len(from_prefix):].lstrip('/')
            new_key_name = f'{to_prefix}/{suffix}' if to_prefix else suffix
            _mv_one(key_name, new_key_name)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# coding=utf-8
#
# Deploy esp_docs package to PyPI
#
# Copyright 2021 Espressif Systems (Shanghai) PTE LTD
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

import subprocess
import os
import json
import urllib.request
from pathlib import Path
from distutils.version import StrictVersion

PROJECT_DIR = Path(os.environ["ESP_DOCS_PATH"])


def get_pypi_dist_version():
    url = "https://pypi.python.org/pypi/esp_docs/json"

    with urllib.request.urlopen(url, timeout=30) as conn:
        data = json.loads(conn.read().decode("utf-8"))

    versions = list(data["releases"].keys())

    versions.sort(key=StrictVersion)
    return StrictVersion(versions[-1])


def get_local_dist_version():
    setup_py_path = PROJECT_DIR / "setup.py"
    ret = subprocess.run(["python3", str(setup_py_path), "--version"], stdout=subprocess.PIPE, check=True, timeout=100)

    return StrictVersion(ret.stdout.decode("utf-8"))


def pypi_dist_is_outdated():
    local_dist_version = get_local_dist_version()
    pydist_dist_version = get_pypi_dist_version()

    print("Local version: {}, PyPI version: {}".format(local_dist_version, pydist_dist_version))

    return local_dist_version > pydist_dist_version


def deploy_dist():
    print("Deploying to PyPI...")
    try:
        subprocess.run(["twine", "upload", "dist/*"], stdout=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise


def main():
    if pypi_dist_is_outdated():
        deploy_dist()
    else:
        print("PyPI version up to date, no need to deploy")


if __name__ == "__main__":
    main()

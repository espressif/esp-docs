#!/usr/bin/env python3

import os
import unittest
import tempfile
import tarfile

from distutils.dir_util import copy_tree
from string import Template
from esp_docs.deploy_docs import build_doc_tarball


class TestBuildTarball(unittest.TestCase):
    BUILD_DIR_TEMPLATE_PATH = '_build_deploy'
    PDF_NAME_TEMPLATE = Template('esp-idf-$lang-$ver-esp32.pdf')
    VERSION = 'v5.1-dev-50-g790aa40c38'

    LANGUAGES = ['en', 'zh_CN']

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        # Get the absolute path to the _build_deploy directory relative to this test file
        test_dir = os.path.dirname(os.path.realpath(__file__))
        build_dir_path = os.path.join(test_dir, self.BUILD_DIR_TEMPLATE_PATH)

        copy_tree(build_dir_path, self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def check_file_exists(self, tarball_path, file_names):
        with tarfile.open(tarball_path) as f:
            output = f.getnames()
            for name in file_names:
                self.assertTrue(any(name in o for o in output))

    def test_build_tarball_tag(self):
        version_pdfs = [self.PDF_NAME_TEMPLATE.substitute(ver=self.VERSION, lang=lang) for lang in self.LANGUAGES]
        tarball_path, _ = build_doc_tarball('v4.1.0', None, self.temp_dir.name)

        self.check_file_exists(tarball_path, version_pdfs)

    def test_build_tarball_latest(self):
        version_pdfs = [self.PDF_NAME_TEMPLATE.substitute(ver=self.VERSION, lang=lang) for lang in self.LANGUAGES]
        tarball_path, _ = build_doc_tarball('latest', self.VERSION, self.temp_dir.name)

        self.check_file_exists(tarball_path, version_pdfs)

    def test_build_tarball_stable(self):
        version_pdfs = [self.PDF_NAME_TEMPLATE.substitute(ver=self.VERSION, lang=lang) for lang in self.LANGUAGES]
        tarball_path, _ = build_doc_tarball('stable', self.VERSION, self.temp_dir.name)

        self.check_file_exists(tarball_path, version_pdfs)

    # Different git repos using different numbers of digits for a commit ID
    # depending on how many is needed for a unique description
    # Check symlink succeeds even if they dont fully match
    def test_build_tarball_latest_short_sha1(self):
        version_pdfs = [self.PDF_NAME_TEMPLATE.substitute(ver=self.VERSION, lang=lang) for lang in self.LANGUAGES]

        version_short_sha1 = self.VERSION[:-1]
        tarball_path, _ = build_doc_tarball('latest', version_short_sha1, self.temp_dir.name)

        self.check_file_exists(tarball_path, version_pdfs)

    def test_build_tarball_latest_long_sha1(self):
        version_pdfs = [self.PDF_NAME_TEMPLATE.substitute(ver=self.VERSION, lang=lang) for lang in self.LANGUAGES]

        version_long_sha1 = self.VERSION + '5'
        tarball_path, _ = build_doc_tarball('latest', version_long_sha1, self.temp_dir.name)

        self.check_file_exists(tarball_path, version_pdfs)

    def test_build_tarball_latest_random_sha(self):
        version_pdfs = [self.PDF_NAME_TEMPLATE.substitute(ver=self.VERSION, lang=lang) for lang in self.LANGUAGES]

        version_long_sha1 = 'ra1n-dom-ID'
        tarball_path, _ = build_doc_tarball('latest', version_long_sha1, self.temp_dir.name)

        self.check_file_exists(tarball_path, version_pdfs)


if __name__ == '__main__':
    unittest.main()

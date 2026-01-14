import os
from esp_docs.sanitize_version import sanitize_version

import unittest


class TestSanitizeVersion(unittest.TestCase):

    def setUp(self):
        self.orig_env = os.environ.copy()
        for key in ['CI_COMMIT_REF_NAME', 'GITHUB_REF_NAME', 'ESP_DOCS_LATEST_BRANCH_NAME']:
            if key in os.environ:
                os.environ.pop(key)

    def tearDown(self):
        os.environ.clear()
        os.environ = self.orig_env

    def test_add_subs(self):
        test_version_mapping = [
            ('master', 'latest'),
            ('fix/update_file', 'fix-update_file'),
            ('fix(ci)/update0123', 'fix-ci--update0123'),
        ]

        for original_version, expected_version in test_version_mapping:
            self.assertEqual(sanitize_version(original_version), expected_version)


if __name__ == '__main__':
    unittest.main()

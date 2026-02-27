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

    def test_gitlab_ci_env_overrides(self):
        os.environ['CI_COMMIT_REF_NAME'] = 'release/v5.0'
        self.assertEqual(sanitize_version('anything'), 'release-v5.0')

    def test_github_ci_env_overrides(self):
        os.environ['GITHUB_REF_NAME'] = 'feature/new-thing'
        self.assertEqual(sanitize_version('anything'), 'feature-new-thing')

    def test_gitlab_takes_precedence_over_github(self):
        os.environ['CI_COMMIT_REF_NAME'] = 'from-gitlab'
        os.environ['GITHUB_REF_NAME'] = 'from-github'
        self.assertEqual(sanitize_version('anything'), 'from-gitlab')

    def test_custom_latest_branch_name(self):
        os.environ['ESP_DOCS_LATEST_BRANCH_NAME'] = 'main'
        self.assertEqual(sanitize_version('main'), 'latest')
        self.assertNotEqual(sanitize_version('master'), 'latest')

    def test_tag_version_preserved(self):
        self.assertEqual(sanitize_version('v5.1.2'), 'v5.1.2')

    def test_safe_characters_preserved(self):
        self.assertEqual(sanitize_version('v5.1-rc1'), 'v5.1-rc1')
        self.assertEqual(sanitize_version('v5.1_beta'), 'v5.1_beta')

    def test_special_characters_replaced(self):
        self.assertEqual(sanitize_version('feat@2!hot'), 'feat-2-hot')

    def test_ci_env_master_becomes_latest(self):
        os.environ['CI_COMMIT_REF_NAME'] = 'master'
        self.assertEqual(sanitize_version('anything'), 'latest')


if __name__ == '__main__':
    unittest.main()

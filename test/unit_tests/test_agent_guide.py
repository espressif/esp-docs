import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from esp_docs.cli import load_agent_guide, main


class TestAgentGuide(unittest.TestCase):

    def test_load_update_docs_guide(self):
        guide = load_agent_guide('update-docs')

        self.assertTrue(guide.startswith('# ESP-IDF Target Documentation Update Guide\n'))
        self.assertIn('## Source hierarchy', guide)
        self.assertIn('## Understand the ESP-Docs target mechanisms', guide)
        self.assertIn('## Workflow', guide)

    def test_update_docs_writes_complete_guide_to_stdout(self):
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            result = main(['agent-guide', 'update-docs'])

        self.assertEqual(result, 0)
        self.assertEqual(stdout.getvalue(), load_agent_guide('update-docs'))

    def test_unknown_guide_is_rejected(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr), self.assertRaises(SystemExit) as error:
            main(['agent-guide', 'unknown'])

        self.assertEqual(error.exception.code, 2)
        self.assertIn('invalid choice', stderr.getvalue())


if __name__ == '__main__':
    unittest.main()

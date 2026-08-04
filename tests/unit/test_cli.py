import unittest
from io import StringIO
from unittest.mock import patch
from src.application.cli import main
from src.application.runtime import RuntimeContext

class TestCLI(unittest.TestCase):

    @patch('src.application.cli.RuntimeEngine.initialize_runtime')
    @patch('sys.stdout', new_callable=StringIO)
    def test_version_flag(self, mock_stdout, mock_init):
        mock_init.return_value = RuntimeContext(
            repository_version="1.0.0",
            schema_version="1.0.0",
            status="READY",
            initialized_at="now",
            environment="development"
        )
        exit_code = main(["--version"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_stdout.getvalue().strip(), "1.0.0")

    @patch('src.application.cli.RuntimeEngine.initialize_runtime')
    @patch('sys.stdout', new_callable=StringIO)
    def test_status_flag(self, mock_stdout, mock_init):
        mock_init.return_value = RuntimeContext(
            repository_version="1.0.0",
            schema_version="1.0.0",
            status="READY",
            initialized_at="now",
            environment="development"
        )
        exit_code = main(["--status"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_stdout.getvalue().strip(), "READY")

    @patch('sys.stderr', new_callable=StringIO)
    def test_invalid_flag(self, mock_stderr):
        exit_code = main(["--invalid-flag"])
        self.assertEqual(exit_code, 2)
        self.assertIn("unrecognized arguments: --invalid-flag", mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_invalid_env(self, mock_stderr):
        exit_code = main(["--env", "invalid_env"])
        self.assertEqual(exit_code, 2)

if __name__ == '__main__':
    unittest.main()
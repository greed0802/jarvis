import unittest
from unittest.mock import patch
from src.application.api import handle_request
from src.application.runtime import RuntimeContext

class TestAPI(unittest.TestCase):

    def test_health(self):
        response = handle_request("/health")
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["health"], "OK")

    @patch('src.application.api.RuntimeEngine.initialize_runtime')
    def test_version(self, mock_init):
        mock_init.return_value = RuntimeContext(
            repository_version="1.0.0",
            schema_version="1.0.0",
            status="READY",
            initialized_at="now",
            environment="development"
        )
        response = handle_request("/version")
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["version"], "1.0.0")

    @patch('src.application.api.RuntimeEngine.initialize_runtime')
    def test_status_endpoint(self, mock_init):
        mock_init.return_value = RuntimeContext(
            repository_version="1.0.0",
            schema_version="1.0.0",
            status="READY",
            initialized_at="now",
            environment="development"
        )
        response = handle_request("/status")
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["runtime_status"], "READY")

    def test_invalid_path(self):
        response = handle_request("/invalid-path")
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["error"], "Not Found")

if __name__ == '__main__':
    unittest.main()
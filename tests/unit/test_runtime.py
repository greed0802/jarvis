import unittest
import os
import tempfile
import yaml
from pathlib import Path
from src.application.runtime import RuntimeEngine, RuntimeContext

class TestRuntime(unittest.TestCase):
    def setUp(self):
        self.engine = RuntimeEngine()
        
        # Create a temporary manifest file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.valid_manifest_path = os.path.join(self.temp_dir.name, "repository.yaml")
        
        valid_data = {
            "schema_version": "1.0.0",
            "versions": {
                "repository_version": "1.2.3"
            }
        }
        with open(self.valid_manifest_path, 'w') as f:
            yaml.dump(valid_data, f)
            
        self.invalid_manifest_path = os.path.join(self.temp_dir.name, "invalid.yaml")
        with open(self.invalid_manifest_path, 'w') as f:
            f.write("invalid: [yaml: content")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initial_state(self):
        self.assertEqual(self.engine.get_status(), "UNINITIALIZED")

    def test_initialize_runtime_success(self):
        context = self.engine.initialize_runtime(self.valid_manifest_path)
        
        self.assertEqual(self.engine.get_status(), "READY")
        self.assertIsInstance(context, RuntimeContext)
        self.assertEqual(context.schema_version, "1.0.0")
        self.assertEqual(context.repository_version, "1.2.3")
        self.assertEqual(context.status, "READY")
        self.assertEqual(context.environment, "development")
        self.assertIsNotNone(context.initialized_at)

    def test_initialize_runtime_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.engine.initialize_runtime(os.path.join(self.temp_dir.name, "does_not_exist.yaml"))
        self.assertEqual(self.engine.get_status(), "ERROR")

    def test_initialize_runtime_invalid_yaml(self):
        with self.assertRaises(ValueError):
            self.engine.initialize_runtime(self.invalid_manifest_path)
        self.assertEqual(self.engine.get_status(), "ERROR")

    def test_shutdown(self):
        self.engine.initialize_runtime(self.valid_manifest_path)
        self.assertEqual(self.engine.get_status(), "READY")
        
        success = self.engine.shutdown()
        self.assertTrue(success)
        self.assertEqual(self.engine.get_status(), "UNINITIALIZED")

if __name__ == '__main__':
    unittest.main()
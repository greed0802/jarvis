from dataclasses import dataclass
from datetime import datetime, timezone
import yaml
import os

@dataclass(frozen=True)
class RuntimeContext:
    repository_version: str
    schema_version: str
    status: str
    initialized_at: str
    environment: str = "development"

class RuntimeEngine:
    def __init__(self):
        self._state = "UNINITIALIZED"
        self._context = None

    def initialize_runtime(self, manifest_path: str = "repository.yaml") -> RuntimeContext:
        if not os.path.exists(manifest_path):
            self._state = "ERROR"
            raise FileNotFoundError(f"Manifest not found at {manifest_path}")

        try:
            with open(manifest_path, 'r') as f:
                manifest_data = yaml.safe_load(f)
        except Exception:
            self._state = "ERROR"
            raise ValueError(f"Failed to load manifest at {manifest_path}")

        schema_version = manifest_data.get("schema_version", "unknown")
        repo_version = manifest_data.get("versions", {}).get("repository_version", "unknown")

        self._state = "READY"
        self._context = RuntimeContext(
            repository_version=repo_version,
            schema_version=schema_version,
            status=self._state,
            initialized_at=datetime.now(timezone.utc).isoformat()
        )

        return self._context

    def get_status(self) -> str:
        return self._state

    def shutdown(self) -> bool:
        self._state = "UNINITIALIZED"
        self._context = None
        return True
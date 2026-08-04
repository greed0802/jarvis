"""DatasetService facade for GoldenDatasetLoader."""

from __future__ import annotations

from jarvis.evaluation.datasets import GoldenDatasetLoader

class DatasetService:
    """Facade over GoldenDatasetLoader for CLI dataset operations."""

    def __init__(self) -> None:
        self._loader = GoldenDatasetLoader()

    def list_datasets(self) -> dict:
        """List all available golden datasets and their cases.

        Returns:
            dict with dataset names, case counts.

        Raises:
            RuntimeError: If dataset discovery fails (exit code 4).
        """
        try:
            datasets = self._loader.list_datasets()
            result = {"datasets": {}}
            for ds in datasets:
                cases = self._loader.load_cases(ds)
                result["datasets"][ds] = {
                    "case_count": len(cases),
                    "baseline_verified": len(cases) > 0,
                }
            return result
        except Exception as exc:
            raise RuntimeError(f"Dataset validation failed: {exc}")
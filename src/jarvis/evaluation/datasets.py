"""Golden dataset loader for M11.0 Evaluation Framework.

Loads versioned, structured golden datasets from the evaluation/datasets/
directory hierarchy. Each dataset is a directory of JSON case files.

Loader provides:
- Metadata discovery (available datasets and their versioning)
- Case loading with baseline attributes

Per AC-3: Cases are structured EvaluationCase instances with explicit expected outputs.
"""
import json
from pathlib import Path
from typing import Any

from jarvis.evaluation.contracts import EvaluationCase

_DEFAULT_DATASET_BASE = Path("evaluation/datasets/golden")

class GoldenDatasetLoader:
    """Loads golden evaluation datasets from the filesystem.

    Datasets are structured as: evaluation/datasets/golden/<name>/case_XXX/
    Each case directory contains JSON files:

      input_evidence.json       — minimal evidence objects for the test (e.g., references)
      expected_findings.json    — Expected findings model (used by EVA-1, EVA-3)
      expected_understanding.json — Expected understanding output (used by EVA-2)
      expected_citations.json    — Expected cited evidence (used by EVA-2, EVA-3)
      expected_routes.json      — Expected navigation routes (used by EVA-3)

    For M11.0 running against M10.6, these are reference golden records.
    """

    def __init__(self, base_path: Path | None = None) -> None:
        self._base = base_path or _DEFAULT_DATASET_BASE

    # -------------------------------------------------------------------------
    # Dataset discovery
    # -------------------------------------------------------------------------

    def list_datasets(self) -> list[str]:
        """Return a list of available golden dataset names."""
        if not self._base.exists():
            return []
        return [
            d.name for d in self._base.iterdir()
            if d.is_dir() and not d.name.startswith(".") and not d.name.startswith("_")
        ]

    # -------------------------------------------------------------------------
    # Case loading
    # -------------------------------------------------------------------------

    def load_case(self, dataset_name: str, case_id: str) -> EvaluationCase | None:
        """Load a single golden evaluation case by dataset and case ID.

        Args:
            dataset_name: Name of the dataset directory (e.g., 'boq_baseline').
            case_id:      Case identifier (e.g., 'case_001').

        Returns:
            EvaluationCase with all JSON inputs bundled, or None if directory doesn't exist.
        """
        case_dir = self._base / dataset_name / case_id
        if not case_dir.is_dir():
            return None

        def _read_json(filename: str) -> dict[str, Any]:
            path = case_dir / filename
            if path.is_file():
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}

        input_artifacts = {
            "evidence": _read_json("input_evidence.json"),
        }

        expected_outputs = {
            "findings": _read_json("expected_findings.json"),
            "understanding": _read_json("expected_understanding.json"),
            "citations": _read_json("expected_citations.json"),
            "routes": _read_json("expected_routes.json"),
        }

        return EvaluationCase(
            case_id=case_id,
            dataset_name=dataset_name,
            input_artifacts=input_artifacts,
            expected_outputs=expected_outputs,
        )

    def load_cases(self, dataset_name: str) -> list[EvaluationCase]:
        """Load all EvaluationCases in a dataset.

        Args:
            dataset_name: Name of the dataset directory.

        Returns:
            List of EvaluationCase objects loadable from this dataset.
        """
        dataset_dir = self._base / dataset_name
        if not dataset_dir.is_dir():
            return []

        cases: list[EvaluationCase] = []
        for entry in sorted(dataset_dir.iterdir()):
            if entry.is_dir() and not entry.name.startswith("."):
                case = self.load_case(dataset_name, entry.name)
                if case:
                    cases.append(case)

        return cases

    def load_all_cases(self) -> list[EvaluationCase]:
        """Load all cases from all available datasets.

        Returns:
            Flat list of all EvaluationCases across all datasets.
        """
        all_cases: list[EvaluationCase] = []
        for dataset_name in self.list_datasets():
            all_cases.extend(self.load_cases(dataset_name))
        return all_cases
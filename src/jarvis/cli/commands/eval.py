"""Handler for `jarvis eval` — platform evaluation execution."""

from __future__ import annotations

from jarvis.cli.exitcodes import ExitCode
from jarvis.cli.services.evaluation_service import EvaluationService

class EvalCommand:
    """Thin command: delegates to EvaluationService ONLY."""

    def __init__(self, service: EvaluationService) -> None:
        self._service = service

    def execute(self, profile_name: str) -> tuple[int, dict]:
        """Execute evaluation profile.

        Args:
            profile_name: smoke, regression, release, or research.

        Returns:
            Tuple of (exit_code, result_dict).
        """
        try:
            result = self._service.run_profile(profile_name)
            if result["promotion_gate_passed"]:
                return ExitCode.EXIT_SUCCESS, result
            return ExitCode.EXIT_EVAL_GATE_FAILED, result
        except ValueError:
            return ExitCode.EXIT_INVALID_ARGS, {"error": f"Invalid profile: {profile_name}"}
        except RuntimeError:
            return ExitCode.EXIT_DATASET_INVALID, {"error": "Dataset validation failed"}
        except Exception:
            return ExitCode.EXIT_INTERNAL_ERROR, {"error": "Internal evaluation error"}
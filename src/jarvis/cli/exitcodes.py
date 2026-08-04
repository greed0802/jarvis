"""Deterministic exit codes for jarvis CLI (Track A1 / ES-A101)."""

from enum import IntEnum

class ExitCode(IntEnum):
    """Machine-verified exit codes for CI/CD automation.

    Per ES-A101: Every CLI command returns a documented exit code.
    """
    EXIT_SUCCESS = 0
    EXIT_INTERNAL_ERROR = 1
    EXIT_INVALID_ARGS = 2
    EXIT_EVAL_GATE_FAILED = 3
    EXIT_DATASET_INVALID = 4
    EXIT_PROJECT_LOAD_FAILED = 5
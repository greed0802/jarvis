"""CheckMate Application Error Model.

Deterministic errors that distinguish between:
- Configuration errors
- Contract violation errors
- Runtime errors
- Unexpected internal failures

No generic Exception propagation across public boundaries.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0 (Principle 7 — Deterministic Applications)
"""

from __future__ import annotations


class CheckMateError(Exception):
    """Base error for all CheckMate application errors.

    All CheckMate errors inherit from this class to ensure
    consumers can catch a single base type when needed.
    """

    def __init__(self, message: str, *, code: str | None = None) -> None:
        """Initialize the error.

        Args:
            message: Human-readable error description.
            code: Optional machine-readable error code.
        """
        self._code = code
        super().__init__(message)

    @property
    def code(self) -> str | None:
        """Get the machine-readable error code."""
        return self._code

    @property
    def message(self) -> str:
        """Get the human-readable error message."""
        return str(self.args[0]) if self.args else ""


class ConfigurationError(CheckMateError):
    """Configuration validation error.

    Raised when application configuration is invalid or missing
    required values.

    Error code: CONFIG_ERR
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, code="CONFIG_ERR")


class ContractViolationError(CheckMateError):
    """Contract violation error.

    Raised when input data violates the expected contract.

    Error code: CONTRACT_VIOLATION
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, code="CONTRACT_VIOLATION")


class ApplicationRuntimeError(CheckMateError):
    """Application runtime error.

    Raised when the application encounters a recoverable runtime
    issue during execution.

    Error code: RUNTIME_ERR
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, code="RUNTIME_ERR")


class InternalError(CheckMateError):
    """Unexpected internal application error.

    Raised when an unexpected internal failure occurs that cannot
    be classified as configuration, contract, or runtime.

    Error code: INTERNAL_ERR
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, code="INTERNAL_ERR")
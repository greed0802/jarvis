"""Tests for CheckMate Application Error Model (IP-0003).

Verifies:
- Error hierarchy
- Error codes
- Error messages
- Error raising and catching
- Error type specificity
"""

from __future__ import annotations

import pytest

from jarvis.applications.checkmate.errors import (
    CheckMateError,
    ConfigurationError,
    ContractViolationError,
    ApplicationRuntimeError,
    InternalError,
)

class TestCheckMateErrorBase:
    """Verify base error class."""

    def test_base_error_is_exception(self):
        """CheckMateError inherits from Exception."""
        assert issubclass(CheckMateError, Exception)

    def test_base_error_with_message(self):
        """Base error stores message."""
        error = CheckMateError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"

    def test_base_error_with_code(self):
        """Base error stores optional code."""
        error = CheckMateError("Test error", code="TEST_CODE")
        assert error.code == "TEST_CODE"

    def test_base_error_without_code(self):
        """Base error code is None when not provided."""
        error = CheckMateError("Test error")
        assert error.code is None

class TestConfigurationError:
    """Verify ConfigurationError."""

    def test_is_checkmate_error(self):
        """ConfigurationError is a CheckMateError."""
        assert issubclass(ConfigurationError, CheckMateError)

    def test_error_code(self):
        """ConfigurationError has correct error code."""
        error = ConfigurationError("Bad config")
        assert error.code == "CONFIG_ERR"

    def test_error_message(self):
        """ConfigurationError stores message."""
        error = ConfigurationError("Invalid log level")
        assert error.message == "Invalid log level"

    def test_can_catch_as_checkmate_error(self):
        """ConfigurationError can be caught as CheckMateError."""
        with pytest.raises(CheckMateError) as exc_info:
            raise ConfigurationError("Test")
        assert isinstance(exc_info.value, ConfigurationError)

class TestContractViolationError:
    """Verify ContractViolationError."""

    def test_is_checkmate_error(self):
        """ContractViolationError is a CheckMateError."""
        assert issubclass(ContractViolationError, CheckMateError)

    def test_error_code(self):
        """ContractViolationError has correct error code."""
        error = ContractViolationError("Missing field")
        assert error.code == "CONTRACT_VIOLATION"

    def test_error_message(self):
        """ContractViolationError stores message."""
        error = ContractViolationError("Evidence missing required fields")
        assert error.message == "Evidence missing required fields"

    def test_can_catch_as_checkmate_error(self):
        """ContractViolationError can be caught as CheckMateError."""
        with pytest.raises(CheckMateError) as exc_info:
            raise ContractViolationError("Test")
        assert isinstance(exc_info.value, ContractViolationError)

class TestApplicationRuntimeError:
    """Verify ApplicationRuntimeError."""

    def test_is_checkmate_error(self):
        """ApplicationRuntimeError is a CheckMateError."""
        assert issubclass(ApplicationRuntimeError, CheckMateError)

    def test_error_code(self):
        """ApplicationRuntimeError has correct error code."""
        error = ApplicationRuntimeError("Runtime issue")
        assert error.code == "RUNTIME_ERR"

    def test_error_message(self):
        """ApplicationRuntimeError stores message."""
        error = ApplicationRuntimeError("Execution failed")
        assert error.message == "Execution failed"

    def test_can_catch_as_checkmate_error(self):
        """ApplicationRuntimeError can be caught as CheckMateError."""
        with pytest.raises(CheckMateError) as exc_info:
            raise ApplicationRuntimeError("Test")
        assert isinstance(exc_info.value, ApplicationRuntimeError)

class TestInternalError:
    """Verify InternalError."""

    def test_is_checkmate_error(self):
        """InternalError is a CheckMateError."""
        assert issubclass(InternalError, CheckMateError)

    def test_error_code(self):
        """InternalError has correct error code."""
        error = InternalError("Unexpected failure")
        assert error.code == "INTERNAL_ERR"

    def test_error_message(self):
        """InternalError stores message."""
        error = InternalError("Unexpected internal failure")
        assert error.message == "Unexpected internal failure"

    def test_can_catch_as_checkmate_error(self):
        """InternalError can be caught as CheckMateError."""
        with pytest.raises(CheckMateError) as exc_info:
            raise InternalError("Test")
        assert isinstance(exc_info.value, InternalError)

class TestErrorHierarchy:
    """Verify the error hierarchy is correct."""

    def test_all_errors_are_distinct(self):
        """All error types are distinct."""
        errors = [
            ConfigurationError("a"),
            ContractViolationError("b"),
            ApplicationRuntimeError("c"),
            InternalError("d"),
        ]
        types = {type(e) for e in errors}
        assert len(types) == 4

    def test_catch_base_catches_all(self):
        """Catching CheckMateError catches all error types."""
        errors_raised = False
        try:
            raise InternalError("Test")
        except CheckMateError:
            errors_raised = True
        assert errors_raised

    def test_specific_catch_before_general(self):
        """Specific error types can be caught before base type."""
        try:
            raise ConfigurationError("Test")
        except ConfigurationError:
            pass
        except CheckMateError:
            pytest.fail("Should have caught ConfigurationError first")

    def test_str_representation(self):
        """Error string representation includes message."""
        error = ConfigurationError("Something went wrong")
        assert "Something went wrong" in str(error)

    def test_no_error_code_conflicts(self):
        """All error codes are unique."""
        errors = [
            ConfigurationError("a"),
            ContractViolationError("b"),
            ApplicationRuntimeError("c"),
            InternalError("d"),
        ]
        codes = [e.code for e in errors]
        assert len(codes) == len(set(codes))
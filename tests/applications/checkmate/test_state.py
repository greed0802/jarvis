"""Tests for CheckMate Application Runtime State (IP-0003).

Verifies:
- Status transitions
- Invalid transitions are rejected
- Runtime state defaults
- Runtime state transitions
- Diagnostics
"""

from __future__ import annotations

import pytest

from jarvis.applications.checkmate.state import CheckMateStatus, CheckMateRuntimeState
from jarvis.applications.checkmate.config import CheckMateConfig

class TestCheckMateStatusTransitions:
    """Verify deterministic status transitions."""

    def test_uninitialized_to_initialized(self):
        """UNINITIALIZED can transition to INITIALIZED."""
        assert CheckMateStatus.UNINITIALIZED.can_transition_to(CheckMateStatus.INITIALIZED)

    def test_initialized_to_input_ready(self):
        """INITIALIZED can transition to INPUT_READY."""
        assert CheckMateStatus.INITIALIZED.can_transition_to(CheckMateStatus.INPUT_READY)

    def test_initialized_to_failed(self):
        """INITIALIZED can transition to FAILED."""
        assert CheckMateStatus.INITIALIZED.can_transition_to(CheckMateStatus.FAILED)

    def test_input_ready_to_running(self):
        """INPUT_READY can transition to RUNNING."""
        assert CheckMateStatus.INPUT_READY.can_transition_to(CheckMateStatus.RUNNING)

    def test_input_ready_to_failed(self):
        """INPUT_READY can transition to FAILED."""
        assert CheckMateStatus.INPUT_READY.can_transition_to(CheckMateStatus.FAILED)

    def test_running_to_complete(self):
        """RUNNING can transition to COMPLETE."""
        assert CheckMateStatus.RUNNING.can_transition_to(CheckMateStatus.COMPLETE)

    def test_running_to_failed(self):
        """RUNNING can transition to FAILED."""
        assert CheckMateStatus.RUNNING.can_transition_to(CheckMateStatus.FAILED)

class TestCheckMateStatusInvalidTransitions:
    """Verify invalid transitions are rejected."""

    def test_uninitialized_cannot_skip_to_running(self):
        """Cannot skip from UNINITIALIZED to RUNNING."""
        assert not CheckMateStatus.UNINITIALIZED.can_transition_to(CheckMateStatus.RUNNING)

    def test_uninitialized_cannot_skip_to_complete(self):
        """Cannot skip from UNINITIALIZED to COMPLETE."""
        assert not CheckMateStatus.UNINITIALIZED.can_transition_to(CheckMateStatus.COMPLETE)

    def test_complete_is_terminal(self):
        """COMPLETE is a terminal state — no outgoing transitions."""
        assert not CheckMateStatus.COMPLETE.can_transition_to(CheckMateStatus.UNINITIALIZED)
        assert not CheckMateStatus.COMPLETE.can_transition_to(CheckMateStatus.INITIALIZED)
        assert not CheckMateStatus.COMPLETE.can_transition_to(CheckMateStatus.INPUT_READY)
        assert not CheckMateStatus.COMPLETE.can_transition_to(CheckMateStatus.RUNNING)
        assert not CheckMateStatus.COMPLETE.can_transition_to(CheckMateStatus.FAILED)

    def test_failed_is_terminal(self):
        """FAILED is a terminal state — no outgoing transitions."""
        assert not CheckMateStatus.FAILED.can_transition_to(CheckMateStatus.UNINITIALIZED)
        assert not CheckMateStatus.FAILED.can_transition_to(CheckMateStatus.INITIALIZED)
        assert not CheckMateStatus.FAILED.can_transition_to(CheckMateStatus.COMPLETE)

    def test_cannot_go_backward(self):
        """Cannot transition backward from INPUT_READY to INITIALIZED."""
        assert not CheckMateStatus.INPUT_READY.can_transition_to(CheckMateStatus.INITIALIZED)

class TestCheckMateRuntimeStateDefaults:
    """Verify runtime state default values."""

    def test_default_status(self):
        """Default status is UNINITIALIZED."""
        state = CheckMateRuntimeState()
        assert state.status == CheckMateStatus.UNINITIALIZED

    def test_default_has_evidence(self):
        """Default has_evidence is False."""
        state = CheckMateRuntimeState()
        assert state.has_evidence is False

    def test_default_has_findings(self):
        """Default has_findings is False."""
        state = CheckMateRuntimeState()
        assert state.has_findings is False

    def test_default_started_at(self):
        """Default started_at is None."""
        state = CheckMateRuntimeState()
        assert state.started_at is None

    def test_default_completed_at(self):
        """Default completed_at is None."""
        state = CheckMateRuntimeState()
        assert state.completed_at is None

    def test_default_error_count(self):
        """Default error_count is 0."""
        state = CheckMateRuntimeState()
        assert state.error_count == 0

    def test_default_errors(self):
        """Default errors is empty list."""
        state = CheckMateRuntimeState()
        assert state.errors == []

    def test_default_diagnostics(self):
        """Default diagnostics is empty dict."""
        state = CheckMateRuntimeState()
        assert state.diagnostics == {}

    def test_config_is_checkmate_config(self):
        """Default config is a CheckMateConfig instance."""
        state = CheckMateRuntimeState()
        assert isinstance(state.config, CheckMateConfig)

    def test_elapsed_none_before_start(self):
        """elapsed_seconds is None before execution starts."""
        state = CheckMateRuntimeState()
        assert state.elapsed_seconds is None

class TestCheckMateRuntimeStateTransitions:
    """Verify runtime state transitions."""

    def test_transition_to_initialized(self):
        """State can transition from UNINITIALIZED to INITIALIZED."""
        state = CheckMateRuntimeState()
        state.transition_to(CheckMateStatus.INITIALIZED)
        assert state.status == CheckMateStatus.INITIALIZED

    def test_transition_to_input_ready(self):
        """State can transition from INITIALIZED to INPUT_READY."""
        state = CheckMateRuntimeState()
        state.transition_to(CheckMateStatus.INITIALIZED)
        state.transition_to(CheckMateStatus.INPUT_READY)
        assert state.status == CheckMateStatus.INPUT_READY

    def test_transition_to_running(self):
        """State can transition from INPUT_READY to RUNNING."""
        state = CheckMateRuntimeState()
        state.transition_to(CheckMateStatus.INITIALIZED)
        state.transition_to(CheckMateStatus.INPUT_READY)
        state.transition_to(CheckMateStatus.RUNNING)
        assert state.status == CheckMateStatus.RUNNING

    def test_transition_to_complete(self):
        """State can transition from RUNNING to COMPLETE."""
        state = CheckMateRuntimeState()
        state.transition_to(CheckMateStatus.INITIALIZED)
        state.transition_to(CheckMateStatus.INPUT_READY)
        state.transition_to(CheckMateStatus.RUNNING)
        state.transition_to(CheckMateStatus.COMPLETE)
        assert state.status == CheckMateStatus.COMPLETE

    def test_transition_to_failed_from_initialized(self):
        """State can transition from INITIALIZED to FAILED."""
        state = CheckMateRuntimeState()
        state.transition_to(CheckMateStatus.INITIALIZED)
        state.transition_to(CheckMateStatus.FAILED)
        assert state.status == CheckMateStatus.FAILED

    def test_invalid_transition_raises(self):
        """Invalid transition raises RuntimeError."""
        state = CheckMateRuntimeState()
        with pytest.raises(RuntimeError, match="Invalid status transition"):
            state.transition_to(CheckMateStatus.RUNNING)

    def test_terminal_state_rejects_transition(self):
        """Terminal state rejects any transition."""
        state = CheckMateRuntimeState()
        state.transition_to(CheckMateStatus.INITIALIZED)
        state.transition_to(CheckMateStatus.INPUT_READY)
        state.transition_to(CheckMateStatus.RUNNING)
        state.transition_to(CheckMateStatus.COMPLETE)
        with pytest.raises(RuntimeError, match="Invalid status transition"):
            state.transition_to(CheckMateStatus.FAILED)

    def test_failed_rejects_transition(self):
        """FAILED state rejects any transition."""
        state = CheckMateRuntimeState()
        state.transition_to(CheckMateStatus.INITIALIZED)
        state.transition_to(CheckMateStatus.FAILED)
        with pytest.raises(RuntimeError, match="Invalid status transition"):
            state.transition_to(CheckMateStatus.COMPLETE)

class TestCheckMateRuntimeStateRecording:
    """Verify error recording and diagnostics."""

    def test_record_error_increments_count(self):
        """Recording an error increments the count."""
        state = CheckMateRuntimeState()
        state.record_error("Test error")
        assert state.error_count == 1

    def test_record_error_appends_message(self):
        """Recording an error appends the message."""
        state = CheckMateRuntimeState()
        state.record_error("Test error")
        assert state.errors == ["Test error"]

    def test_record_multiple_errors(self):
        """Recording multiple errors increments count and appends."""
        state = CheckMateRuntimeState()
        state.record_error("Error 1")
        state.record_error("Error 2")
        state.record_error("Error 3")
        assert state.error_count == 3
        assert state.errors == ["Error 1", "Error 2", "Error 3"]

    def test_diagnostics_is_mutable_dict(self):
        """Diagnostics can be updated after creation."""
        state = CheckMateRuntimeState()
        state.diagnostics["key"] = "value"
        assert state.diagnostics["key"] == "value"

    def test_config_assigned(self):
        """Custom config is assigned during state creation."""
        config = CheckMateConfig(log_level="DEBUG")
        state = CheckMateRuntimeState(config=config)
        assert state.config.log_level == "DEBUG"
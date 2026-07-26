"""Tests for CheckMate Application Configuration (IP-0003).

Verifies:
- Configuration creation with defaults
- Configuration immutability
- Configuration validation
- Edge cases
"""

from __future__ import annotations

import pytest

from jarvis.applications.checkmate.config import CheckMateConfig


class TestCheckMateConfigDefaults:
    """Verify default configuration values."""

    def test_default_log_level(self):
        """Default log level is INFO."""
        config = CheckMateConfig()
        assert config.log_level == "INFO"

    def test_default_validate_inputs(self):
        """Input validation is enabled by default."""
        config = CheckMateConfig()
        assert config.validate_inputs is True

    def test_default_diagnostics_disabled(self):
        """Diagnostics are disabled by default."""
        config = CheckMateConfig()
        assert config.enable_diagnostics is False

    def test_default_max_errors(self):
        """Default max errors is 10."""
        config = CheckMateConfig()
        assert config.max_errors == 10


class TestCheckMateConfigCustomization:
    """Verify custom configuration values."""

    def test_custom_log_level(self):
        """Custom log level is accepted."""
        config = CheckMateConfig(log_level="DEBUG")
        assert config.log_level == "DEBUG"

    def test_diagnostics_enabled(self):
        """Diagnostics can be enabled."""
        config = CheckMateConfig(enable_diagnostics=True)
        assert config.enable_diagnostics is True

    def test_input_validation_disabled(self):
        """Input validation can be disabled."""
        config = CheckMateConfig(validate_inputs=False)
        assert config.validate_inputs is False

    def test_custom_max_errors(self):
        """Custom max errors is accepted."""
        config = CheckMateConfig(max_errors=5)
        assert config.max_errors == 5

    def test_case_insensitive_log_level(self):
        """Log level comparison is case-insensitive during validation."""
        config = CheckMateConfig(log_level="debug")
        assert config.log_level == "debug"

    def test_multiple_custom_values(self):
        """Multiple custom values can be set simultaneously."""
        config = CheckMateConfig(
            log_level="WARNING",
            validate_inputs=False,
            enable_diagnostics=True,
            max_errors=3,
        )
        assert config.log_level == "WARNING"
        assert config.validate_inputs is False
        assert config.enable_diagnostics is True
        assert config.max_errors == 3


class TestCheckMateConfigImmutability:
    """Verify configuration is immutable."""

    def test_config_is_frozen(self):
        """CheckMateConfig dataclass is frozen."""
        config = CheckMateConfig()
        assert config.__dataclass_params__.frozen is True

    def test_cannot_modify_log_level(self):
        """Cannot modify log_level after creation."""
        config = CheckMateConfig()
        with pytest.raises(AttributeError):
            config.log_level = "DEBUG"  # type: ignore[misc]

    def test_cannot_modify_max_errors(self):
        """Cannot modify max_errors after creation."""
        config = CheckMateConfig()
        with pytest.raises(AttributeError):
            config.max_errors = 5  # type: ignore[misc]


class TestCheckMateConfigValidation:
    """Verify configuration validation."""

    def test_invalid_log_level_raises(self):
        """Invalid log level raises ValueError."""
        with pytest.raises(ValueError, match="Invalid log_level"):
            CheckMateConfig(log_level="INVALID")

    def test_zero_max_errors_raises(self):
        """max_errors < 1 raises ValueError."""
        with pytest.raises(ValueError, match="Invalid max_errors"):
            CheckMateConfig(max_errors=0)

    def test_negative_max_errors_raises(self):
        """Negative max_errors raises ValueError."""
        with pytest.raises(ValueError, match="Invalid max_errors"):
            CheckMateConfig(max_errors=-1)

    def test_empty_log_level_raises(self):
        """Empty log level raises ValueError."""
        with pytest.raises(ValueError, match="Invalid log_level"):
            CheckMateConfig(log_level="")

    @pytest.mark.parametrize("valid_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    def test_all_valid_log_levels(self, valid_level):
        """All valid log levels are accepted."""
        config = CheckMateConfig(log_level=valid_level)
        assert config.log_level == valid_level


class TestCheckMateConfigEquality:
    """Verify configuration equality semantics."""

    def test_equal_configs(self):
        """Configs with same values are equal."""
        config_a = CheckMateConfig(log_level="DEBUG")
        config_b = CheckMateConfig(log_level="DEBUG")
        assert config_a == config_b

    def test_different_configs_not_equal(self):
        """Configs with different values are not equal."""
        config_a = CheckMateConfig(log_level="INFO")
        config_b = CheckMateConfig(log_level="DEBUG")
        assert config_a != config_b
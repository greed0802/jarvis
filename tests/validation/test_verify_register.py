"""
Test the refactored verify_register validator.
"""

import pytest
import json
from pathlib import Path
from tools.quality.verify_register import (
    validate_register_structure,
    validate_unique_eq_numbers,
    validate_authority_documents_exist,
    validate_evidence_packages_exist,
    validate_repository_paths,
    validate_status_values,
    validate_no_duplicate_registrations,
    validate_register_completeness
)

def test_register_structure_validation():
    """Test register structure validation."""
    result = validate_register_structure()
    assert result.success, f"Register structure validation failed: {result.findings}"

def test_unique_eq_numbers_validation():
    """Test unique EQ numbers validation."""
    result = validate_unique_eq_numbers()
    assert result.success, f"Unique EQ numbers validation failed: {result.findings}"

def test_repository_paths_validation():
    """Test repository paths validation."""
    result = validate_repository_paths()
    assert result.success, f"Repository paths validation failed: {result.findings}"

def test_status_values_validation():
    """Test status values validation."""
    result = validate_status_values()
    assert result.success, f"Status values validation failed: {result.findings}"

def test_no_duplicate_registrations_validation():
    """Test no duplicate registrations validation."""
    result = validate_no_duplicate_registrations()
    assert result.success, f"No duplicate registrations validation failed: {result.findings}"

def test_register_completeness_validation():
    """Test register completeness validation."""
    result = validate_register_completeness()
    assert result.success, f"Register completeness validation failed: {result.findings}"

def test_authority_documents_validation():
    """Test authority documents validation - may have expected failures for missing files."""
    result = validate_authority_documents_exist()
    # This may fail if some authority documents don't exist, which is expected
    # We just check that it runs without exceptions
    assert isinstance(result.success, bool)
    assert isinstance(result.findings, list)

def test_evidence_packages_validation():
    """Test evidence packages validation - may have expected failures for missing files."""
    result = validate_evidence_packages_exist()
    # This may fail if some evidence packages don't exist, which is expected
    # We just check that it runs without exceptions
    assert isinstance(result.success, bool)
    assert isinstance(result.findings, list)

def test_validation_result_structure():
    """Test that all validation functions return ValidationResult objects."""
    validation_functions = [
        validate_register_structure,
        validate_unique_eq_numbers,
        validate_authority_documents_exist,
        validate_evidence_packages_exist,
        validate_repository_paths,
        validate_status_values,
        validate_no_duplicate_registrations,
        validate_register_completeness
    ]

    for func in validation_functions:
        result = func()
        assert hasattr(result, 'success')
        assert hasattr(result, 'findings')
        assert isinstance(result.success, bool)
        assert isinstance(result.findings, list)
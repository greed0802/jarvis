"""
Test the shared governance library functionality.
"""

import pytest
from pathlib import Path
from tools.quality.shared_governance import (
    EngineeringRegisterParser,
    EngineeringQuestion,
    RepositoryPath,
    FileValidator,
    ValidationResult,
    count_findings_by_severity,
    generate_validation_report
)

def test_repository_paths_enum():
    """Test that RepositoryPath enum contains expected paths."""
    assert RepositoryPath.ENGINEERING_REGISTER.value.exists()
    assert RepositoryPath.ENGINEERING_QUESTIONS.value.exists()
    assert RepositoryPath.ENGINEERING_EVIDENCE.value.exists()

def test_engineering_question_model():
    """Test EngineeringQuestion data model."""
    eq = EngineeringQuestion(
        eq_number="EQ-0001",
        title="Test EQ",
        status="Active",
        authority_document_text="Test Authority",
        authority_document_path="../questions/EQ_0001.md",
        evidence_text="Test Evidence",
        evidence_path="../evidence/EQ_0001/",
        outcome="Test Outcome",
        repository_location="docs/engineering/"
    )

    assert eq.validate_authority_document_path()
    assert eq.validate_evidence_path()
    assert eq.validate_status()
    assert eq.validate_repository_location()

    # Test invalid cases
    eq_invalid_status = EngineeringQuestion(
        eq_number="EQ-0001",
        title="Test EQ",
        status="Invalid",
        authority_document_text="Test Authority",
        authority_document_path="../questions/EQ_0001.md",
        evidence_text="Test Evidence",
        evidence_path="../evidence/EQ_0001/",
        outcome="Test Outcome",
        repository_location="docs/engineering/"
    )
    assert not eq_invalid_status.validate_status()

def test_file_validator():
    """Test FileValidator utilities."""
    # Test with existing file
    success, findings = FileValidator.validate_file_exists(
        RepositoryPath.ENGINEERING_REGISTER.value,
        "Engineering Register not found"
    )
    assert success
    assert len(findings) == 0

    # Test with non-existing file
    success, findings = FileValidator.validate_file_exists(
        Path("/non/existent/file.md"),
        "Test file not found"
    )
    assert not success
    assert len(findings) == 1
    assert "ERROR: Test file not found" in findings[0]

def test_validation_result():
    """Test ValidationResult class."""
    result = ValidationResult(True, ["INFO: Test finding"])
    assert result.success
    assert result.to_dict() == {
        "success": True,
        "findings": ["INFO: Test finding"]
    }

def test_count_findings_by_severity():
    """Test findings severity counting."""
    findings = [
        "ERROR: Critical error",
        "WARN: Warning message",
        "INFO: Information",
        "ERROR: Another error",
        "Some other message"
    ]

    counts = count_findings_by_severity(findings)
    assert counts["error_count"] == 2
    assert counts["warning_count"] == 1
    assert counts["info_count"] == 1

def test_generate_validation_report():
    """Test validation report generation."""
    results = [
        ("test1", ValidationResult(True, [])),
        ("test2", ValidationResult(False, ["ERROR: Test error"])),
        ("test3", ValidationResult(True, ["WARN: Test warning"]))
    ]

    report = generate_validation_report("test_tool", results)

    assert report["tool"] == "test_tool"
    assert report["overall_pass"] is False
    assert report["summary"]["total_checks"] == 3
    assert report["summary"]["passed_checks"] == 2
    assert report["summary"]["failed_checks"] == 1
    assert report["summary"]["error_count"] == 1
    assert report["summary"]["warning_count"] == 1
    assert report["summary"]["info_count"] == 0

def test_engineering_register_parsing():
    """Test Engineering Register parsing functionality."""
    success, findings, eq_entries = EngineeringRegisterParser.parse_register()

    assert success, f"Register parsing failed: {findings}"
    assert len(eq_entries) > 0, "No EQ entries found in register"

    # Test that all entries have required fields
    for eq in eq_entries:
        assert eq.eq_number.startswith("EQ-")
        assert eq.title.strip()
        assert eq.status.strip()
        assert eq.authority_document_text.strip()
        assert eq.authority_document_path.strip()
        assert eq.evidence_text.strip()
        assert eq.evidence_path.strip()
        assert eq.outcome.strip()
        assert eq.repository_location.strip()

def test_register_structure_validation():
    """Test register structure validation."""
    success, findings = EngineeringRegisterParser.validate_register_structure()
    assert success, f"Register structure validation failed: {findings}"


# ============================================================
# TASK 5: Deterministic Test Fixtures
# Comprehensive edge case coverage for the shared library
# ============================================================

class TestEngineeringQuestionPathResolution:
    """Verify path resolution for valid and invalid inputs."""

    def test_valid_authority_path_resolves_correctly(self):
        """Valid '../questions/X.md' path maps to ENGINEERING_QUESTIONS/X.md."""
        eq = EngineeringQuestion(
            eq_number="EQ-9999",
            title="Test",
            status="Active",
            authority_document_text="Test_Document.md",
            authority_document_path="../questions/Test_Document.md",
            evidence_text="Test Evidence",
            evidence_path="../evidence/Test/",
            outcome="Approved",
            repository_location="docs/engineering/"
        )
        resolved = eq.get_authority_document_full_path()
        expected = RepositoryPath.ENGINEERING_QUESTIONS.value / "Test_Document.md"
        assert resolved == expected.resolve(), f"Expected {expected}, got {resolved}"

    def test_valid_evidence_path_resolves_correctly(self):
        """Valid '../evidence/X/' path maps to ENGINEERING_EVIDENCE/X."""
        eq = EngineeringQuestion(
            eq_number="EQ-9999",
            title="Test",
            status="Active",
            authority_document_text="Test.md",
            authority_document_path="../questions/Test.md",
            evidence_text="Test Evidence",
            evidence_path="../evidence/Test_Package/",
            outcome="Approved",
            repository_location="docs/engineering/"
        )
        resolved = eq.get_evidence_package_full_path()
        expected = RepositoryPath.ENGINEERING_EVIDENCE.value / "Test_Package"
        assert resolved == expected.resolve(), f"Expected {expected}, got {resolved}"

    def test_authority_path_without_prefix_still_resolves(self):
        """Fallback: path without '../questions/' prefix resolves relative to register dir."""
        eq = EngineeringQuestion(
            eq_number="EQ-9999",
            title="Test",
            status="Active",
            authority_document_text="SomeFile.md",
            authority_document_path="SomeFile.md",
            evidence_text="Test",
            evidence_path="SomeDir/",
            outcome="Approved",
            repository_location="docs/engineering/"
        )
        resolved = eq.get_authority_document_full_path()
        register_dir = RepositoryPath.ENGINEERING_REGISTER.value.parent
        expected = (register_dir / "SomeFile.md").resolve()
        assert resolved == expected, f"Expected {expected}, got {resolved}"


class TestEngineeringQuestionValidation:
    """Verify all validation methods for EngineeringQuestion."""

    def test_missing_authority_document(self):
        """Authority document that doesn't exist on filesystem."""
        eq = EngineeringQuestion(
            eq_number="EQ-9999",
            title="Missing Auth Doc",
            status="Completed",
            authority_document_text="NonExistent.md",
            authority_document_path="../questions/NonExistent.md",
            evidence_text="Evidence",
            evidence_path="../evidence/EQ_0010/",
            outcome="Approved",
            repository_location="docs/engineering/"
        )
        full_path = eq.get_authority_document_full_path()
        assert not full_path.exists(), "Non-existent file should not exist"

    def test_missing_evidence_package(self):
        """Evidence package directory that doesn't exist on filesystem."""
        eq = EngineeringQuestion(
            eq_number="EQ-9999",
            title="Missing Evidence",
            status="Completed",
            authority_document_text="EQ_0010_Deterministic_BOQ_Structural_Intelligence.md",
            authority_document_path="../questions/EQ_0010_Deterministic_BOQ_Structural_Intelligence.md",
            evidence_text="Evidence",
            evidence_path="../evidence/NonExistentDir/",
            outcome="Approved",
            repository_location="docs/engineering/"
        )
        full_path = eq.get_evidence_package_full_path()
        assert not full_path.exists(), "Non-existent directory should not exist"

    def test_broken_relative_path(self):
        """Path that doesn't match expected format."""
        eq = EngineeringQuestion(
            eq_number="EQ-9999",
            title="Broken Path",
            status="Completed",
            authority_document_text="Doc.md",
            authority_document_path="../../../etc/passwd",
            evidence_text="Evidence",
            evidence_path="../../../tmp/",
            outcome="Approved",
            repository_location="docs/engineering/"
        )
        assert not eq.validate_authority_document_path(), "Broken path should fail validation"
        assert not eq.validate_evidence_path(), "Broken path should fail validation"
        # Ensure path still resolves (fallback) but doesn't exist
        resolved_auth = eq.get_authority_document_full_path()
        assert not resolved_auth.exists(), "Broken relative path should not resolve to real file"

    def test_duplicate_eq_numbers(self):
        """Two EQ objects with same EQ number."""
        eq1 = EngineeringQuestion(
            eq_number="EQ-0001", title="First", status="Active",
            authority_document_text="A.md", authority_document_path="../questions/A.md",
            evidence_text="E", evidence_path="../evidence/A/",
            outcome="Outcome", repository_location="docs/engineering/"
        )
        eq2 = EngineeringQuestion(
            eq_number="EQ-0001", title="Second", status="Active",
            authority_document_text="B.md", authority_document_path="../questions/B.md",
            evidence_text="E", evidence_path="../evidence/B/",
            outcome="Outcome", repository_location="docs/engineering/"
        )
        assert eq1.eq_number == eq2.eq_number, "Same EQ number means duplicate"

    def test_invalid_status(self):
        """Status not in valid statuses list."""
        for bad_status in ["Invalid", "pending", "COMPLETED", "", "Frozen-Approved"]:
            eq = EngineeringQuestion(
                eq_number="EQ-0001", title="Test", status=bad_status,
                authority_document_text="A.md", authority_document_path="../questions/A.md",
                evidence_text="E", evidence_path="../evidence/A/",
                outcome="Outcome", repository_location="docs/engineering/"
            )
            assert not eq.validate_status(), f"Status '{bad_status}' should be invalid"

    def test_invalid_repository_location(self):
        """Repository location not matching expected."""
        for bad_location in ["docs/", "docs/Engineering/", "src/", "", "docs/engineering/questions/"]:
            eq = EngineeringQuestion(
                eq_number="EQ-0001", title="Test", status="Active",
                authority_document_text="A.md", authority_document_path="../questions/A.md",
                evidence_text="E", evidence_path="../evidence/A/",
                outcome="Outcome", repository_location=bad_location
            )
            assert not eq.validate_repository_location(), f"Location '{bad_location}' should be invalid"

    def test_empty_fields(self):
        """EQ with empty required fields."""
        eq = EngineeringQuestion(
            eq_number="EQ-0001", title="", status="Active",
            authority_document_text="", authority_document_path="../questions/A.md",
            evidence_text="E", evidence_path="../evidence/A/",
            outcome="", repository_location=""
        )
        assert eq.title.strip() == ""
        assert eq.outcome.strip() == ""
        assert not eq.validate_repository_location()

    def test_valid_statuses_all_pass(self):
        """All valid statuses recognized."""
        for valid_status in ["Completed", "Active", "Draft", "Frozen"]:
            eq = EngineeringQuestion(
                eq_number="EQ-0001", title="Test", status=valid_status,
                authority_document_text="A.md", authority_document_path="../questions/A.md",
                evidence_text="E", evidence_path="../evidence/A/",
                outcome="Outcome", repository_location="docs/engineering/"
            )
            assert eq.validate_status(), f"Status '{valid_status}' should be valid"

    def test_path_format_validation_edge_cases(self):
        """Edge cases for path format validation."""
        # Missing .md extension
        eq_no_ext = EngineeringQuestion(
            eq_number="EQ-0001", title="Test", status="Active",
            authority_document_text="A", authority_document_path="../questions/A",
            evidence_text="E", evidence_path="../evidence/A/",
            outcome="Outcome", repository_location="docs/engineering/"
        )
        assert not eq_no_ext.validate_authority_document_path()

        # Missing trailing slash on evidence
        eq_no_slash = EngineeringQuestion(
            eq_number="EQ-0001", title="Test", status="Active",
            authority_document_text="A.md", authority_document_path="../questions/A.md",
            evidence_text="E", evidence_path="../evidence/A",
            outcome="Outcome", repository_location="docs/engineering/"
        )
        assert not eq_no_slash.validate_evidence_path()

        # Wrong prefix
        eq_wrong_prefix = EngineeringQuestion(
            eq_number="EQ-0001", title="Test", status="Active",
            authority_document_text="A.md", authority_document_path="./questions/A.md",
            evidence_text="E", evidence_path="./evidence/A/",
            outcome="Outcome", repository_location="docs/engineering/"
        )
        assert not eq_wrong_prefix.validate_authority_document_path()
        assert not eq_wrong_prefix.validate_evidence_path()


class TestParserDeterminism:
    """Verify EngineeringRegisterParser is deterministic."""

    def test_repeated_parse_identical(self):
        """Multiple parses produce identical results."""
        results = []
        for _ in range(5):
            success, findings, eq_entries = EngineeringRegisterParser.parse_register()
            results.append((success, len(findings), len(eq_entries)))

        # All results must be identical
        assert all(r == results[0] for r in results), \
            f"Non-deterministic parse results: {results}"

    def test_eq_numbers_unique_and_ordered(self):
        """Verify no duplicate EQ numbers and entries are in register order."""
        _, _, eq_entries = EngineeringRegisterParser.parse_register()
        eq_nums = [eq.eq_number for eq in eq_entries]
        assert len(eq_nums) == len(set(eq_nums)), f"Duplicate EQ numbers: {eq_nums}"
        # Verify sorted order matches register order (EQ-0010 through EQ-0017)
        assert eq_nums == sorted(eq_nums, key=lambda x: int(x.split('-')[1])), \
            "EQ entries not in numeric order"

    def test_every_entry_has_all_nine_fields(self):
        """Each parsed entry has exactly 9 fields populated."""
        _, _, eq_entries = EngineeringRegisterParser.parse_register()
        for eq in eq_entries:
            fields = [
                eq.eq_number, eq.title, eq.status,
                eq.authority_document_text, eq.authority_document_path,
                eq.evidence_text, eq.evidence_path,
                eq.outcome, eq.repository_location
            ]
            assert all(f.strip() for f in fields), \
                f"Empty field in {eq.eq_number}: fields={dict(zip(
                    ['number','title','status','auth_text','auth_path',
                     'ev_text','ev_path','outcome','repo_loc'], fields))}"

    def test_field_values_match_register(self):
        """Verify key field values against known register contents."""
        _, _, eq_entries = EngineeringRegisterParser.parse_register()
        eq_map = {eq.eq_number: eq for eq in eq_entries}

        # EQ-0010 specific checks
        eq10 = eq_map["EQ-0010"]
        assert eq10.title == "Deterministic BOQ Structural Intelligence"
        assert eq10.status == "Completed"
        assert eq10.outcome == "Approved"
        assert eq10.repository_location == "docs/engineering/"
        assert eq10.authority_document_text == "EQ_0010_Deterministic_BOQ_Structural_Intelligence.md"
        assert eq10.evidence_text == "evidence/EQ_0010/"

        # EQ-0017 (last entry) specific checks
        eq17 = eq_map["EQ-0017"]
        assert eq17.title == "Repository Governance Migration"
        assert eq17.status == "Completed"
        assert eq17.outcome == "Approved"
        assert eq17.authority_document_text == "EQ_0017_Repository_Governance_Migration.md"
        assert eq17.evidence_text == "evidence/EQ_0017/"

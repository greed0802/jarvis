"""Stable Presentation Identity (IP-0006, Part A).

Immutable, renderer-independent identifiers for presentation items.
Presentation IDs are stable across all rendering technologies (GUI, CLI,
PDF, HTML, JSON, CSV, Markdown) and never expose internal engine
identifiers.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - IP-0006 — CheckMate Review Session & Human Workflow
"""

from __future__ import annotations

from dataclasses import dataclass
import enum


class PresentationIdPrefix(enum.Enum):
    """Stable prefix for presentation identity."""
    FINDING = "PF"
    RECOMMENDATION = "PR"
    SECTION = "PS"
    NAVIGATION = "PN"


@dataclass(frozen=True)
class PresentationId:
    """Immutable, renderer-independent presentation identity.

    Stable across all rendering technologies. Does NOT expose rule
    IDs, engine identifiers, or platform details.

    Attributes:
        prefix: Type prefix (PF, PR, PS, PN).
        numeric_id: Zero-padded numeric component.
    """

    prefix: PresentationIdPrefix
    numeric_id: str

    @classmethod
    def for_finding(cls, index: int) -> PresentationId:
        """Create a PresentationId for a finding.

        Args:
            index: Zero-based index (may reference display order).

        Returns:
            PF-XXXXXX formatted ID.
        """
        return cls(prefix=PresentationIdPrefix.FINDING, numeric_id=f"{index + 1:06d}")

    @classmethod
    def for_recommendation(cls, index: int) -> PresentationId:
        """Create a PresentationId for a recommendation."""
        return cls(prefix=PresentationIdPrefix.RECOMMENDATION, numeric_id=f"{index + 1:06d}")

    @classmethod
    def for_section(cls, index: int) -> PresentationId:
        """Create a PresentationId for a section."""
        return cls(prefix=PresentationIdPrefix.SECTION, numeric_id=f"{index + 1:06d}")

    @classmethod
    def for_navigation(cls, index: int) -> PresentationId:
        """Create a PresentationId for a navigation item."""
        return cls(prefix=PresentationIdPrefix.NAVIGATION, numeric_id=f"{index + 1:06d}")

    def to_external(self) -> str:
        """Render the ID as a stable external string (e.g., 'PF-000001')."""
        return f"{self.prefix.value}-{self.numeric_id}"

    def __str__(self) -> str:
        return self.to_external()

    def __hash__(self) -> int:
        return hash(self.to_external())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PresentationId):
            return NotImplemented
        return self.to_external() == other.to_external()
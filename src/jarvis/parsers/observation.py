"""
HISTORICAL ENGINEERING — ADR_0025 REJECTED ARCHITECTURE

Engineering Traceability

ADR: ADR_0025 (rejected 2026-07-11)
Classification: Historical Engineering (2026-07-13)
See also: Repository Knowledge Preservation Strategy (Draft v1.0)

This module is not part of the supported production dependency graph.

--- Original docstring preserved below ---

Observation ontology runtime types.

The runtime types defined here are an implementation of the Observation ontology
and SHALL remain structurally consistent with the ontology documents. Divergence
between runtime types and ontology definitions is considered an architectural defect.

These types are platform ontology runtime types produced by parsers for
consumption by downstream platform components (Memory, Evidence, Validation,
Context Engine).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping


@dataclass(frozen=True)
class Provenance:
    """Provenance records the Source identifier, Observer, and Procedure for an Observation.

    Together with the Observation's identity, Provenance enables full traceability
    and reproducibility as defined in observation_acquisition.md.
    """

    source_identifier: str
    observer: str
    procedure: str
    timestamp: datetime


@dataclass(frozen=True)
class Observation:
    """Observation is the base type for all observations.

    An Observation is an immutable, deterministic record of one or more
    observable properties directly acquired from a specific source by a specific
    observer, without interpretation or inference.

    Invariants:
    - observation_id SHALL be unique within its ObservationSet.
    - observation_id SHALL be deterministic under equivalent acquisition conditions.
    - provenance SHALL be immutable.
    """

    observation_id: str
    provenance: Provenance


@dataclass(frozen=True)
class ObservationSet:
    """ObservationSet is an immutable container of Observations from one acquisition run.

    ObservationSet owns acquisition session metadata (acquisition_id, timestamp).
    Individual Observations within the set retain their own provenance.

    Invariants:
    - ObservationSet SHALL contain at least one Observation.
    - ObservationSet SHALL NOT modify contained Observations.
    - ObservationSet SHALL be immutable once created.
    """

    acquisition_id: str
    timestamp: datetime
    observations: tuple[Observation, ...]

    def __post_init__(self) -> None:
        """Validate invariants after dataclass initialization."""
        if not self.observations:
            raise ValueError("ObservationSet SHALL contain at least one Observation")


@dataclass(frozen=True)
class WorkbookObservation(Observation):
    """WorkbookObservation records workbook-level observable properties.

    This is a specialization of Observation. It extends Observation only by
    specifying which observable properties are within scope for a workbook source.

    Observable properties (in scope):
    - Source identity (via provenance)
    - File format (.xlsx, .xls, .xlsb)
    - Format version where applicable
    - Creator or author
    - Creation timestamp
    - Last modified timestamp
    - Application that produced the workbook
    - Calculation mode
    - Date system (1900 or 1904)
    - Worksheet count
    - Worksheet names in workbook order
    - Structure protection state
    - Window protection state
    - Visibility state

    Note: worksheet_name is NOT included here because WorkbookObservation
    observes the workbook container, not worksheet content. Worksheet relationships
    are captured through provenance and ordering in the ObservationSet.

    Non-observable (out of scope):
    - Worksheet contents (rows, cells, values, formulas)
    - Named ranges
    - BOQ sections or any domain-specific classification
    """

    file_format: str | None
    format_version: str | None
    creator: str | None
    created: datetime | None
    modified: datetime | None
    application: str | None
    calculation_mode: str | None
    date_system: str | None
    worksheet_count: int
    worksheet_names: tuple[str, ...]
    structure_protection: bool | None
    window_protection: bool | None
    visibility: str | None


@dataclass(frozen=True)
class WorksheetObservation(Observation):
    """WorksheetObservation records worksheet-level observable properties.

    This is a specialization of Observation. It extends Observation only by
    specifying which observable properties are within scope for a worksheet source.

    Observable properties (in scope):
    - Source identity (via provenance)
    - Worksheet identifier (name or index)
    - Worksheet name
    - Worksheet index
    - Visibility state
    - Row count
    - Column count
    - Merged ranges (coordinate ranges)
    - Freeze panes (frozen row/column boundaries)
    - Auto filter range
    - Print area
    - Hidden rows (indices)
    - Hidden columns (indices)

    Non-observable (out of scope):
    - Cell values (belong to CellObservation)
    - Cell formatting
    - Classification of rows (Header, Item, etc.)
    """

    worksheet_name: str
    worksheet_index: int
    visibility: str | None
    row_count: int
    column_count: int
    merged_ranges: tuple[str, ...]
    freeze_panes: tuple[int, int] | None
    auto_filter: str | None
    print_area: str | None
    hidden_rows: tuple[int, ...]
    hidden_columns: tuple[int, ...]


@dataclass(frozen=True)
class RowObservation(Observation):
    """RowObservation records row-level observable properties.

    This is a specialization of Observation. It extends Observation only by
    specifying which observable properties are within scope for a row source.

    Observable properties (in scope):
    - Source identity (via provenance)
    - Worksheet identifier (worksheets are the parent container for rows)
    - Row identifier (row number)
    - Row number
    - Visibility state
    - Height

    Note: worksheet_name is included because a row is observed within a specific
    worksheet context, and this relationship is an observable property, not
    provenance. The row's container worksheet is part of what is directly seen.

    Non-observable (out of scope):
    - Cell values (belong to CellObservation)
    - Cell count (ambiguous across formats)
    - Classification of row (Header, Item, Heading, Note)
    """

    worksheet_name: str
    row_number: int
    visibility: str | None
    height: float | None


@dataclass(frozen=True)
class CellObservation(Observation):
    """CellObservation records cell-level observable properties.

    This is a specialization of Observation. It extends Observation only by
    specifying which observable properties are within scope for a cell source.

    Observable properties (in scope):
    - Coordinate (row, column, reference)
    - Raw value (string, number, boolean, date, error)
    - Formula expression
    - Calculated value
    - Data type (string, number, boolean, date, datetime, error)
    - Number format mask
    - Font attributes (typeface, size, bold, italic, underline, color, strikethrough)
    - Fill attributes (background color, pattern style, pattern color)
    - Alignment attributes (horizontal, vertical, wrap text, indent, rotation)
    - Border attributes (style and color for top, bottom, left, right, diagonal)
    - Protection state (locked, hidden)
    - Merged state
    - Comment content

    Note: font, fill, alignment, border use Mapping for deep immutability.
    These fields will be None until acquired in a later procedure.

    Non-observable (out of scope):
    - Interpretation of the cell's value (quantity, description, rate, etc.)
    - Classification of the cell's role
    - Validation of the cell's value
    - Business semantics
    """

    worksheet_name: str
    row: int
    column: int
    reference: str | None
    value: Any | None
    formula: str | None
    calculated_value: Any | None
    data_type: str | None
    number_format: str | None
    font: Mapping[str, Any] | None
    fill: Mapping[str, Any] | None
    alignment: Mapping[str, Any] | None
    border: Mapping[str, Any] | None
    locked: bool | None
    hidden: bool | None
    merged: bool | None
    comment: str | None
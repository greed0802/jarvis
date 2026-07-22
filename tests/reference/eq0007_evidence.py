"""Accepted engineering evidence for BOQ Intelligence acceptance testing.

This module is the single source of truth for production regression tests.

Authority:
- Engineering Question: EQ-0007 (Accepted)
- Cross-validated by: EQ-0009
- Fixture: tests/fixtures/costx/full_boq.xlsx
- Fixture identity verified through tests/fixtures/fixtures.json

Any change to these values requires:
1. New engineering evidence
2. Project Owner approval
3. Update to this module

Status: ACCEPTED
"""

ROW_CLASSIFICATION = {
    "Head": 2011,
    "Note": 520,
    "Section": 15,
    "Item": 3605,
    "Other": 198,
}

SECTION_STATISTICS = {
    "OMISSION": {
        "negative_qty": 169,
        "positive_qty": 7,
    },
    "ADDITION": {
        "negative_qty": 0,
        "positive_qty": 3,
    },
}

KNOWN_ANOMALIES = [
    {"row_number": 6202, "code": "BE/2", "quantity": 21.0, "section": "OMISSION"},
    {"row_number": 6343, "code": "BH/24", "quantity": 6.0, "section": "OMISSION"},
    {"row_number": 6344, "code": "BH/25", "quantity": 4.0, "section": "OMISSION"},
    {"row_number": 6345, "code": "BH/26", "quantity": 1.0, "section": "OMISSION"},
    {"row_number": 6346, "code": "BH/27", "quantity": 3.0, "section": "OMISSION"},
    {"row_number": 6347, "code": "BH/28", "quantity": 5.0, "section": "OMISSION"},
    {"row_number": 6348, "code": "BH/29", "quantity": 5.0, "section": "OMISSION"},
]

TOTAL_ROWS = 6349
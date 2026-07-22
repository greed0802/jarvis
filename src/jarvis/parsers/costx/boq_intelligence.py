"""BOQ Intelligence — Increment 1 + Increment 2 + Increment 3.

Pure functions that analyze extracted BOQ rows to produce structured
intelligence: classification summary, statistics, section analysis,
hierarchy reconstruction, known anomaly reporting, and structural detection evidence.

Operates entirely over list[BOQRow]. No parser modifications, no runtime
integration, no kernel changes.

Authority:
- Capability Evaluation 001 (Increment 1 — Approved)
- EQ-0007 Production Extraction Report (Increment 1)
- EQ-0009 Context Discovery Report (Increment 1)
- EQ-0010 Deterministic BOQ Structural Intelligence (Increment 2 — Approved)
- EQ-0011 BOQ Semantic Intelligence Boundary (Increment 3 — Approved)
"""

from __future__ import annotations

from dataclasses import dataclass

from jarvis.parsers.costx.boq_extraction import BOQRow

_VALID_ROW_TYPES = frozenset({"Head", "Note", "Section", "Item", "Other"})


@dataclass(frozen=True)
class BOQHeaderNode:
    """Header node in reconstructed BOQ hierarchy.
    
    Evidence: EQ-0010 Spike 4 (hierarchy reconstruction algorithm).
    
    Represents a single header (Head1-5) in the deterministic tree structure
    built from linear BOQRow sequence using stack-based reconstruction.
    """

    level: int  # Head1→1, Head2→2, etc. (Spike 2)
    row_number: int  # Original BOQRow.row_number (Spike 1)
    uom: str  # Original UOM string (Spike 1)
    description: str | None  # Original description (Spike 1)
    section: str | None  # Original section context (Spike 1)
    depth: int  # Computed depth in tree (Spike 4)
    parent_row_number: int | None  # Parent's row_number, None for roots (Spike 4)
    children_headers: tuple[BOQHeaderNode, ...]  # Child header nodes (Spike 4)
    children_items: tuple[dict[str, int | str | float | None], ...]  # Child items (Spike 4)

@dataclass(frozen=True)
class BOQIntelligenceResult:
    """Immutable analysis result from BOQ Intelligence Increment 1 + Increment 2 + Increment 3.

    Frozen dataclass provides shallow immutability. Deep immutability
    may be revisited if a future consumer requires it.
    """

    row_classification: dict[str, int]
    section_statistics: dict[str, dict[str, int]]
    boq_statistics: dict[str, int | float]
    known_anomalies: list[dict[str, int | str | float]]
    hierarchy: tuple[BOQHeaderNode, ...] | None = None  # Root headers (Spike 4)
    hierarchy_statistics: dict[str, int | float] | None = None  # Hierarchy stats (Spike 4)
    detected_level_skips: tuple[dict[str, int], ...] | None = None  # Increment 3: Level skip evidence
    zero_quantity_items: tuple[dict[str, int | str | float | None], ...] | None = None  # Increment 3: Zero quantity evidence
    structural_containment_findings: tuple[dict[str, int], ...] | None = None  # Increment 3: Structural containment evidence
    completeness_findings: tuple[dict[str, int | str], ...] | None = None  # Increment 3: Basic completeness evidence


def analyze_boq(rows: list[BOQRow], *, include_hierarchy: bool = False, include_detection: bool = False) -> BOQIntelligenceResult:
    """Analyze extracted BOQ rows and produce intelligence result.
    
    Increment 1 provides: row classification, section statistics, BOQ statistics,
    known anomalies.
    
    Increment 2 provides (if include_hierarchy=True): hierarchy reconstruction,
    hierarchy statistics.
    
    Increment 3 provides (if include_detection=True): structural detection evidence
    (level skips, zero quantities, structural containment, basic completeness).

    Args:
        rows: Extracted BOQ rows from extract_boq().
        include_hierarchy: If True, perform hierarchy reconstruction (Increment 2).
                          Default False for backward compatibility.
        include_detection: If True, perform structural detection evidence (Increment 3).
                          Default False for backward compatibility. Requires include_hierarchy=True.

    Returns:
        Immutable BOQIntelligenceResult with requested analysis.
    """
    hierarchy = None
    hierarchy_statistics = None
    detected_level_skips = None
    zero_quantity_items = None
    structural_containment_findings = None
    completeness_findings = None
    
    if include_hierarchy:
        hierarchy = _reconstruct_hierarchy(rows)
        hierarchy_statistics = _compute_hierarchy_statistics(hierarchy)
    
    if include_detection and hierarchy:
        detected_level_skips = _detect_level_skips(hierarchy)
        zero_quantity_items = _detect_zero_quantities(rows)
        structural_containment_findings = _detect_structural_containment(hierarchy)
        completeness_findings = _detect_basic_completeness(rows, hierarchy)
    
    return BOQIntelligenceResult(
        row_classification=_count_row_types(rows),
        section_statistics=_compute_section_stats(rows),
        boq_statistics=_compute_boq_stats(rows),
        known_anomalies=_detect_anomalies(rows),
        hierarchy=hierarchy,
        hierarchy_statistics=hierarchy_statistics,
        detected_level_skips=detected_level_skips,
        zero_quantity_items=zero_quantity_items,
        structural_containment_findings=structural_containment_findings,
        completeness_findings=completeness_findings,
    )


def _count_row_types(rows: list[BOQRow]) -> dict[str, int]:
    counts: dict[str, int] = {"Head": 0, "Note": 0, "Section": 0, "Item": 0, "Other": 0}
    for row in rows:
        if row.row_type not in _VALID_ROW_TYPES:
            raise ValueError(f"Unknown row type: {row.row_type!r}")
        counts[row.row_type] += 1
    return counts


def _compute_boq_stats(rows: list[BOQRow]) -> dict[str, int | float]:
    total = len(rows)
    code_rows = sum(1 for r in rows if r.code is not None)
    description_rows = sum(1 for r in rows if r.description is not None)
    quantity_rows = sum(1 for r in rows if r.quantity is not None)
    uom_rows = sum(1 for r in rows if r.uom is not None)
    section_rows = sum(1 for r in rows if r.section is not None)

    return {
        "total_rows": total,
        "code_rows": code_rows,
        "description_rows": description_rows,
        "quantity_rows": quantity_rows,
        "uom_rows": uom_rows,
        "section_rows": section_rows,
    }


def _compute_section_stats(rows: list[BOQRow]) -> dict[str, dict[str, int]]:
    sections: dict[str, dict[str, int]] = {}

    for row in rows:
        if row.section is None:
            continue
        if row.section not in sections:
            sections[row.section] = {"negative_qty": 0, "positive_qty": 0}
        if row.quantity is not None:
            if row.quantity < 0:
                sections[row.section]["negative_qty"] += 1
            elif row.quantity > 0:
                sections[row.section]["positive_qty"] += 1

    return dict(sorted(sections.items()))


def _detect_anomalies(rows: list[BOQRow]) -> list[dict[str, int | str | float]]:
    anomalies: list[dict[str, int | str | float]] = []
    for row in rows:
        if (
            row.section == "OMISSION"
            and row.quantity is not None
            and row.quantity > 0
        ):
            anomalies.append({
                "row_number": row.row_number,
                "code": row.code,
                "quantity": row.quantity,
                "section": row.section,
            })
    return sorted(anomalies, key=lambda a: a["row_number"])

# --- Increment 2: Hierarchy Reconstruction ---
# Evidence: EQ-0010 Spike 4

def _extract_head_level(uom: str | None) -> int | None:
    """Extract numeric level from Head1-5 UOM string.
    
    Evidence: EQ-0010 Spike 2 (UOM pattern analysis).
    
    Args:
        uom: UOM string from BOQRow.
        
    Returns:
        Numeric level (1-5) if Head1-5, None otherwise.
    """
    if uom and uom.startswith("Head") and len(uom) == 5 and uom[4].isdigit():
        return int(uom[4])
    return None

def _reconstruct_hierarchy(rows: list[BOQRow]) -> tuple[BOQHeaderNode, ...]:
    """Reconstruct heading tree using deterministic stack algorithm.
    
    Evidence: EQ-0010 Spike 4 (hierarchy reconstruction).
    Algorithm: Stack-based reconstruction from Spike 4.
    
    Args:
        rows: Extracted BOQ rows.
        
    Returns:
        Tuple of root header nodes representing the reconstructed hierarchy.
    """
    tree: list[BOQHeaderNode] = []  # Root-level headers
    stack: list[dict] = []  # Current path (mutable during construction)
    
    for row in rows:
        if row.row_type == "Head" and row.uom:
            level = _extract_head_level(row.uom)
            if level is None:
                continue
            
            # Mutable node during construction
            node = {
                "level": level,
                "row_number": row.row_number,
                "uom": row.uom,
                "description": row.description,
                "section": row.section,
                "depth": 0,
                "parent_row_number": None,
                "children_headers": [],
                "children_items": [],
            }
            
            # Pop stack while top level >= current level
            while stack and stack[-1]["level"] >= level:
                stack.pop()
            
            # Assign parent and depth
            if stack:
                parent = stack[-1]
                parent["children_headers"].append(node)
                node["depth"] = parent["depth"] + 1
                node["parent_row_number"] = parent["row_number"]
            else:
                tree.append(node)
                node["depth"] = 1
                node["parent_row_number"] = None
            
            stack.append(node)
            
        elif row.row_type == "Item":
            if stack:
                stack[-1]["children_items"].append({
                    "row_number": row.row_number,
                    "code": row.code,
                    "description": row.description,
                    "quantity": row.quantity,
                    "uom": row.uom,
                })
    
    # Convert mutable tree to immutable BOQHeaderNode tree
    return tuple(_freeze_node(node) for node in tree)

def _freeze_node(node: dict) -> BOQHeaderNode:
    """Convert mutable node dict to immutable BOQHeaderNode.
    
    Recursively freezes all children headers.
    """
    return BOQHeaderNode(
        level=node["level"],
        row_number=node["row_number"],
        uom=node["uom"],
        description=node["description"],
        section=node["section"],
        depth=node["depth"],
        parent_row_number=node["parent_row_number"],
        children_headers=tuple(_freeze_node(c) for c in node["children_headers"]),
        children_items=tuple(node["children_items"]),
    )

def _compute_hierarchy_statistics(tree: tuple[BOQHeaderNode, ...]) -> dict[str, int | float]:
    """Compute hierarchy statistics from reconstructed tree.
    
    Evidence: EQ-0010 Spike 4 (depth distribution, items-per-header).
    
    Args:
        tree: Root headers from hierarchy reconstruction.
        
    Returns:
        Dictionary of hierarchy statistics.
    """
    if not tree:
        return {
            "total_headers": 0,
            "root_headers": 0,
            "depth_distribution": {},
            "items_per_header_by_uom": {},
        }
    
    # Collect all nodes via traversal
    all_nodes: list[BOQHeaderNode] = []
    
    def traverse(node: BOQHeaderNode) -> None:
        all_nodes.append(node)
        for child in node.children_headers:
            traverse(child)
    
    for root in tree:
        traverse(root)
    
    # Depth distribution
    depth_dist: dict[int, int] = {}
    for node in all_nodes:
        depth_dist[node.depth] = depth_dist.get(node.depth, 0) + 1
    
    # Items per header by UOM
    items_by_uom: dict[str, list[int]] = {}
    for node in all_nodes:
        if node.uom not in items_by_uom:
            items_by_uom[node.uom] = []
        items_by_uom[node.uom].append(len(node.children_items))
    
    items_per_header: dict[str, float] = {}
    for uom, counts in items_by_uom.items():
        items_per_header[uom] = sum(counts) / len(counts) if counts else 0.0
    
    return {
        "total_headers": len(all_nodes),
        "root_headers": len(tree),
        "depth_distribution": depth_dist,
        "items_per_header_by_uom": items_per_header,
    }

# --- Increment 3: Structural Detection Evidence ---
# Evidence: EQ-0011 Spike 2, Spike 3, Spike 4

def _detect_level_skips(tree: tuple[BOQHeaderNode, ...]) -> tuple[dict[str, int], ...]:
    """Detect level skip evidence in reconstructed hierarchy.
    
    Evidence: EQ-0010 Spike 4, EQ-0011 Spike 2, EQ-0011 Spike 3.
    
    Records observable facts about level skips: parent level, child level,
    skip magnitude, row numbers. Does not assess legitimacy.
    
    Args:
        tree: Root headers from hierarchy reconstruction.
        
    Returns:
        Tuple of level skip evidence dicts.
    """
    skips: list[dict[str, int]] = []
    
    def traverse(node: BOQHeaderNode) -> None:
        for child in node.children_headers:
            level_delta = child.level - node.level
            if level_delta > 1:
                skips.append({
                    "parent_row_number": node.row_number,
                    "parent_level": node.level,
                    "child_row_number": child.row_number,
                    "child_level": child.level,
                    "skip_magnitude": level_delta - 1,
                })
            traverse(child)
    
    for root in tree:
        traverse(root)
    
    return tuple(skips)

def _detect_zero_quantities(rows: list[BOQRow]) -> tuple[dict[str, int | str | float | None], ...]:
    """Detect zero quantity evidence in Item rows.
    
    Evidence: EQ-0010 Spike 1, EQ-0011 Spike 2, EQ-0011 Spike 3.
    
    Records observable facts about items with quantity == 0.0.
    Does not assess acceptability.
    
    Args:
        rows: Extracted BOQ rows.
        
    Returns:
        Tuple of zero quantity evidence dicts.
    """
    zero_items: list[dict[str, int | str | float | None]] = []
    
    for row in rows:
        if row.row_type == "Item" and row.quantity == 0.0:
            zero_items.append({
                "row_number": row.row_number,
                "code": row.code,
                "description": row.description,
                "section": row.section,
                "quantity": row.quantity,
                "uom": row.uom,
            })
    
    return tuple(zero_items)

def _detect_structural_containment(tree: tuple[BOQHeaderNode, ...]) -> tuple[dict[str, int], ...]:
    """Detect structural containment evidence in reconstructed hierarchy.
    
    Evidence: EQ-0010 Spike 4, EQ-0011 Spike 3.
    
    Verifies structural hierarchy relationships only (child_level <= parent_level).
    Records observable facts about structural inversions.
    Does not perform semantic scope assessment.
    
    Args:
        tree: Root headers from hierarchy reconstruction.
        
    Returns:
        Tuple of structural containment evidence dicts.
    """
    inversions: list[dict[str, int]] = []
    
    def traverse(node: BOQHeaderNode) -> None:
        for child in node.children_headers:
            if child.level > node.level:
                # This should never occur given stack algorithm, but check anyway
                inversions.append({
                    "parent_row_number": node.row_number,
                    "parent_level": node.level,
                    "child_row_number": child.row_number,
                    "child_level": child.level,
                })
            traverse(child)
    
    for root in tree:
        traverse(root)
    
    return tuple(inversions)

def _detect_basic_completeness(rows: list[BOQRow], tree: tuple[BOQHeaderNode, ...]) -> tuple[dict[str, int | str], ...]:
    """Detect basic completeness evidence for sections.
    
    Evidence: EQ-0010 Spike 3, EQ-0011 Spike 3.
    
    Records observable facts about sections with zero measurable items.
    Does not assess project completeness.
    
    Args:
        rows: Extracted BOQ rows.
        tree: Root headers from hierarchy reconstruction.
        
    Returns:
        Tuple of completeness evidence dicts.
    """
    # Group Items by section
    section_items: dict[str, int] = {}
    for row in rows:
        if row.row_type == "Item" and row.section:
            section_items[row.section] = section_items.get(row.section, 0) + 1
    
    # Find sections with zero items
    empty_sections: list[dict[str, int | str]] = []
    
    # Collect all sections mentioned in headers
    all_sections: set[str] = set()
    
    def collect_sections(node: BOQHeaderNode) -> None:
        if node.section:
            all_sections.add(node.section)
        for child in node.children_headers:
            collect_sections(child)
    
    for root in tree:
        collect_sections(root)
    
    for section in sorted(all_sections):
        item_count = section_items.get(section, 0)
        if item_count == 0:
            empty_sections.append({
                "section": section,
                "item_count": item_count,
            })
    
    return tuple(empty_sections)

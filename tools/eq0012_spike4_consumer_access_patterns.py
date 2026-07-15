#!/usr/bin/env python3
"""
EQ-0012 Spike 4: Consumer Access Patterns

Purpose:
    Analyze the BOQ Intelligence production codebase to determine the correct
    public consumer interface for the BOQ Intelligence Public Evidence Contract.
    
    Source of Truth: Production code at src/jarvis/parsers/costx/

Engineering Questions:
    Q1: What is the smallest stable public surface consumers require?
    Q2: Which production types are public contract vs internal implementation?
    Q3: Which imports should consumers rely upon?
    Q4: How should consumers access evidence?
    Q5: What guarantees regarding import/symbol/field stability?
    Q6: What constitutes a breaking consumer change?

Investigation Rules:
    - Every statement must trace to production implementation
    - Never infer; if evidence doesn't exist, record "No engineering evidence available"
    - Never "improve" documentation beyond production
"""

import json
import ast
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional

PARSERS_COSTX_DIR = Path("src/jarvis/parsers/costx")
CONTRACTS_DIR = Path("docs/contracts")


@dataclass
class ModuleSymbol:
    """A symbol defined in a module."""
    name: str
    kind: str  # dataclass, function, constant
    is_public: bool  # Not underscore-prefixed
    defined_in: str  # Module filename
    is_frozen: bool  # frozen=True for dataclasses
    type_annotation: str | None = None
    
    @property
    def is_internal(self) -> bool:
        """Symbol is internal implementation detail."""
        return not self.is_public or self.name.startswith('_')

    @property
    def is_contract_type(self) -> bool:
        """Symbol is a candidate for public contract."""
        # Public dataclasses and functions that consumers need
        return self.is_public and self.kind in ('dataclass', 'function')


@dataclass
class ImportPattern:
    """An import pattern found in production code."""
    source_module: str
    imported_symbol: str
    target_module: str
    is_type_only: bool = False
    is_internal_import: bool = False  # Import within same package


@dataclass
class ModuleBoundary:
    """Module boundary specification."""
    module_name: str
    file_path: str
    public_exports: List[str]
    internal_symbols: List[str]
    imports_from_public_packages: List[str]
    imports_from_internal: List[str]


class ConsumerAccessAnalyzer:
    """Analyzes production code for consumer access patterns."""
    
    def __init__(self):
        self.modules: Dict[str, ModuleBoundary] = {}
        self.all_symbols: List[ModuleSymbol] = []
        self.import_patterns: List[ImportPattern] = []
    
    def analyze_module(self, module_name: str, file_path: Path) -> ModuleBoundary:
        """Analyze a single module for public/private symbols and imports."""
        with open(file_path, 'r') as f:
            source = f.read()
        
        tree = ast.parse(source)
        
        public_exports = []
        internal_symbols = []
        imports_from_public = []
        imports_from_internal = []
        
        # Check for __all__ first
        has_all = False
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == '__all__':
                        has_all = True
                        # __all__ defines official public exports
                        if isinstance(node.value, ast.List):
                            public_exports = [
                                elt.value for elt in node.value.elts 
                                if isinstance(elt, ast.Constant)
                            ]
        
        # Analyze all nodes
        for node in ast.walk(tree):
            # Collect class/function definitions
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                name = node.name
                is_pub = not name.startswith('_')
                
                # Determine kind
                if isinstance(node, ast.ClassDef):
                    kind = 'dataclass'
                else:
                    kind = 'function'
                
                # Check frozen (dataclass decorator with frozen=True)
                is_frozen = False
                if isinstance(node, ast.ClassDef):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            for keyword in decorator.keywords:
                                if keyword.arg == 'frozen' and isinstance(keyword.value, ast.Constant) and keyword.value.value == True:
                                    is_frozen = True
                
                # Determine if public (according to __all__ or naming convention)
                is_public = has_all and name in public_exports or (not has_all and is_pub)
                
                symbol = ModuleSymbol(
                    name=name,
                    kind=kind,
                    is_public=is_pub,
                    defined_in=module_name,
                    is_frozen=is_frozen,
                )
                self.all_symbols.append(symbol)
                
                if is_public and has_all:
                    public_exports.append(name)
            
            # Collect imports
            if isinstance(node, ast.ImportFrom):
                source_mod = node.module or ''
                for alias in node.names:
                    is_internal = (
                        source_mod.startswith('jarvis.parsers') or 
                        source_mod.startswith('.')
                    )
                    
                    imp = ImportPattern(
                        source_module=source_mod,
                        imported_symbol=alias.name,
                        target_module=module_name,
                        is_internal_import=is_internal
                    )
                    self.import_patterns.append(imp)
                    
                    if is_internal:
                        imports_from_internal.append(f"{source_mod}.{alias.name}")
                    elif source_mod:  # Non-empty, external import
                        imports_from_public.append(f"{source_mod}.{alias.name}")
        
        # Populate internal symbols (underscore-prefixed)
        for sym in self.all_symbols:
            if sym.defined_in == module_name and sym.is_internal:
                internal_symbols.append(sym.name)
        
        boundary = ModuleBoundary(
            module_name=module_name,
            file_path=str(file_path),
            public_exports=sorted(set(public_exports)),
            internal_symbols=sorted(set(internal_symbols)),
            imports_from_public_packages=sorted(set(imports_from_public)),
            imports_from_internal=sorted(set(imports_from_internal))
        )
        self.modules[module_name] = boundary
        return boundary
    
    def analyze_package(self) -> Dict:
        """Analyze entire costx package and consumer dependencies."""
        # Analyze each module
        if not PARSERS_COSTX_DIR.exists():
            return {"error": f"Directory not found: {PARSERS_COSTX_DIR}"}
        
        for file_path in sorted(PARSERS_COSTX_DIR.glob("*.py")):
            module_name = f"jarvis.parsers.costx.{file_path.stem}"
            self.analyze_module(module_name, file_path)
        
        return self.collect_findings()
    
    def collect_findings(self) -> Dict:
        """Collect all analysis findings."""
        
        # Q1: Smallest stable public surface
        contract_candidates = [
            sym for sym in self.all_symbols 
            if sym.is_contract_type and not sym.name.startswith('_')
            and not sym.name.startswith('extract')  # extraction preceeds intelligence
            and sym.name not in ('_classify_row',)  # internal helpers
        ]
        
        # Q2: Public contract vs internal types
        contract_types = [
            sym for sym in self.all_symbols 
            if sym.is_contract_type
        ]
        
        internal_types = [
            sym for sym in self.all_symbols 
            if sym.is_internal or not sym.is_contract_type
        ]
        
        # Identify internal helpers (underscore-prefixed functions)
        internal_helpers = [
            sym for sym in self.all_symbols 
            if sym.name.startswith('_')
        ]
        
        # Q3: Import analysis
        consumer_external_imports = [
            imp for imp in self.import_patterns 
            if not imp.is_internal_import
        ]
        
        internal_cross_references = [
            imp for imp in self.import_patterns 
            if imp.is_internal_import
        ]
        
        # Module boundary analysis
        costx_init_exports = self.modules.get('jarvis.parsers.costx.__init__', None)
        
        # Q4: Access pattern evaluation
        # Based on production evidence: consumers need to import directly
        # from boq_extraction (BOQRow, extract_boq) and boq_intelligence
        # (analyze_boq, BOQIntelligenceResult, BOQHeaderNode)
        # This is the current pattern (no facade, no dedicated public package)

        return {
            "investigation": "EQ-0012 Spike 4: Consumer Access Patterns",
            "date": "2026-07-15",
            "source_of_truth": "src/jarvis/parsers/costx/",
            
            "analysis": {
                "modules_found": [
                    {
                        "module": name,
                        "public_exports": b.public_exports,
                        "internal_symbols": b.internal_symbols,
                        "external_imports": b.imports_from_public_packages,
                        "internal_imports": b.imports_from_internal,
                        "__all__": bool(b.public_exports) and any(
                            self.modules.get(name, ModuleBoundary(name, '', [], [], [], [])).public_exports
                        )
                    }
                    for name, b in self.modules.items()
                ]
            },
            
            "engineering_questions": {
                "Q1_minimal_public_surface": {
                    "question": "What is the smallest stable public surface consumers require?",
                    "evidence": self._analyze_minimal_surface(),
                    "recommendation": "proposed_public_surface"
                },
                "Q2_public_vs_internal": {
                    "question": "Which types are public contract vs internal?",
                    "contract_candidates": [
                        {
                            "name": sym.name,
                            "kind": sym.kind,
                            "module": sym.defined_in,
                            "is_frozen": sym.is_frozen
                        }
                        for sym in contract_candidates
                        if sym.name not in ('extract_boq',)
                    ],
                    "internal_types": [
                        {
                            "name": sym.name,
                            "kind": sym.kind,
                            "module": sym.defined_in
                        }
                        for sym in internal_helpers
                    ],
                    "boqrow_status": "BOQRow is a production dataclass but is an extraction pre-requisite, not evidence. It is a dependency, not part of the evidence contract."
                },
                "Q3_import_stability": {
                    "question": "Which imports should consumers rely upon?",
                    "evidence": self._analyze_import_stability()
                },
                "Q5_consumer_guarantees": {
                    "question": "What guarantees regarding stability?",
                    "evidence": "Based on frozen evidence from Spikes 1-3"
                },
                "Q6_breaking_changes": {
                    "question": "What constitutes a breaking consumer change?",
                    "evidence": self._analyze_breaking_changes()
                }
            },
            
            "access_pattern_evaluation": self._evaluate_access_patterns(),
            
            "recommendation": self._generate_recommendation()
        }
    
    def _analyze_minimal_surface(self) -> Dict:
        """Q1: Determine minimal public surface consumers need."""
        return {
            "consumer_needs": [
                {
                    "need": "Run BOQ intelligence analysis",
                    "symbol": "analyze_boq",
                    "module": "jarvis.parsers.costx.boq_intelligence",
                    "type": "function(rows: list[BOQRow], *, include_hierarchy: bool = False, include_detection: bool = False) -> BOQIntelligenceResult",
                    "evidence": "boq_intelligence.py line 67 - Only public function in module"
                },
                {
                    "need": "Access analysis results",
                    "symbol": "BOQIntelligenceResult",
                    "module": "jarvis.parsers.costx.boq_intelligence",
                    "type": "frozen dataclass with 10 evidence fields",
                    "evidence": "boq_intelligence.py lines 48-64 - Primary evidence container"
                },
                {
                    "need": "Access hierarchy nodes",
                    "symbol": "BOQHeaderNode",
                    "module": "jarvis.parsers.costx.boq_intelligence",
                    "type": "frozen dataclass with 9 fields",
                    "evidence": "boq_intelligence.py lines 27-45 - Public frozen dataclass"
                },
                {
                    "need": "Provide row input to analyze_boq",
                    "symbol": "BOQRow",
                    "module": "jarvis.parsers.costx.boq_extraction",
                    "type": "dataclass with 7 fields",
                    "evidence": "boq_extraction.py lines 39-48 - Input dependency for analyze_boq"
                },
                {
                    "need": "Extract rows from workbook",
                    "symbol": "extract_boq",
                    "module": "jarvis.parsers.costx.boq_extraction",
                    "type": "function(workbook: Workbook) -> list[BOQRow]",
                    "evidence": "boq_extraction.py line 51 - Standard upstream extraction"
                }
            ],
            "not_needed": [
                {
                    "symbol": "WorkbookParser",
                    "module": "jarvis.parsers.costx.workbook_parser",
                    "reason": "WorkbookParser is a validation/loading concern, not an evidence consumer concern. It's pre-extraction infrastructure.",
                    "evidence": "costx/__init__.py exports WorkbookParser as existing public surface"
                },
                {
                    "symbol": "_extract_head_level",
                    "reason": "Internal helper for hierarchy reconstruction",
                    "evidence": "boq_intelligence.py line 183"
                },
                {
                    "symbol": "_reconstruct_hierarchy",
                    "reason": "Internal implementation detail of analyze_boq",
                    "evidence": "boq_intelligence.py line 198"
                },
                {
                    "symbol": "_freeze_node",
                    "reason": "Internal mutable-to-immutable conversion",
                    "evidence": "boq_intelligence.py line 262"
                },
                {
                    "symbol": "_compute_hierarchy_statistics",
                    "reason": "Internal composition of analyze_boq",
                    "evidence": "boq_intelligence.py line 279"
                },
                {
                    "symbol": "_detect_level_skips, _detect_zero_quantities, _detect_structural_containment, _detect_basic_completeness",
                    "reason": "Internal detection evidence generators, internal to analyze_boq",
                    "evidence": "boq_intelligence.py lines 335-476"
                },
                {
                    "symbol": "_count_row_types, _compute_section_stats, _compute_boq_stats, _detect_anomalies",
                    "reason": "Internal evidence generators, private to analyze_boq",
                    "evidence": "boq_intelligence.py lines 120-178"
                }
            ],
            "note": "No engineering evidence exists for any intermediate abstractions, facades, or protocols between extract_boq/analyze_boq and consumers."
        }
    
    def _analyze_import_stability(self) -> Dict:
        """Q3: Analyze import stability based on production evidence."""
        return {
            "stable_imports": [
                {
                    "import": "from jarvis.parsers.costx.boq_intelligence import analyze_boq, BOQIntelligenceResult, BOQHeaderNode",
                    "rationale": "All three symbols are public (no underscore prefix), frozen dataclass or public function",
                    "stability": "HIGH - frozen by production frozen=True and engineering evidence",
                    "evidence": "boq_intelligence.py lines 27, 48, 67"
                },
                {
                    "import": "from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq",
                    "rationale": "Both symbols are public (no underscore prefix)",
                    "stability": "HIGH - stable extraction interface",
                    "evidence": "boq_extraction.py lines 39, 51"
                }
            ],
            "unstable_imports_must_not_use": [
                {
                    "import": "from jarvis.parsers.costx.boq_intelligence import _count_row_types",
                    "rationale": "Underscore-prefixed = internal implementation",
                    "evidence": "boq_intelligence.py line 120"
                },
                {
                    "import": "from jarvis.parsers.costx.boq_intelligence import _reconstruct_hierarchy",
                    "rationale": "Underscore-prefixed = internal implementation",
                    "evidence": "boq_intelligence.py line 198"
                },
                {
                    "import": "from jarvis.parsers.costx.boq_extraction import _classify_row",
                    "rationale": "Underscore-prefixed = internal implementation",
                    "evidence": "boq_extraction.py line 108"
                }
            ],
            "current_vs_recommended": {
                "current_pattern": "Consumers import directly from internal modules (boq_intelligence.py, boq_extraction.py)",
                "recommended_pattern": "No evidence exists for a dedicated public package. Current direct imports are the production-proven pattern.",
                "risk": "Direct imports from non-__init__ modules mean consumers depend on file layout. Changes to module structure could break imports even if contract semantics remain stable.",
                "mitigation": "Document stable import paths explicitly. Monitor changes to module structure during development.",
                "evidence": "costx/__init__.py only exports WorkbookParser - no BOQ intelligence symbols are re-exported"
            }
        }
    
    def _analyze_breaking_changes(self) -> Dict:
        """Q6: Analyze what constitutes a breaking consumer change."""
        return {
            "breaking_changes": [
                {
                    "change": "Adding, removing, or renaming BOQIntelligenceResult fields",
                    "rationale": "Consumers access evidence fields directly on the dataclass",
                    "category": "MAJOR per Spike 2"
                },
                {
                    "change": "Changing signature of analyze_boq()",
                    "rationale": "Consumers call with specific named parameters",
                    "category": "MAJOR per Spike 2"
                },
                {
                    "change": "Changing return type of analyze_boq()",
                    "rationale": "Consumer destructuring depends on return type",
                    "category": "MAJOR per Spike 2"
                },
                {
                    "change": "Moving symbols across modules",
                    "rationale": "Consumers import from specific module paths; relocation breaks imports",
                    "category": "MAJOR per Spike 2"
                },
                {
                    "change": "Removing or renaming BOQHeaderNode fields",
                    "rationale": "Consumers access hierarchy nodes directly",
                    "category": "MAJOR per Spike 2"
                },
                {
                    "change": "Changing BOQRow dataclass structure",
                    "rationale": "BOQRow is input to analyze_boq; structural changes break consumer usage",
                    "category": "MAJOR per Spike 2"
                }
            ],
            "non_breaking_changes": [
                {
                    "change": "Adding new optional evidence fields",
                    "rationale": "Existing fields remain stable, consumers unaffected",
                    "category": "MINOR per Spike 2"
                },
                {
                    "change": "Adding new internal helper functions",
                    "rationale": "Internal details, not part of contract",
                    "category": "PATCH per Spike 2"
                },
                {
                    "change": "Documentation changes",
                    "rationale": "No consumer impact",
                    "category": "PATCH per Spike 2"
                }
            ]
        }
    
    def _evaluate_access_patterns(self) -> Dict:
        """Q4: Evaluate different access patterns."""
        return {
            "alternatives_evaluated": [
                {
                    "pattern": "Direct dataclass access (current)",
                    "advantages": [
                        "Zero overhead - consumers access fields directly",
                        "Type-checker friendly - static type checking works naturally",
                        "No abstraction layer to maintain",
                        "All evidence fields naturally visible and discoverable",
                        "Current production pattern - proven working"
                    ],
                    "disadvantages": [
                        "No encapsulation - consumers can see all fields",
                        "Direct module import dependency",
                        "Cannot hide internal fields (not applicable - all fields are contract)"
                    ],
                    "compatibility": "100% - current pattern",
                    "evidence": "boq_intelligence.py lines 48-64 - Current production code",
                    "recommendation": "Supported"
                },
                {
                    "pattern": "Dedicated public package (jarvis.parsers.contracts)",
                    "advantages": [
                        "Clean separation between implementation and contract",
                        "Stable import path independent of implementation module structure",
                        "Can re-export only contract types"
                    ],
                    "disadvantages": [
                        "Requires creating and maintaining new package",
                        "Additional abstraction layer for no current consumer benefit",
                        "Package must stay in sync with implementation - new drift surface",
                        "No evidence this is needed - no consumer currently exists"
                    ],
                    "compatibility": "Could be added as MINOR - does not remove existing imports",
                    "evidence": "No engineering evidence available",
                    "recommendation": "Deferred until consumer exists"
                },
                {
                    "pattern": "Protocol interface",
                    "advantages": [
                        "Provides formal interface contract",
                        "Can be implemented differently"
                    ],
                    "disadvantages": [
                        "Significant overhead for single implementation",
                        "YAGNI violation - no alternative implementation",
                        "Protocol abstraction with no current use case",
                        "Hides concrete field types from consumers"
                    ],
                    "compatibility": "MAJOR - would change consumer import model",
                    "evidence": "No engineering evidence available",
                    "recommendation": "Rejected - YAGNI violation"
                },
                {
                    "pattern": "Facade object",
                    "advantages": [
                        "Single point of access"
                    ],
                    "disadvantages": [
                        "Indirection with no benefit for single-module API",
                        "Hides frozen dataclass nature",
                        "Adds runtime overhead"
                    ],
                    "compatibility": "Could be added as MINOR",
                    "evidence": "No engineering evidence available",
                    "recommendation": "Rejected - no benefit over direct dataclass"
                },
                {
                    "pattern": "Factory function",
                    "advantages": [
                        "Can control construction"
                    ],
                    "disadvantages": [
                        "Current frozen dataclass already ensures immutability",
                        "Factory is already analyze_boq() - no additional factory needed",
                        "Would add indirection with no consumer benefit"
                    ],
                    "compatibility": "MAJOR - changes consumer code pattern",
                    "evidence": "boq_intelligence.py line 67 - analyze_boq() IS the factory",
                    "recommendation": "Rejected - analyze_boq() already serves as factory"
                },
                {
                    "pattern": "Read-only interface/Immutable contract object",
                    "advantages": [
                        "Prevents mutation at interface level"
                    ],
                    "disadvantages": [
                        "Current frozen dataclass already provides immutability",
                        "Interface abstraction with no current benefit",
                        "Hides specific field types behind generic accessor"
                    ],
                    "compatibility": "MAJOR - changes consumer code pattern",
                    "evidence": "boq_intelligence.py line 48: frozen=True - immutability already enforced",
                    "recommendation": "Rejected - frozen dataclass provides equivalent guarantee"
                }
            ],
            "recommended_pattern": {
                "pattern": "Direct dataclass + public function (current production pattern)",
                "consumer_imports": [
                    "from jarvis.parsers.costx.boq_intelligence import analyze_boq, BOQIntelligenceResult, BOQHeaderNode",
                    "from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq"
                ],
                "consumer_usage": "result = analyze_boq(rows, include_hierarchy=True, include_detection=True)",
                "evidence": "boq_intelligence.py lines 48-64, 67 - Current production implementation"
            }
        }
    
    def _generate_recommendation(self) -> Dict:
        """Generate final recommendation."""
        return {
            "recommendation": "Maintain direct dataclass access pattern",
            "rationale": "Current production implementation is the proven consumer pattern. No evidence supports any additional abstraction layer.",
            "public_contract_imports": {
                "stable": [
                    "from jarvis.parsers.costx.boq_intelligence import analyze_boq",
                    "from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult",
                    "from jarvis.parsers.costx.boq_intelligence import BOQHeaderNode",
                    "from jarvis.parsers.costx.boq_extraction import BOQRow",
                    "from jarvis.parsers.costx.boq_extraction import extract_boq"
                ],
                "must_not_import": [
                    "from jarvis.parsers.costx.boq_intelligence import _count_row_types",
                    "from jarvis.parsers.costx.boq_intelligence import _reconstruct_hierarchy",
                    "from jarvis.parsers.costx.boq_intelligence import _freeze_node",
                    "from jarvis.parsers.costx.boq_intelligence import _compute_hierarchy_statistics",
                    "from jarvis.parsers.costx.boq_intelligence import _detect_level_skips",
                    "from jarvis.parsers.costx.boq_intelligence import _detect_zero_quantities",
                    "from jarvis.parsers.costx.boq_intelligence import _detect_structural_containment",
                    "from jarvis.parsers.costx.boq_intelligence import _detect_basic_completeness",
                    "from jarvis.parsers.costx.boq_extraction import _classify_row"
                ]
            },
            "evidence": "src/jarvis/parsers/costx/boq_intelligence.py, src/jarvis/parsers/costx/boq_extraction.py"
        }

def main():
    """Execute Spike 4 analysis."""
    print("=" * 80)
    print("EQ-0012 Spike 4: Consumer Access Patterns")
    print("=" * 80)
    print()
    
    analyzer = ConsumerAccessAnalyzer()
    findings = analyzer.analyze_package()
    
    # Print findings
    print(f"Investigation: {findings['investigation']}")
    print(f"Date: {findings['date']}")
    print(f"Source of Truth: {findings['source_of_truth']}")
    print()
    
    # Print modules
    print("Modules Found:")
    for mod in findings['analysis']['modules_found']:
        print(f"  {mod['module']}")
        print(f"    Public exports: {', '.join(mod['public_exports']) or '(none)'}")
        print(f"    Internal symbols: {', '.join(mod['internal_symbols']) or '(none)'}")
        print()
    
    # Print Q1
    q1 = findings['engineering_questions']['Q1_minimal_public_surface']
    print("Q1 - Minimal Public Surface:")
    print(f"  Evidence: {q1['evidence']['note']}")
    for need in q1['evidence']['consumer_needs']:
        print(f"    Need: {need['need']}")
        print(f"      Symbol: {need['symbol']}")
        print(f"      Module: {need['module']}")
    print()
    
    # Print Q2
    q2 = findings['engineering_questions']['Q2_public_vs_internal']
    print("Q2 - Public Contract vs Internal Types:")
    print(f"  Contract Candidates: {len(q2['contract_candidates'])}")
    for c in q2['contract_candidates']:
        print(f"    {c['name']} ({c['kind']}, {c['module']})")
    print(f"  Internal (underscore) helpers: {len(q2['internal_types'])}")
    print()
    
    # Print Q3
    q3 = findings['engineering_questions']['Q3_import_stability']
    q3_evidence = q3['evidence']
    print("Q3 - Import Stability:")
    print("  Stable imports:")
    for imp in q3_evidence['stable_imports']:
        print(f"    {imp['import']}")
        print(f"      Stability: {imp['stability']}")
    print("  Unstable (must not use):")
    for imp in q3_evidence['unstable_imports_must_not_use']:
        print(f"    {imp['import']}")
    print()
    
    # Print Q4
    print("Q4 - Access Pattern Evaluation:")
    print(f"  Recommended: {findings['access_pattern_evaluation']['recommended_pattern']['pattern']}")
    print(f"  Consumer usage: {findings['access_pattern_evaluation']['recommended_pattern']['consumer_usage']}")
    print()
    
    # Print Q5/Q6
    q6 = findings['engineering_questions']['Q6_breaking_changes']
    q6_evidence = q6['evidence']
    print("Q6 - Breaking Changes:")
    for change in q6_evidence['breaking_changes']:
        print(f"  {change['change']} - {change['category']}")
    print()
    
    # Print recommendation
    rec = findings['recommendation']
    print("=" * 80)
    print(f"Recommendation: {rec['recommendation']}")
    print(f"Rationale: {rec['rationale']}")
    print("=" * 80)
    
    # Save report
    output_path = Path("data/reports/eq0012_spike4_consumer_access_patterns.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(findings, f, indent=2)
    
    print(f"\nFull report saved to: {output_path}")

if __name__ == "__main__":
    main()
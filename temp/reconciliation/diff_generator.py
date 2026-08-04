import logging
from pathlib import Path
import difflib

REPO_ROOT = Path("d:/Jarvis")
FEDORA_ROOT = REPO_ROOT / "temp" / "reconciliation" / "fedora_snapshot"
OUTPUT_DIR = REPO_ROOT / "temp" / "reconciliation" / "conflict_resolution"

CONFLICT_FILES = [
    ".gitignore",
    "AGENTS.md",
    "docs/engineering/Engineering_Register.md",
    "docs/governance/WORKSTREAM_GOVERNANCE.md",
    "docs/implementation/IP_0001/README.md",
    "docs/knowledge/04_Engineering_Governance.md",
    "knowledge/registry/knowledge_inventory.csv",
    "knowledge/registry/source_manifest.json",
    "src/jarvis/application/__init__.py",
    "tests/__init__.py",
    "tests/validation/test_verify_governance_integration.py"
]

def generate_diffs():
    with open(OUTPUT_DIR / "Conflict_Diff_Summary.md", "w", encoding="utf-8") as out:
        out.write("# Conflict Diff Summary\n\n")

        for relative_path in CONFLICT_FILES:
            win_path = REPO_ROOT / relative_path
            fed_path = FEDORA_ROOT / relative_path

            out.write(f"## File: {relative_path}\n\n")

            win_lines = []
            if win_path.exists():
                with open(win_path, "r", encoding="utf-8", errors="replace") as f:
                    win_lines = f.readlines()

            fed_lines = []
            if fed_path.exists():
                with open(fed_path, "r", encoding="utf-8", errors="replace") as f:
                    fed_lines = f.readlines()

            diff = list(difflib.unified_diff(
                win_lines, fed_lines, 
                fromfile=f"Windows: {relative_path}", 
                tofile=f"Fedora: {relative_path}"
            ))

            if diff:
                out.write("```diff\n")
                out.writelines(diff)
                out.write("```\n\n")
            else:
                out.write("No textual difference or file reading error.\n\n")

if __name__ == "__main__":
    generate_diffs()
    print("Diffs generated.")
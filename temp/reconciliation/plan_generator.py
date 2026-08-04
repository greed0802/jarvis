import os
from pathlib import Path

REPO_ROOT = Path("d:/Jarvis")
REPORTS_DIR = REPO_ROOT / "temp" / "reconciliation" / "reports"

def generate_merge_plan():
    with open(REPORTS_DIR / "Repository_Reconciliation_Inventory.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    fedora_only = []
    diffs = []
    for line in lines:
        if "FEDORA_ONLY" in line:
            parts = line.split("|")
            if len(parts) > 2:
                fedora_only.append(parts[1].strip())
        elif "DIFFERENT" in line:
            parts = line.split("|")
            if len(parts) > 2:
                diffs.append(parts[1].strip())
            
    with open(REPORTS_DIR / "Merge_Plan.md", "w", encoding='utf-8') as f:
        f.write("# Merge Plan\n\n")
        
        f.write("## Phase 1: Fedora Only (Action: KEEP_FEDORA)\n\n")
        f.write("These files exist only in the Fedora snapshot and will be copied over.\n\n")
        for f_only in fedora_only:
            f.write(f"- KEEP_FEDORA: {f_only}\n")
            
        f.write("\n## Phase 2: Conflicts & Protected Artifacts (Action: REQUIRES_HUMAN)\n\n")
        f.write("These files exist in both repositories but differ. As they fall under protected or sensitive paths, they are marked for human resolution per the reconciliation protocol.\n\n")
        for diff in diffs:
            f.write(f"- REQUIRES_HUMAN: {diff}\n")

if __name__ == "__main__":
    generate_merge_plan()
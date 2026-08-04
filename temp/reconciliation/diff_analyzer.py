import os
from pathlib import Path
import json

REPO_ROOT = Path("d:/Jarvis")
REPORTS_DIR = REPO_ROOT / "temp" / "reconciliation" / "reports"

def analyze():
    with open(REPORTS_DIR / "Repository_Reconciliation_Inventory.md", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    fedora_only = []
    for line in lines:
        if "FEDORA_ONLY" in line:
            parts = line.split("|")
            if len(parts) > 2:
                fedora_only.append(parts[1].strip())
                
    print("FEDORA ONLY FILES:")
    for f in fedora_only:
        print(f"- {f}")

if __name__ == "__main__":
    analyze()
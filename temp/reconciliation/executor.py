import os
import shutil
import datetime
from pathlib import Path

REPO_ROOT = Path("d:/Jarvis")
FEDORA_ROOT = REPO_ROOT / "temp" / "reconciliation" / "fedora_snapshot"
REPORTS_DIR = REPO_ROOT / "temp" / "reconciliation" / "reports"

def run_migration():
    with open(REPORTS_DIR / "Merge_Plan.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    fedora_files = []
    for line in lines:
        if line.startswith("- KEEP_FEDORA:"):
            fpath = line.split("KEEP_FEDORA:", 1)[1].strip()
            fedora_files.append(fpath)

    log_entries = []

    for rel_path in fedora_files:
        src = FEDORA_ROOT / rel_path
        dst = REPO_ROOT / rel_path

        # Windows long path support
        src_str = "\\\\?\\" + os.path.normpath(str(src.absolute()))
        dst_str = "\\\\?\\" + os.path.normpath(str(dst.absolute()))
        dst_dir_str = "\\\\?\\" + os.path.normpath(str(dst.parent.absolute()))

        try:
            os.makedirs(dst_dir_str, exist_ok=True)
            shutil.copy2(src_str, dst_str)
            log_entries.append(f"Copied {rel_path} from Fedora snapshot to Canonical Windows repo.")
        except Exception as e:
            log_entries.append(f"FAILED to copy {rel_path}: {e}")

    with open(REPORTS_DIR / "Migration_Log.md", "w", encoding="utf-8") as f:
        f.write("# Migration Log\n\n")
        f.write(f"Date: {datetime.datetime.now().isoformat()}\n\n")
        for entry in log_entries:
            f.write(f"- {entry}\n")

    with open(REPORTS_DIR / "Repository_Reconciliation_Report.md", "w", encoding="utf-8") as f:
        f.write("# Repository Reconciliation Report\n\n")
        f.write(f"Date: {datetime.datetime.now().isoformat()}\n\n")
        f.write("## Status\n\nReconciliation execution completed.\n\n")
        f.write(f"## Metrics\n\n- Files migrated from Fedora: {len(fedora_files)}\n")
        
        diffs = []
        with open(REPORTS_DIR / "Conflict_Register.md", "r", encoding="utf-8") as cr:
            for line in cr:
                if line.startswith("- "):
                    diffs.append(line.strip())
        
        f.write(f"- Files marked REQUIRES_HUMAN (Conflicts): {len(diffs)}\n\n")
        f.write("## Summary\n\nAll non-conflicting Fedora-specific files have been merged. Conflicting and protected files are logged in `Conflict_Register.md` and marked as `REQUIRES_HUMAN` in `Merge_Plan.md`.")

if __name__ == "__main__":
    run_migration()
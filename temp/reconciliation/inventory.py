import os
import filecmp
import hashlib
from pathlib import Path

REPO_ROOT = Path("d:/Jarvis")
FEDORA_ROOT = REPO_ROOT / "temp" / "reconciliation" / "fedora_snapshot"
REPORTS_DIR = REPO_ROOT / "temp" / "reconciliation" / "reports"

IGNORE_DIRS = {".git", ".venv", "temp", "__pycache__", "node_modules", ".pytest_cache", ".idea", ".vscode"}
IGNORE_FILES = {".DS_Store"}

def get_files(root: Path):
    result = set()
    for root_dir, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if f in IGNORE_FILES:
                continue
            if f.endswith('.pyc') or f.endswith('.pyo'):
                continue
            rel = (Path(root_dir) / f).relative_to(root)
            result.add(rel.as_posix())
    return result

def file_hash(path: Path):
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return "ERROR_READING_FILE"

def analyze():
    win_files = get_files(REPO_ROOT)
    fed_files = get_files(FEDORA_ROOT)
    
    all_files = sorted(list(win_files | fed_files))
    
    inventory = []
    diffs = []
    conflicts = []
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    for f in all_files:
        win_path = REPO_ROOT / f
        fed_path = FEDORA_ROOT / f
        
        in_win = win_path.exists()
        in_fed = fed_path.exists()
        
        if in_win and in_fed:
            try:
                is_identical = filecmp.cmp(win_path, fed_path, shallow=False)
            except Exception:
                is_identical = False
                
            if is_identical:
                inventory.append({"file": f, "status": "IDENTICAL", "hash": file_hash(win_path)})
            else:
                inventory.append({"file": f, "status": "DIFFERENT"})
                diffs.append(f)
                conflicts.append(f)
        elif in_win:
            inventory.append({"file": f, "status": "WINDOWS_ONLY"})
        else:
            inventory.append({"file": f, "status": "FEDORA_ONLY"})
            
    with open(REPORTS_DIR / "Repository_Reconciliation_Inventory.md", "w", encoding='utf-8') as f_inv:
        f_inv.write("# Repository Reconciliation Inventory\n\n")
        f_inv.write("| File | Status | SHA-256 (Windows) |\n")
        f_inv.write("|---|---|---|\n")
        for item in inventory:
            h = item.get("hash", "N/A")
            f_inv.write(f"| {item['file']} | {item['status']} | {h} |\n")
            
    with open(REPORTS_DIR / "Repository_Difference_Report.md", "w", encoding='utf-8') as f_diff:
        f_diff.write("# Repository Difference Report\n\n")
        for diff in diffs:
            f_diff.write(f"- {diff}\n")
            
    with open(REPORTS_DIR / "Conflict_Register.md", "w", encoding='utf-8') as f_conf:
        f_conf.write("# Conflict Register\n\n")
        for conf in conflicts:
            f_conf.write(f"- {conf}\n")
            
    print(f"Total files analyzed: {len(all_files)}")
    print(f"Identical: {len([x for x in inventory if x['status'] == 'IDENTICAL'])}")
    print(f"Windows Only: {len([x for x in inventory if x['status'] == 'WINDOWS_ONLY'])}")
    print(f"Fedora Only: {len([x for x in inventory if x['status'] == 'FEDORA_ONLY'])}")
    print(f"Different (Conflicts): {len(conflicts)}")

if __name__ == "__main__":
    analyze()
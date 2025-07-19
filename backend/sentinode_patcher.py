import json
import re
import os
import subprocess
from datetime import datetime

# ===== CONFIGURATION =====
INPUT_FILE = "../code_sample.js"      # File to scan
OUTPUT_FILE = "../code_sample.js"     # Will modify original file (with backup)
BACKUP_FILE = "../code_sample.bak"    # Backup location

# ===== SECURITY FIX PATTERNS =====
SECURITY_PATTERNS = {
    "Hardcoded API Key": (
        r'(\w+)\s*=\s*["\'](AKIA|AIza|ghp_|sk_)[a-zA-Z0-9_\-]+["\']',
        r'\1 = process.env.\1',
        "Replaced with environment variable"
    ),
    "Hardcoded Password": (
        r'(password|passwd|pwd|secret)\s*=\s*["\'][^"\']+["\']',
        r'\1 = process.env.\1_CREDENTIAL',
        "Replaced with env variable"
    )
}

def create_backup():
    """Create backup of original file"""
    if os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "r") as src, open(BACKUP_FILE, "w") as dst:
            dst.write(src.read())

def suggest_patch(issue, code):
    """Apply security fixes"""
    if issue['type'] not in SECURITY_PATTERNS:
        return code
    
    pattern, replacement, _ = SECURITY_PATTERNS[issue['type']]
    lines = code.split('\n')
    
    if 'line' in issue and 0 <= issue['line']-1 < len(lines):
        line_content = lines[issue['line']-1]
        if re.search(pattern, line_content):
            lines[issue['line']-1] = re.sub(pattern, replacement, line_content)
            return '\n'.join(lines)
    return code

def main():
    print(f"🔍 SENTINODE Patcher - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"⚠️ Modifying: {os.path.basename(INPUT_FILE)} (backup at {os.path.basename(BACKUP_FILE)})")
    
    # Validate files
    if not os.path.exists(INPUT_FILE):
        print(f"🚨 Missing: {INPUT_FILE}")
        return
    
    if not os.path.exists("../report.json"):
        print("🚨 Missing: ../report.json")
        return
    
    try:
        # Create backup
        create_backup()
        
        # Load files
        with open("../report.json") as f:
            report = json.load(f)
        
        with open(INPUT_FILE) as f:
            code = f.read()
        
        # Apply fixes
        changes_made = False
        for issue in report.get("issues", []):
            print(f"\n🛠️ Fixing: {issue['type']} (Line {issue.get('line', 'N/A')})")
            
            before = code.split('\n')[issue.get('line', 1)-1] if 'line' in issue else code
            patched = suggest_patch(issue, code)
            
            if patched != code:
                changes_made = True
                code = patched
                after = code.split('\n')[issue.get('line', 1)-1] if 'line' in issue else code
                print("🔴 Before: " + before.strip())
                print("🟢 After:  " + after.strip())
            else:
                print("ℹ️ No changes needed (already patched or pattern not found)")
        
        # Save changes
        if changes_made:
            with open(OUTPUT_FILE, "w") as f:
                f.write(code)
            print("\n✅ Successfully patched file")
        else:
            print("\nℹ️ No vulnerabilities needed patching")
            
    except Exception as e:
        print(f"🚨 Error: {str(e)}")
        print("⚠️ Restoring from backup...")
        if os.path.exists(BACKUP_FILE):
            with open(BACKUP_FILE, "r") as src, open(INPUT_FILE, "w") as dst:
                dst.write(src.read())

if __name__ == "__main__":
    main()
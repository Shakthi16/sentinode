import json
import re
import os

# ===== CONFIG =====
REPORT_PATH = "report.json"         # ✅ Fixed path
SOURCE_FILE = "code_sample_to_test.js"
ENV_TEMPLATE_FILE = ".env.template"  # ✅ Output file at project root

# ===== Patterns to match for extracting variable names =====
ENV_VAR_PATTERNS = {
    "Hardcoded API Key": r'(\w+)\s*=\s*["\'](AKIA|AIza|ghp_|sk_)[a-zA-Z0-9_\-]+["\']',
    "Hardcoded Password": r'(password|passwd|pwd|secret)\s*=\s*["\'][^"\']+["\']',
}

def extract_variable_names(code, issues):
    env_vars = set()

    lines = code.split('\n')
    for issue in issues:
        issue_type = issue.get("type")
        pattern = ENV_VAR_PATTERNS.get(issue_type)

        if not pattern:
            continue

        line_number = issue.get("line", 1) - 1
        if 0 <= line_number < len(lines):
            line = lines[line_number]
            match = re.search(pattern, line)
            if match:
                var = match.group(1)
                if issue_type == "Hardcoded Password":
                    var = f"{var}_CREDENTIAL"
                env_vars.add(var)

    return env_vars

def generate_env_template(env_vars):
    with open(ENV_TEMPLATE_FILE, "w") as f:
        for var in sorted(env_vars):
            f.write(f"{var}=\n")
    print(f"✅ .env.template generated with {len(env_vars)} variables")

def main():
    if not os.path.exists(REPORT_PATH) or not os.path.exists(SOURCE_FILE):
        print("🚨 report.json or code_sample.js not found")
        return

    with open(REPORT_PATH) as f:
        report = json.load(f)

    with open(SOURCE_FILE) as f:
        code = f.read()

    issues = report.get("issues", [])
    env_vars = extract_variable_names(code, issues)

    if env_vars:
        generate_env_template(env_vars)
    else:
        print("ℹ️ No environment variables detected to generate")

if __name__ == "__main__":
    main()

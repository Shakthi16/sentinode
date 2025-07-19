# scan.py
import json
import re

# Sample test input (will be replaced when running via backend)
code_sample = """
const API_KEY = "AKIA1234567890XYZ";
const password = "123456";
"""

# Patterns to detect
patterns = [
    {
        "pattern": r"AKIA[0-9A-Z]{16}",
        "type": "Hardcoded API Key",
        "severity": "High",
        "suggestion": "Use env variable"
    },
    {
        "pattern": r"(password\s*=\s*[\"'].*[\"'])",
        "type": "Hardcoded Password",
        "severity": "High",
        "suggestion": "Use vault secret manager"
    }
]

def scan(code):
    issues = []
    lines = code.split("\n")
    for i, line in enumerate(lines, start=1):
        for rule in patterns:
            if re.search(rule["pattern"], line):
                issues.append({
                    "line": i,
                    "type": rule["type"],
                    "severity": rule["severity"],
                    "suggestion": rule["suggestion"]
                })
    return issues

# Run scan
results = scan(code_sample)

# Save report
with open("report.json", "w") as f:
    json.dump({"issues": results}, f, indent=4)

print("✅ Report saved as report.json")

import json

sample_code = '''
const API_KEY = "AKIAEXAMPLE123456789";
const password = "1234";
'''

issues = []

lines = sample_code.strip().split('\n')
for i, line in enumerate(lines, 1):
    if "AKIA" in line:
        issues.append({
            "line": i,
            "type": "Hardcoded API Key",
            "severity": "High",
            "suggestion": "Use env variable"
        })
    if "password" in line:
        issues.append({
            "line": i,
            "type": "Hardcoded Password",
            "severity": "High",
            "suggestion": "Use vault secret manager"
        })

with open("report.json", "w") as f:
    json.dump({"issues": issues}, f, indent=2)

print("AI Scan complete. Report saved to report.json")

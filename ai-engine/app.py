from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze_code():
    data = request.json
    code = data.get("code", "")
    issues = []

    # Rule 1: Hardcoded AWS keys or common token patterns
    if re.search(r'["\']?(AKIA|AIza|ghp_|sk_|eyJ)[\w\d]{10,}["\']?', code):
        issues.append({
            "line": 1,
            "type": "Hardcoded API Key",
            "severity": "High",
            "suggestion": "Use environment variables instead of hardcoding"
        })

    # Rule 2: Plaintext password
    if re.search(r'(password|passwd|pwd)\s*=\s*["\'].*["\']', code, re.IGNORECASE):
        issues.append({
            "line": 2,
            "type": "Hardcoded Password",
            "severity": "High",
            "suggestion": "Never store passwords in plain text"
        })

    return jsonify({"issues": issues})

if __name__ == "__main__":
    app.run(port=5000, debug=True)

import { useState } from "react";
import axios from "axios";
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-javascript";
import "ace-builds/src-noconflict/theme-github";
import { FaBug } from "react-icons/fa";

function App() {
  const [code, setCode] = useState("// Paste your code here...");
  const [issues, setIssues] = useState([]);

  const handleScan = async () => {
    try {
      const res = await axios.post("http://localhost:4000/scan", { code });
      setIssues(res.data.issues);
    } catch (err) {
      alert("Failed to connect to backend.");
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-6">
      <h1 className="text-3xl font-bold mb-4 flex items-center gap-2 text-blue-700">
        <FaBug /> SENTINODE DevSec Dashboard
      </h1>

      <AceEditor
        mode="javascript"
        theme="github"
        name="code-editor"
        onChange={(val) => setCode(val)}
        value={code}
        fontSize={16}
        width="100%"
        height="300px"
        className="border rounded"
      />

      <button
        onClick={handleScan}
        className="mt-4 bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
      >
        🔍 Scan Code
      </button>

      <div className="mt-6">
        <h2 className="text-xl font-semibold">🛡️ Vulnerability Report</h2>
        {issues.length === 0 ? (
          <p className="text-green-600 mt-2">✅ No issues found</p>
        ) : (
          <ul className="mt-2 space-y-2">
            {issues.map((issue, idx) => (
              <li
                key={idx}
                className="bg-white p-4 rounded shadow border-l-4 border-red-500"
              >
                <p><strong>Type:</strong> {issue.type}</p>
                <p><strong>Severity:</strong> {issue.severity}</p>
                <p><strong>Line:</strong> {issue.line}</p>
                <p><strong>Suggestion:</strong> {issue.suggestion}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;

// 🚨 Insecure Example for Testing Patch Suggestion

const API_KEY = "AKIA1234567890XYZ";        // Hardcoded API Key
const password = "supersecret123";          // Hardcoded password
const dbURL = "mongodb://admin:admin@localhost:27017"; // Credentials in DB URL

function login(user, pass) {
    if (user && pass) {
        console.log("User authenticated");
        return true;
    }
    return false;
}

function fetchData(query) {
    const sql = "SELECT * FROM users WHERE name = '" + query + "'"; // SQL Injection risk
    console.log("Running query:", sql);
}

const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();
const PORT = 4000;

app.use(cors());
app.use(bodyParser.json());

// Route to send code snippet to Python AI engine and return results
app.post("/scan", async (req, res) => {
  const { code } = req.body;

  try {
    // Forward code to Python Flask service at http://localhost:5000/analyze
    const response = await axios.post("http://localhost:5000/analyze", { code });
    
    // Return the issues received from Python service
    res.json(response.data);
  } catch (error) {
    console.error("AI Engine Error:", error.message);
    res.status(500).json({ error: "AI Engine not available. Make sure it's running." });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Backend running at http://localhost:${PORT}`);
});

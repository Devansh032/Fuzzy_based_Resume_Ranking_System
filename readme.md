# 🧠 Resume Ranking System using Fuzzy Logic

A web-based resume ranking system that uses fuzzy logic to evaluate and rank candidate resumes based on job descriptions.
The system utilizes a Python backend for processing logic, Node.js to handle execution using the `spawn` function, and a modern TypeScript + React frontend for interaction.

---

## 📌 Features

- 🔍 Intelligent ranking using **fuzzy logic**
- 📁 Resume and Job Description upload support
- 🚀 Cross-language integration: Node.js (backend) + Python (ranking logic)
- ⚛️ Frontend developed with **TypeScript** and **React**
- 📤 Real-time results displayed on the frontend
- 🧪 Easily extendable with more evaluation criteria

---

## 🛠 Tech Stack

### 🧩 Backend

- **Node.js**
  - Used `child_process.spawn()` to interface with Python
  - Handles resume/job description file uploads
  - Sends files to Python for processing and returns rankings

### 🐍 Python

- Used for implementing fuzzy logic ranking
- Libraries:
  - `fuzzywuzzy` – String similarity
  - `skfuzzy` – Fuzzy logic control
  - `pandas`, `numpy` – Data manipulation
- Reads resumes and job description
- Applies fuzzy rules to rank resumes

### 💻 Frontend

- **React + TypeScript**
  - Clean UI to upload resumes and job description
  - Fetches and displays ranked list
  - Uses `axios` for API calls

---

## ⚙️ How it Works

1. User uploads resumes and a job description from the React frontend.
2. Backend receives the data and uses `spawn` to execute the Python script:
   ```js
   const { spawn } = require('child_process');
   const py = spawn('python', ['ranker.py', 'data/input.json']);

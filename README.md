# 📞 PostCallTranscriptionAnalyser

Analyze customer service call transcripts with AI!  
Get actionable feedback, agent scoring, and complaint type detection — all powered by LLMs via Ollama.

---

## 🚀 Features

- 🤖 **Agent Scoring:** Rates empathy, problem-solving, and professionalism.
- 📝 **Complaint Type Detection:** Identifies the main issue from a call.
- 🗣️ **Speaker Feedback:** Generates feedback for each unique speaker.

---

## 🛠️ API Endpoints

### ✅ Health Check

`GET /health`  
Returns API health status.

---

### 🏅 Score Transcript and Extract Complaint 

`POST /score`

**Request:**
```json
{
  "transcript_id": "1"
}
```
**Response:**  
Score, feedback, and complaint type in JSON.

---

### 📋 Generate Call Report

`POST /GenerateReport`

**Request:**
```json
{
  "transcript_id": "1"
}
```
**Response:**  
Speaker-wise feedback in JSON.

---

## ⚡ Quickstart

1. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

2. **Start Ollama** (ensure `llama3` model is available)

3. **Run the app**
   ```sh
   python app.py
   ```

   Or with Docker:
   ```sh
   docker build -t postcall-analyser .
   docker run -p 5000:5000 postcall-analyser
   ```

---

## 📂 Project Structure

- `app.py` — Flask API server
- `TranscriptAnalyzer.py` — Transcript analysis logic
- `requirements.txt` — Python dependencies
- `Dockerfile` — Containerization

---

## 💡 Example Usage

```sh
curl -X POST http://localhost:5000/score -H "Content-Type: application/json" -d '{"transcript_id": "1"}'
```

---

## 🧑‍💻 Requirements

- Python 3.11+
- Flask
- Ollama Python client
- Ollama server with `llama3` model

---

> Made with ❤️ for call center QA prototyping.
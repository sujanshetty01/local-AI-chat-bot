# 🤖 Local AI Chatbot with CSV/JSON Upload

A fully local AI chatbot system built using **Streamlit**, **FastAPI**, **Ollama (Gemma3/Mistral)**, and **SQLite/PostgreSQL**, allowing users to upload structured data (CSV/JSON), embed it locally, and ask natural language questions to get contextual answers.

---

## 🚀 Features

* Upload and parse CSV/JSON datasets.
* Embed data locally using `nomic-embed-text`.
* Ask natural language questions about the dataset.
* Uses **Ollama** for running open-source LLMs (e.g., Gemma3) locally.
* Streamlit frontend for easy user interaction.
* FastAPI backend for processing and embedding.
* Lightweight and containerized with Docker.

---

## 📁 Folder Structure

```
local-AI-chat-bot/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── database.py          # SQLite or PostgreSQL logic
│   └── embed_utils.py       # Embedding & retrieval logic
├── frontend/
│   └── app.py               # Streamlit UI
├── data/                    # Uploaded CSV/JSON files
├── models/                  # Ollama model configuration
├── Dockerfile               # For containerizing the app
├── docker-compose.yml       # Run frontend & backend together
├── .env                     # Config (DB paths, API keys)
└── requirements.txt         # Python dependencies
```

---

## 🛠️ Requirements

* Python 3.10+
* Ollama (running locally)
* Docker & Docker Compose (optional but recommended)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧠 Ollama Setup

Install and start Ollama:

```bash
ollama run gemma3
```

Or pull another model:

```bash
ollama pull mistral
```

> Ensure Ollama is running on `http://localhost:11434`

---

## 🚦 How to Run

### 🔹 Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 🔹 Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```

> Update `.env` files or hardcoded paths to match your environment.

---

## 🐳 Run with Docker (Optional)

Build and run using Docker Compose:

```bash
docker compose up --build
```

---

## 💡 Example Use Case

1. Upload a `flights.csv` or `cars.json`.
2. Ask questions like:

   * "What is the average price of the cars?"
   * "Which airline has the longest average flight time?"
3. The model gives intelligent, local responses without internet.

---

## ✅ To-Do

* [x] CSV/JSON support
* [x] Local vector embeddings
* [x] Ollama LLM integration
* [ ] File delete and refresh support
* [ ] Export chat history
* [ ] Authentication (admin vs guest)

---

## 🧑‍💻 Author

**Sujan S Shetty**
GitHub: [@sujanshetty01](https://github.com/sujanshetty01)

---

## 📜 License

This project is licensed under the MIT License.

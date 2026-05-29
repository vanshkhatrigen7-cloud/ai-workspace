# 🤖 AI Workspace Assistant

> A full-stack AI-powered PDF Chat application built from scratch using FastAPI, Groq LLM, and RAG (Retrieval-Augmented Generation). Ask questions about your documents and get intelligent, context-aware answers in seconds.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70b-F55036?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-6C63FF?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

---

## 📸 Screenshots

### 💬 PDF Chat UI
![PDF Chat UI](screenshots/chat_ui.png)

### ⚡ API Response via Swagger
![API Swagger](screenshots/swagger_response.png)

---

## 🚀 What This Project Does

Upload any PDF and have a real conversation with it. The app extracts text, breaks it into smart chunks, converts them into vector embeddings, stores them in ChromaDB, and retrieves the most relevant context before answering — all powered by **LLaMA 3.3 70b via Groq**.

No hallucinations. No guessing. Answers come strictly from your document.

---

## ✨ Features

- 📄 **PDF Upload & Processing** — upload any PDF and instantly make it queryable
- 🧠 **RAG Pipeline** — Retrieval-Augmented Generation for accurate, document-grounded answers
- ⚡ **Groq LLM** — ultra-fast inference using LLaMA 3.3 70b (one of the fastest LLMs available)
- 🔍 **Semantic Search** — finds the most relevant chunks using vector similarity, not just keyword matching
- 💬 **Chat History** — maintains conversation context across follow-up questions
- 📦 **Multi-PDF Support** — upload multiple PDFs and query across all of them simultaneously
- 🌐 **REST API** — clean FastAPI backend with auto-generated Swagger docs at `/docs`
- 🖥️ **Clean Dark UI** — modern frontend built with vanilla HTML/CSS/JS, no frameworks needed

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     INGESTION PIPELINE                   │
│                   (runs once per PDF)                    │
│                                                          │
│  PDF File → Extract Text → Chunk (500 chars, 50 overlap) │
│          → Embed (MiniLM-L6-v2) → Store in ChromaDB      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                      QUERY PIPELINE                      │
│                  (runs on every question)                │
│                                                          │
│  User Question → Embed → Similarity Search in ChromaDB  │
│               → Top 3 Chunks → Build Prompt → Groq LLM  │
│               → Answer returned to user                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI |
| LLM Provider | Groq (LLaMA 3.3 70b Versatile) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| PDF Parsing | PyMuPDF (fitz) |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Environment | python-dotenv |

---

## 📁 Project Structure

```
ai-workspace/
├── backend/
│   ├── main.py              ← FastAPI app, all API routes
│   ├── .env                 ← API keys (not pushed to GitHub)
│   ├── requirements.txt
│   ├── uploads/             ← temporary PDF storage
│   └── rag/
│       ├── __init__.py
│       ├── ingest.py        ← PDF → chunks → embeddings → ChromaDB
│       └── query.py         ← question → search → Groq → answer
└── frontend/
    └── index.html           ← complete chat UI
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/vanshkhatrigen7-cloud/ai-workspace.git
cd ai-workspace/backend
```

### 2. Install dependencies
```bash
py -m pip install -r requirements.txt
```

### 3. Create your `.env` file
Inside the `backend/` folder, create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at [console.groq.com](https://console.groq.com)

### 4. Run the backend server
```bash
py -m uvicorn main:app --reload
```

### 5. Open the frontend
Open `frontend/index.html` directly in your browser.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/chat` | General AI chat (Phase 1) |
| POST | `/upload-pdf` | Upload and ingest a PDF |
| POST | `/ask-pdf` | Ask a question about a specific PDF |
| POST | `/ask-all-pdfs` | Ask a question across all uploaded PDFs |

Full interactive API docs available at:
```
http://localhost:8000/docs
```

---

## 💡 How RAG Works (Simple Explanation)

Traditional LLMs can't read your private documents. RAG solves this in two steps:

**Step 1 — Ingestion:** Your PDF is split into small overlapping chunks. Each chunk is converted into a vector (a list of numbers that represents its meaning) using a sentence transformer model. These vectors are stored in ChromaDB.

**Step 2 — Query:** When you ask a question, it is also converted into a vector. ChromaDB finds the chunks whose vectors are most similar (semantically closest) to your question. Those chunks are sent to Groq as context, and the LLM answers based only on that context.

This means answers are always grounded in your actual document — not hallucinated.

---

## 🗺️ Roadmap

- [x] Phase 1 — FastAPI backend + Groq LLM chat
- [x] Phase 2 — PDF ingestion + RAG pipeline
- [x] Phase 3 — Full chat UI + chat history + multi-PDF support
- [ ] Phase 4 — Deploy to cloud (Railway / Render)
- [ ] Phase 5 — Show answer sources with page numbers
- [ ] Phase 6 — Export chat as PDF/text

---

## 👨‍💻 Author

**Vansh**
- GitHub: [@vanshkhatrigen7-cloud](https://github.com/vanshkhatrigen7-cloud)
- LinkedIn: [vansh-genai](https://www.linkedin.com/in/vansh-genai)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built with 💜 as a personal AI project — learning by building.
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os
from typing import List
from fastapi import UploadFile, File
import shutil, uuid
from rag.ingest import ingest_pdf
from rag.query import query_pdf

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

client = Groq(api_key=api_key)

app = FastAPI(title="AI Workspace Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[Message]

@app.get("/")
def home():
    return {"message": "AI Workspace Assistant is running!", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Build messages list for Groq
        # Groq uses "assistant" role (not "model" like Gemini)
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI Workspace Assistant. Help users with their questions clearly and concisely. Be friendly but professional. If you don't know something, say so honestly."
            }
        ]

        # Add conversation history
        for msg in request.history:
            role = "assistant" if msg.role == "model" else msg.role
            messages.append({"role": role, "content": msg.content})

        # Add the new user message
        messages.append({"role": "user", "content": request.message})

        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
        )

        reply = response.choices[0].message.content

        return {"reply": reply, "status": "success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")
    collection_id = str(uuid.uuid4())[:8]
    save_path = f"{UPLOAD_DIR}/{collection_id}.pdf"
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    num_chunks = ingest_pdf(save_path, collection_name=collection_id)
    return {"collection_id": collection_id, "chunks_created": num_chunks}

class QuestionRequest(BaseModel):
    collection_id: str
    question: str

@app.post("/ask-pdf")
async def ask_pdf(req: QuestionRequest):
    try:
        answer = query_pdf(req.question, collection_name=req.collection_id)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
import os
from groq import Groq
from dotenv import load_dotenv
from rag.ingest import embedder, chroma_client

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def query_pdf(question: str, collection_name: str, history: list = []) -> str:
    # Embed and search
    question_embedding = embedder.encode(question).tolist()
    collection = chroma_client.get_collection(collection_name)
    results = collection.query(query_embeddings=[question_embedding], n_results=3)
    context = "\n\n---\n\n".join(results["documents"][0])

    # Build messages with history
    messages = [
        {
            "role": "system",
            "content": f"""You are a helpful assistant that answers questions based ONLY on the document context below.
If the answer isn't in the context, say "I couldn't find that in the document."

CONTEXT:
{context}"""
        }
    ]

    # Add previous conversation turns
    for turn in history[:-1]:  # exclude the current question
        messages.append({"role": turn["role"], "content": turn["content"]})

    # Add current question
    messages.append({"role": "user", "content": question})

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return response.choices[0].message.content
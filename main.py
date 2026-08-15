from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from google import genai

app = FastAPI(title="RAG Document Q&A API")

# Initialize ChromaDB persistent client and collection
db_client = chromadb.PersistentClient(path="./chroma_db")
collection = db_client.get_or_create_collection(name="rag_docs")

# Initialize the Gemini client (reads GEMINI_API_KEY from environment variables)
gemini_client = genai.Client()

# Define the expected request schema using Pydantic
class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    query_text = request.question
    
    # 1. Retrieve the top 2 relevant chunks from ChromaDB
    results = collection.query(
        query_texts=[query_text],
        n_results=2
    )
    
    retrieved_chunks = results["documents"][0] if results["documents"] else []
    context_text = "\n\n".join(retrieved_chunks)
    
    # 2. Build the strict RAG prompt
    prompt = f"""You are a precise document Q&A assistant. 
Answer the user's question using ONLY the provided context below. 
Do not make assumptions or use outside knowledge. If the answer cannot be found in the context, say "I cannot find the answer in the provided documents."

Context:
{context_text}

Question: {query_text}
"""

    # 3. Call the Gemini API
    response = gemini_client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    
    # 4. Return structured JSON response
    return {
        "query": query_text,
        "answer": response.text
    }
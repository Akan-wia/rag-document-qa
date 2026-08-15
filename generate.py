import os
import chromadb
from google import genai

# 1. Connect to ChromaDB and get your collection
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="rag_docs")

# 2. Initialize the Gemini client 
# (Make sure you have set your GEMINI_API_KEY environment variable)
gemini_client = genai.Client()

# 3. Define the user's question
query_text = "What are the remote work rules?"

# 4. Retrieve the top 2 most relevant chunks from ChromaDB
results = collection.query(
    query_texts=[query_text],
    n_results=2
)

# Combine the retrieved chunks into a single context string
retrieved_chunks = results["documents"][0]
context_text = "\n\n".join(retrieved_chunks)

# 5. Build the strict RAG prompt
prompt = f"""You are a precise document Q&A assistant. 
Answer the user's question using ONLY the provided context below. 
Do not make assumptions or use outside knowledge. If the answer cannot be found in the context, say "I cannot find the answer in the provided documents."

Context:
{context_text}

Question: {query_text}
"""

# 6. Call the Gemini API with an active model version
response = gemini_client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

# 7. Print the final synthesized answer
print("🔍 User Query:", query_text)
print("\n🤖 Generated Answer:\n")
print(response.text)
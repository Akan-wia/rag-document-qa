import chromadb

# 1. Connect to the existing persistent ChromaDB database
client = chromadb.PersistentClient(path="./chroma_db")

# 2. Get the "rag_docs" collection we created during ingestion
collection = client.get_or_create_collection(name="rag_docs")

# 3. Define a natural language question to search for
query_text = "What are the remote work rules?"

# 4. Query the collection for the top 2 most semantically similar chunks
results = collection.query(
    query_texts=[query_text],
    n_results=2
)

# 5. Display the retrieved results clearly
print(f"🔍 Query: '{query_text}'\n")
for i, doc in enumerate(results["documents"][0]):
    distance = results["distances"][0][i]
    print(f"Result {i+1} (Distance score: {distance:.4f}):")
    print(f"{doc}\n")
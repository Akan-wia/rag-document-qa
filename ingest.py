# import chromadb
# from langchain_text_splitters import CharacterTextSplitter

# # 1. Open and read the file
# with open("sample.txt", "r", encoding="utf-8") as file:
#     content = file.read()

# print("--- Original File Preview ---")
# print(content[:150] + "...\n")

# # 2. Split the text into chunks
# splitter = CharacterTextSplitter(
#     chunk_size=100,
#     chunk_overlap=20,
#     separator=" "
# )

# chunks = splitter.split_text(content.replace("\n", " "))
# print(f"📄 Total Number of Chunks: {len(chunks)}")

# # 3. Initialize a persistent ChromaDB client (saves data locally in a folder named 'chroma_db')
# client = chromadb.PersistentClient(path="./chroma_db")

# # 4. Create or get a collection named "rag_docs"
# collection = client.get_or_create_collection(name="rag_docs")

# # 5. Generate unique string IDs for each chunk
# ids = [f"chunk_{i}" for i in range(len(chunks))]

# # 6. Add chunks to ChromaDB (ChromaDB automatically embeds them behind the scenes)
# collection.add(
#     documents=chunks,
#     ids=ids
# )

# print("✅ Chunks successfully embedded and stored in ChromaDB!")
# print(f"📊 Total items currently stored in collection: {collection.count()}")

import os
import shutil
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Open and read the file
with open("sample.txt", "r", encoding="utf-8") as file:
    content = file.read()

# 2. Use RecursiveCharacterTextSplitter for intelligent splitting
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)

chunks = splitter.split_text(content)
print(f"📄 Total Number of Chunks: {len(chunks)}")

# Clear old chroma_db folder if it exists to avoid duplicate accumulation during testing
if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")

# 3. Initialize a persistent ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

# 4. Create collection
collection = client.get_or_create_collection(name="rag_docs")

# 5. Generate unique IDs and add to database
ids = [f"chunk_{i}" for i in range(len(chunks))]
collection.add(
    documents=chunks,
    ids=ids
)

print("✅ Clean chunks successfully embedded and stored in ChromaDB!")
# RAG-Based Document Q&A API: The Big Picture Workflow

## 1. You Feed It Documents (Ingestion)
* You upload text files or PDFs into your system.
* Because an AI can't read a whole book all at once, a script breaks your documents down into smaller paragraphs or "chunks."
* An AI model converts each chunk into numbers (embeddings) and stores them in a special database called **ChromaDB**, which is optimized to search through meaning rather than just keywords.

## 2. You Ask a Question (Retrieval)
* Through a React web page, you type a question like: *"What is our company's remote work policy?"*
* Your backend takes your question, turns it into an embedding, and asks ChromaDB: *"Which document chunks are closest in meaning to this question?"*
* ChromaDB instantly hands back the 3 or 4 paragraphs that actually contain the answer.

## 3. The AI Generates the Answer (Generation / RAG)
* Your backend takes those retrieved paragraphs and hands them to the OpenAI API along with a strict instruction: *"Answer the user's question using only the text provided below. Do not make anything up."*
* OpenAI reads those specific snippets and writes a clean, conversational answer.

## 4. You See It on the Screen (Frontend & Deployment)
* The answer streams back line-by-line onto a modern **React chat interface**.
* The whole application is wrapped in **Docker** containers so it can run smoothly on any computer without dependency headaches.
Step 4 explanation:
The Engineering Concept: From CLI Scripts to a Backend API Wrapper
Right now, your RAG logic is isolated inside command-line scripts (generate.py, ingest.py). While this is perfect for core development and debugging, a web browser (like your future React frontend) cannot execute a local Python script directly.

To bridge this gap, you need a Backend API Wrapper (commonly built using a modern framework like FastAPI).

The Role of the API: The backend acts as a translator and gatekeeper. It listens for HTTP requests (like a POST request containing a user's question) sent over the network, validates the input format using data validation schemas, runs your RAG query logic behind the scenes, and returns the synthesized answer back as clean JSON.

Asynchronous Routing: Modern API frameworks are built on asynchronous event loops, allowing them to handle multiple user queries concurrently without blocking the server while waiting for cloud LLM responses.

## Commands

```
python -m venv venv
venv\Scripts\activate
pip install chromadb openai langchain-text-splitters

```
```
python ingest.py

```
```
python query.py

```

<h4> Note: Because we used a simple CharacterTextSplitter with a chunk_size of only 100 characters, it aggressively sliced your text right in the middle of sentences. In real-world RAG applications, tiny chunk sizes break semantic flow. Best practices recommend chunk sizes between 500 to 1,000 characters using a RecursiveCharacterTextSplitter, which intelligently breaks text at natural boundaries like paragraphs and sentences rather than arbitrary character counts. </h4>

Note: query.py is a standalone test and debugging script.

import os
import requests
import streamlit as st

# Read backend URL from environment or fallback to your production/local endpoint
BACKEND_URL = os.getenv(
    "BACKEND_URL", "https://rag-document-qa-swml.onrender.com/ask"
)

st.set_page_config(page_title="RAG Document Q&A", page_icon="🤖")

st.title("🤖 RAG Document Q&A Assistant")
st.write(
    "Ask questions about your uploaded documents powered by your FastAPI backend."
)

# Input box for the user query
query = st.text_input(
    "Enter your question:", placeholder="What are the remote work rules?"
)

if st.button("Ask Assistant"):
    if query:
        with st.spinner("Querying vector database and generating answer..."):
            try:
                # Send POST request to your FastAPI backend
                response = requests.post(BACKEND_URL, json={"question": query})

                if response.status_code == 200:
                    data = response.json()
                    st.success("Answer:")
                    st.write(data["answer"])
                else:
                    st.error(
                        f"Server Error ({response.status_code}): {response.text}"
                    )
            except requests.exceptions.ConnectionError:
                st.error(
                    f"Could not connect to backend at {BACKEND_URL}. Make sure your server is running."
                )
    else:
        st.warning("Please enter a question first.")
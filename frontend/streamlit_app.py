import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # Or your deployed backend

st.set_page_config(page_title="AI Medical Chatbot 🤖💊")

st.title("🧠 AI Medical Report Assistant")

# File Upload
uploaded_file = st.file_uploader("📄 Upload your medical PDF report", type=["pdf"])
if uploaded_file and st.button("📥 Upload and Process"):
    with st.spinner("Uploading and processing..."):
        files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(f"{BACKEND_URL}/upload/", files=files)
        if response.status_code == 200:
            st.success("✅ File processed successfully.")
        else:
            st.error("❌ Upload failed. Try again.")

# Query Input
query = st.text_input("🔍 Ask a question based on the report")

if query and st.button("💬 Get Answer"):
    with st.spinner("Thinking..."):
        res = requests.get(f"{BACKEND_URL}/query/", params={"query": query})
        if res.status_code == 200:
            st.markdown("### 🧠 Response:")
            st.write(res.json()["response"])
        else:
            st.error("⚠ Query failed. Please upload a PDF first.")
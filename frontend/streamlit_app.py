import streamlit as st
import requests

# Set backend API base URL
API_BASE = "https://medisage-51pi.onrender.com"

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Page Config
st.set_page_config(page_title="MediSage AI", page_icon="🩺", layout="centered")

st.title("🩺 MediSage AI Medical Assistant")
st.markdown("Upload your *PDF medical report* and ask any health-related question.")

# File upload section
with st.expander("📄 Upload Medical Report", expanded=True):
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file:
        with st.spinner("Uploading and processing the PDF..."):
            res = requests.post(f"{API_BASE}/upload", files={"file": uploaded_file})
        if res.ok:
            st.success("✅ File uploaded and processed successfully.")
            st.session_state.chat_history = []  # Reset history on new file
        else:
            st.error("❌ Failed to upload. Try again.")

# Ask questions section
st.markdown("### 💬 Ask Your Medical Question")
user_input = st.text_input("Type your question here:")

if user_input:
    with st.spinner("Consulting the AI doctor..."):
        res = requests.get(f"{API_BASE}/query", params={"query": user_input})

    if res.ok and "response" in res.json():
        ai_response = res.json()["response"]
        # Append to chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("MediSage AI", ai_response))
    else:
        st.error("❌ Error getting response. Make sure a file is uploaded first.")

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 🗂 Chat History")
    for speaker, msg in st.session_state.chat_history[::-1]:
        with st.chat_message(speaker if speaker == "You" else "assistant"):
            st.markdown(msg)
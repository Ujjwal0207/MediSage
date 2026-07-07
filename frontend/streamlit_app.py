import os
import uuid

import requests
import streamlit as st

API_BASE = os.getenv("MEDISAGE_API_URL", "https://medisage-51pi.onrender.com")


def build_headers() -> dict[str, str]:
    headers = {"X-Session-ID": st.session_state.session_id}
    api_key = os.getenv("MEDISAGE_API_KEY") or st.secrets.get("MEDISAGE_API_KEY", "")
    if api_key:
        headers["X-API-Key"] = api_key
    return headers


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="MediSage AI", page_icon="🩺", layout="centered")

st.title("🩺 MediSage AI Medical Assistant")
st.markdown("Upload your *PDF medical report* and ask any health-related question.")

with st.expander("📄 Upload Medical Report", expanded=True):
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file:
        with st.spinner("Uploading and processing the PDF..."):
            res = requests.post(
                f"{API_BASE}/upload",
                files={"file": uploaded_file},
                headers=build_headers(),
            )
        if res.ok:
            st.success("✅ File uploaded and processed successfully.")
            st.session_state.chat_history = []
        else:
            payload = res.json()
            detail = payload.get("detail", "Failed to upload. Try again.")
            if isinstance(detail, list):
                detail = detail[0].get("msg", str(detail)) if detail else "Failed to upload."
            st.error(f"❌ {detail}")

st.markdown("### 💬 Ask Your Medical Question")
user_input = st.text_input("Type your question here:")

if user_input:
    with st.spinner("Consulting the AI doctor..."):
        res = requests.post(
            f"{API_BASE}/query",
            json={"session_id": st.session_state.session_id, "query": user_input},
            headers=build_headers(),
        )

    payload = res.json()
    if res.ok and "response" in payload:
        ai_response = payload["response"]
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("MediSage AI", ai_response))
    else:
        error_message = payload.get("error", payload.get("detail", "Error getting response."))
        st.error(f"❌ {error_message}")

if st.session_state.chat_history:
    st.markdown("### 🗂 Chat History")
    for speaker, msg in st.session_state.chat_history[::-1]:
        with st.chat_message("user" if speaker == "You" else "assistant"):
            st.markdown(msg)


# 🧠 MediSage : Making Medical Reports Understandable for Everyone

**MediSage** is a smart healthcare assistant designed to help patients — especially those with limited medical knowledge — understand their diagnostic reports and make informed decisions.

### 💡 The Vision

Millions of people undergo medical tests but struggle to interpret the results. Many visit doctors just to understand basic terms, while others delay or avoid follow-up care. **MediSage** bridges this gap by reading medical reports (like blood tests, lipid profiles, etc.), explaining them in simple terms, answering follow-up questions, and helping users decide what to do next — whether it's consulting a doctor, waiting, or self-care.

In the future, this system will evolve into a full-fledged platform that:
- **Evaluates the urgency of a condition**
- **Recommends verified doctors based on the report**
- **Allows helpers to support patients (especially elderly or digitally unaware)**
- **Works via SMS or low-bandwidth methods**
- **Rewards users who refer or assist others**

---

## 🧩 Project Roadmap

### ✅ **Phase 1: AI-powered Report Chatbot** *(Completed)*

- Upload medical PDF reports
- Use a **RAG (Retrieval-Augmented Generation)** system to extract insights
- Ask questions and get responses using **Gemini 1.5**
- Backend powered by **FastAPI**, deployed on Render
- Frontend built with **Streamlit**, hosted on Streamlit Cloud
- Chat history preserved in the UI

### 🏥 **Phase 2: Medical Triage System** *(Planned)*

- Based on symptoms + report → AI decides:
  - Emergency attention needed
  - Routine doctor consultation
  - Self-care okay

### 🧑‍⚕️ **Phase 3: Doctor Recommendation Engine**

- Suggest verified doctors using:
  - Specialization needed (from report)
  - Location proximity
  - Ratings & availability

### 👥 **Phase 4: Helpers & Assisted Mode**

- Let friends/family upload reports on behalf of others
- SMS notifications for patients
- Reward helpers who refer or assist others

### 📲 **Phase 5: Mobile & Offline Support**

- Android/iOS apps with offline-first features
- Support for users with no smartphones: Use **SMS** to interact

---

## 🌐 Live Demo

- **Frontend (Streamlit)**: [https://medisagegit-m7fgqgz8ez4teqzk2zysja.streamlit.app](https://medisagegit-m7fgqgz8ez4teqzk2zysja.streamlit.app)
- **Backend (FastAPI)**: [https://medisage-51pi.onrender.com](https://medisage-51pi.onrender.com)
<img width="1280" height="715" alt="Screenshot 2025-07-30 at 9 50 09 PM" src="https://github.com/user-attachments/assets/10db611d-cb09-4bd6-bf4c-7e563b9f10b4" />

  

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLM**: Gemini 1.5 Pro (Google Generative AI)
- **Retrieval**: FAISS + Custom RAG Pipeline
- **Deployment**: Render + Streamlit Cloud

---
## 📂 Project Structure

```
MediSage:
  backend:
    main.py: "FastAPI server with /upload and /query routes"
    rag:
      loader.py: "Handles PDF text extraction"
      retriever.py: "Creates and queries FAISS vectorstore"
      embedder.py: "Encodes text using OpenAI or Google embeddings"
      prompt_builder.py: "Constructs prompts for the LLM"
  frontend:
    streamlit_app.py: "Streamlit-based user interface for chatbot"
    requirements.txt: "Python dependencies for frontend"
  .env: "Environment variables including API keys"
  README.md: "Project documentation"
  .gitignore: "Specifies files to ignore in version control"


```
---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.10+
- Google API Key (for Gemini)
- FAISS library: `pip install faiss-cpu`
- `.env` file in root:

```env
GOOGLE_API_KEY="your-google-api-key"
```
1. Clone the Repository
```
git clone [https://github.com/yourusername/ai-med-bot.git](https://github.com/Ujjwal0207/MediSage.git)
```
2. Run Backend
```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
3. Run Frontend
```
cd ../frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

⚠️ **Disclaimer**

This tool is for educational and informational purposes only.  
It is **not** a replacement for professional medical advice.  
Always consult a licensed doctor for medical decisions.

🤝 **Contributing**

Pull requests are welcome!  
If you’d like to improve the UI, add new functionality, or extend the triage logic — open an issue or PR.



# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from rag.loader import extract_text_from_pdf
from rag.retriever import create_vectorstore, retrieve_relevant_docs
from rag.prompt_builder import build_prompt
from google.generativeai import GenerativeModel
import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorstore = None

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global vectorstore
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = extract_text_from_pdf(tmp_path)
    vectorstore = create_vectorstore(text)
    return {"message": "PDF uploaded and processed successfully."}


@app.get("/query")
async def query_bot(query: str):
    if not vectorstore:
        return {"error": "No PDF uploaded yet."}

    docs = retrieve_relevant_docs(query, vectorstore)
    prompt = build_prompt(query, docs)

    model = GenerativeModel("models/gemini-1.5-flash")


    chat = model.start_chat()
    response = chat.send_message(prompt)

    return {"response": response.text}

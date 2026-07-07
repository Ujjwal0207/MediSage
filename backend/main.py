# main.py
import os
import tempfile
import uuid

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.generativeai import GenerativeModel
from pydantic import BaseModel, Field

from rag.loader import extract_text_from_pdf
from rag.prompt_builder import build_prompt
from rag.retriever import create_vectorstore, retrieve_relevant_docs
from rag.safety import append_disclaimer, get_emergency_response, is_emergency_query

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorstores: dict[str, object] = {}


class QueryRequest(BaseModel):
    session_id: str
    query: str = Field(..., min_length=1)


def validate_session_id(session_id: str) -> str:
    try:
        return str(uuid.UUID(session_id))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid session_id") from exc


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_session_id: str = Header(..., alias="X-Session-ID"),
):
    session_id = validate_session_id(x_session_id)
    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)
        vectorstores[session_id] = create_vectorstore(text)
        return {"message": "PDF uploaded and processed successfully."}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/query")
async def query_bot(body: QueryRequest):
    session_id = validate_session_id(body.session_id)
    vectorstore = vectorstores.get(session_id)

    if not vectorstore:
        return {"error": "No PDF uploaded yet for this session."}

    if is_emergency_query(body.query):
        return {"response": get_emergency_response()}

    docs = retrieve_relevant_docs(body.query, vectorstore)
    prompt = build_prompt(body.query, docs)

    model = GenerativeModel("models/gemini-1.5-flash")
    chat = model.start_chat()
    response = chat.send_message(prompt)

    return {"response": append_disclaimer(response.text)}

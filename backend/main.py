# main.py
import os
import tempfile
import uuid
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Header, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.generativeai import GenerativeModel
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from rag.guards import validate_pdf_bytes, verify_api_key
from rag.loader import PDFExtractionError, extract_text_from_pdf
from rag.prompt_builder import build_prompt
from rag.retriever import create_vectorstore, retrieve_relevant_docs
from rag.safety import append_disclaimer, get_emergency_response, is_emergency_query

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

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
@limiter.limit("5/minute")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    x_session_id: str = Header(..., alias="X-Session-ID"),
    _: None = Depends(verify_api_key),
):
    session_id = validate_session_id(x_session_id)
    content = await file.read()
    validate_pdf_bytes(content)

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        page_docs = extract_text_from_pdf(tmp_path)
        vectorstores[session_id] = create_vectorstore(page_docs)
        return {"message": "PDF uploaded and processed successfully."}
    except PDFExtractionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/query")
@limiter.limit("20/minute")
async def query_bot(
    request: Request,
    body: QueryRequest,
    _: None = Depends(verify_api_key),
):
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

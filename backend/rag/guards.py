import os

from fastapi import Header, HTTPException

MAX_UPLOAD_BYTES = int(os.getenv("MEDISAGE_MAX_UPLOAD_MB", "10")) * 1024 * 1024
MEDISAGE_API_KEY = os.getenv("MEDISAGE_API_KEY")
PDF_MAGIC = b"%PDF"


def verify_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    if not MEDISAGE_API_KEY:
        return
    if not x_api_key or x_api_key != MEDISAGE_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


def validate_pdf_bytes(content: bytes) -> None:
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(content) > MAX_UPLOAD_BYTES:
        max_mb = MAX_UPLOAD_BYTES // (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum upload size is {max_mb} MB.",
        )

    if not content.startswith(PDF_MAGIC):
        raise HTTPException(status_code=400, detail="File is not a valid PDF.")

from langchain_core.documents import Document
from PyPDF2 import PdfReader

MIN_EXTRACTED_CHARS = 100


class PDFExtractionError(Exception):
    """Raised when a PDF yields too little readable text."""


def _char_count(docs: list[Document]) -> int:
    return sum(len(doc.page_content.strip()) for doc in docs)


def _extract_with_pypdf2(pdf_path: str) -> list[Document]:
    reader = PdfReader(pdf_path)
    docs: list[Document] = []

    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            docs.append(Document(page_content=text, metadata={"page": index, "source": "pypdf2"}))

    return docs


def _extract_with_pymupdf(pdf_path: str) -> list[Document]:
    try:
        import fitz
    except ImportError:
        return []

    docs: list[Document] = []
    with fitz.open(pdf_path) as pdf:
        for index, page in enumerate(pdf, start=1):
            text = (page.get_text() or "").strip()
            if text:
                docs.append(Document(page_content=text, metadata={"page": index, "source": "pymupdf"}))

    return docs


def _extract_with_ocr(pdf_path: str) -> list[Document]:
    try:
        from pdf2image import convert_from_path
        import pytesseract
    except ImportError:
        return []

    try:
        pytesseract.get_tesseract_version()
    except Exception:
        return []

    docs: list[Document] = []
    try:
        images = convert_from_path(pdf_path)
    except Exception:
        return []

    for index, image in enumerate(images, start=1):
        text = (pytesseract.image_to_string(image) or "").strip()
        if text:
            docs.append(Document(page_content=text, metadata={"page": index, "source": "ocr"}))

    return docs


def extract_text_from_pdf(pdf_path: str) -> list[Document]:
    extractors = (_extract_with_pypdf2, _extract_with_pymupdf, _extract_with_ocr)
    best_docs: list[Document] = []

    for extractor in extractors:
        docs = extractor(pdf_path)
        if _char_count(docs) > _char_count(best_docs):
            best_docs = docs

    if _char_count(best_docs) < MIN_EXTRACTED_CHARS:
        raise PDFExtractionError(
            "Could not extract enough readable text from this PDF. "
            "The file may be scanned, encrypted, or low quality. "
            "Try a text-based PDF or ensure Tesseract OCR is installed on the server."
        )

    return best_docs

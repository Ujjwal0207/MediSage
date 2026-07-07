from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from .embedder import get_embedder

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
RETRIEVAL_K = 8
RETRIEVAL_FETCH_K = 24


def _build_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", "; ", ", ", " ", ""],
    )


def create_vectorstore(page_docs: list[Document]):
    splitter = _build_splitter()
    chunks = splitter.split_documents(page_docs)
    return FAISS.from_documents(chunks, get_embedder())


def retrieve_relevant_docs(query: str, vectorstore, k: int = RETRIEVAL_K):
    return vectorstore.max_marginal_relevance_search(
        query,
        k=k,
        fetch_k=RETRIEVAL_FETCH_K,
    )

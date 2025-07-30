#retriever
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .embedder import get_embedder

def create_vectorstore(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=chunk) for chunk in splitter.split_text(text)]
    return FAISS.from_documents(docs, get_embedder())

def retrieve_relevant_docs(query: str, vectorstore, k: int = 3):
    return vectorstore.similarity_search(query, k=k)

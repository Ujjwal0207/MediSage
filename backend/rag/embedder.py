from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

# embeddings

class GeminiEmbedder(Embeddings):
    def __init__(self):
        self.embedder = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            api_key=os.getenv("GOOGLE_API_KEY") 
        )

    def embed_documents(self, texts):
        return self.embedder.embed_documents(texts)

    def embed_query(self, text):
        return self.embedder.embed_query(text)

def get_embedder():
    return GeminiEmbedder()

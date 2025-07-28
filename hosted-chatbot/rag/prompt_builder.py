# prompt
def build_prompt(query: str, documents: list):
    context = "\n\n".join(doc.page_content for doc in documents)
    return f"""You are a helpful medical assistant. Answer the question based on the following report data.

Report Content:
{context}

Question:
{query}

Answer:"""

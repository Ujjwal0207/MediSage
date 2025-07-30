def build_prompt(query: str, docs) -> str:
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"""
You are a highly knowledgeable and helpful AI medical assistant.

Below is the extracted content from a patient's medical report:

--- Start of Medical Report ---
{context}
--- End of Medical Report ---

Answer the following user question using the report above. If a medical parameter (like RBC count, hemoglobin, cholesterol, etc.) is outside the normal range, mention the possible diseases or health issues it may indicate. Be concise, helpful, and explain whether the values are in a healthy range or not.

User Question: "{query}"

Give a clear and medically accurate answer.
"""
    return prompt

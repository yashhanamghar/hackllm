from app.vector_store import FAISSVectorStore, chunk_text
from app.llm_client import get_openai_answer
vector_store = FAISSVectorStore()
def process_document_and_answer_questions(document_text: str, questions: list):
    chunks = chunk_text(document_text)
    vector_store.add_texts(chunks)
    results = []
    for question in questions:
        top_chunks = vector_store.search(question, k=1)  # Use fewer chunks
        combined_context = "\n\n".join([chunk for chunk, _ in top_chunks])
        combined_context = combined_context[:3000]  # Trim to avoid token overflow
        answer = get_openai_answer(combined_context, question)
        results.append({"question": question, "answer": answer})
    return results
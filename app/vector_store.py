import faiss
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

class FAISSVectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)
        self.text_chunks = []

    def add_texts(self, texts: List[str]):
        embeddings = model.encode(texts)
        self.index.add(np.array(embeddings).astype("float32"))
        self.text_chunks.extend(texts)

    def search(self, query: str, k: int = 1) -> List[Tuple[str, float]]:
        q_embedding = model.encode([query]).astype("float32")
        D, I = self.index.search(q_embedding, k)
        return [(self.text_chunks[i], float(D[0][idx])) for idx, i in enumerate(I[0])]

def chunk_text(text: str, chunk_size=500, chunk_overlap=200) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


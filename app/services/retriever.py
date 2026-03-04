import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

DATA_DIR = "data"
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(DATA_DIR, "chunks.pkl")


class Retriever:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        if not os.path.exists(INDEX_PATH):
            raise Exception("FAISS index not found. Please upload a document first.")

        self.index = faiss.read_index(INDEX_PATH)

        with open(CHUNKS_PATH, "rb") as f:
            self.chunks = pickle.load(f)

    def retrieve(self, query: str, k: int = 10):
        # query -> embedding
        query_embedding = self.model.encode([query])

        # search (returns distances (L2) and indices)
        distances, indices = self.index.search(np.array(query_embedding), k)

        results = []
        for pos, chunk_id in enumerate(indices[0]):
            # chunk_id is an integer index into self.chunks
            distance = float(distances[0][pos])
            text = self.chunks[chunk_id]
            # convert L2 distance to an intuitive similarity score (optional)
            similarity = 1.0 / (1.0 + distance)
            results.append({
                "chunk_id": int(chunk_id),
                "distance": distance,        # L2 distance (lower = closer)
                "score": similarity,         # normalized similarity (0..1-ish)
                "text": text
            })

        return results
import fitz  # PyMuPDF
import faiss
import numpy as np
import os
import pickle
import re
from sentence_transformers import SentenceTransformer


DATA_DIR = "data"
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(DATA_DIR, "chunks.pkl")


class IngestionService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    def extract_text(self, pdf_path: str) -> str:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text


    def chunk_text(self, text: str):
        # Split by numbered section headers like "1 Introduction", "3.1 Execution Overview"
        pattern = r"\n(?=\d+(?:\.\d+)*\s+[A-Z])"
        sections = re.split(pattern, text)

        # Clean and filter
        chunks = [sec.strip() for sec in sections if len(sec.strip()) > 200]

        return chunks

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        return chunks

    def build_and_save_index(self, chunks):
        embeddings = self.model.encode(chunks)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings))

        faiss.write_index(index, INDEX_PATH)

        with open(CHUNKS_PATH, "wb") as f:
            pickle.dump(chunks, f)
            


# 📄 ResearchAI — Research Paper Assistant

A production-style Retrieval-Augmented Generation (RAG) system that enables structured question answering over research papers using local LLMs, FAISS vector search, a FastAPI backend, and a Streamlit UI.

---

## 🚀 Overview

ResearchAI allows users to:

- 📥 Upload research papers (PDF)
- 🧠 Automatically generate a structured document overview
- 📑 Extract section headers (Index view)
- ❓ Ask grounded questions about the paper
- 📎 View source citations with similarity scores

The system uses **section-aware chunking** and **FAISS vector similarity search** to improve retrieval precision over naive fixed-length chunking.

---

## 🏗 System Architecture

```
Streamlit UI
     ↓
FastAPI Backend
     ↓
RAG Pipeline
     ↓
Retriever (FAISS)
     ↓
Local LLM (Ollama - Llama3)
```

---

## 🧠 Core Design Decisions

### 1️⃣ Section-Aware Chunking
Instead of naive character splitting, the document is split using structural section headers (e.g., `3.1 Execution Overview`).  
This significantly improves retrieval quality for research papers.

---

### 2️⃣ FAISS Vector Index (IndexFlatL2)
- Embedding model: `all-MiniLM-L6-v2`
- Distance metric: L2
- Stores embeddings only
- Text chunks stored separately

---

### 3️⃣ Structured Retrieval Output

Retriever returns structured results:

```json
{
  "chunk_id": int,
  "distance": float,
  "score": float,
  "text": string
}
```

This enables:
- Transparent similarity inspection
- Ranking-based UI display
- Explainable retrieval behavior

---

### 4️⃣ Strict Prompt Constraints

The LLM is instructed to:
- Use only retrieved context
- Avoid inference
- Avoid hallucination
- Return clean structured answers
- Respond “Not found in document” if context missing

---

### 5️⃣ Automatic Overview Generation

Upon upload:
- Entire document is indexed
- Overview is generated automatically
- Section headers extracted deterministically (regex-based)
- Displayed as index page in UI

---

## ⚙️ Tech Stack

- Python 3.11
- FastAPI
- FAISS
- SentenceTransformers
- Ollama (Llama3 local LLM)
- Streamlit
- PyMuPDF



---

## 🔬 Retrieval Improvements Implemented

| Technique | Reason |
|-----------|--------|
| Section-aware chunking | Improves semantic precision |
| Increased k retrieval | Improves recall |
| Strict prompt constraints | Reduces hallucination |
| Structured citation return | Improves explainability |

## 🧑‍💻 Author

Sharayu Nagre  
AI / ML Engineering Focus  
USC Viterbi

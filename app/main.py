from fastapi import FastAPI, UploadFile, File
import shutil
import os
from app.services.ingestion_service import IngestionService
from app.services.rag_pipeline import RAGPipeline



app = FastAPI()

DATA_DIR = "data"

ingestion_service = IngestionService()
rag_pipeline = None  


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global rag_pipeline

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    file_path = os.path.join(DATA_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = ingestion_service.extract_text(file_path)

    

    chunks = ingestion_service.chunk_text(text)
    ingestion_service.build_and_save_index(chunks)

    rag_pipeline = RAGPipeline()


    overview = rag_pipeline.generate_overview()

    return {
        "message": "Document processed successfully",
        "overview": overview["overview"],
       
    }


@app.post("/ask")
async def ask_question(question: str):
    if rag_pipeline is None:
        return {"error": "Please upload a document first."}

    return rag_pipeline.generate_answer(question)

@app.get("/overview")
async def overview():
    if rag_pipeline is None:
        return {"error": "Please upload a document first."}

    return rag_pipeline.generate_overview()
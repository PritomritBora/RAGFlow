from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict
from ..orchestrator import ResearchOrchestrator
from ..config import settings
import tempfile
import os

router = APIRouter()
orchestrator = ResearchOrchestrator(settings)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    citations: List[Dict]
    confidence: float
    retrieval_steps: List[Dict]

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    result = await orchestrator.process_question(request.question)
    return result

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        orchestrator.ingest_document(tmp_path, {"source": file.filename})
        return {"status": "success", "filename": file.filename}
    finally:
        os.unlink(tmp_path)

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .orchestrator import ResearchOrchestrator
from .config import Settings
from .models import QueryRequest, QueryResponse, DocumentUpload
import shutil
from pathlib import Path
import uuid

app = FastAPI(title="Research Assistant API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = Settings()
orchestrator = ResearchOrchestrator(settings)

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process research question with advanced RAG pipeline"""
    try:
        result = await orchestrator.process_question(
            question=request.question,
            session_id=request.session_id,
            use_query_expansion=request.use_query_expansion,
            use_reranking=request.use_reranking
        )
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and index document (PDF or Markdown)"""
    try:
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        metadata = {
            "filename": file.filename,
            "type": file.content_type,
            "upload_id": str(uuid.uuid4())
        }
        
        # Process based on file type
        if file.filename.endswith('.pdf'):
            orchestrator.ingest_document(str(file_path), metadata)
        elif file.filename.endswith(('.md', '.markdown')):
            chunks = orchestrator.processor.process_markdown(str(file_path), metadata)
            orchestrator.vector_store.add_documents(chunks)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        return {
            "message": "Document uploaded and indexed",
            "filename": file.filename,
            "chunks": "processed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}/history")
async def get_session_history(session_id: str):
    """Get conversation history for a session"""
    session = orchestrator.memory.load_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.post("/session/new")
async def create_session():
    """Create new conversation session"""
    session_id = str(uuid.uuid4())
    session = orchestrator.memory.create_session(session_id)
    return {"session_id": session_id}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0"}

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        collection_info = orchestrator.vector_store.client.get_collection(
            orchestrator.settings.collection_name
        )
        return {
            "total_documents": collection_info.points_count,
            "vector_size": collection_info.config.params.vectors.size,
            "active_sessions": len(orchestrator.memory.sessions)
        }
    except Exception as e:
        return {"error": str(e)}

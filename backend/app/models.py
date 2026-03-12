from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    use_query_expansion: bool = True
    use_reranking: bool = True

class Citation(BaseModel):
    id: int
    source: str
    relevance: float
    section: Optional[str] = None
    text_preview: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: float
    retrieval_steps: List[Dict[str, str]]
    query_analysis: Dict
    validation: Dict

class DocumentUpload(BaseModel):
    file_path: str
    metadata: Dict = Field(default_factory=dict)

class QueryAnalysis(BaseModel):
    query_type: str = Field(description="Type: comparison, summary, factual, multi-hop")
    sub_queries: List[str] = Field(description="Decomposed sub-questions")
    requires_multi_hop: bool = Field(description="Whether multi-hop retrieval needed")

class Evaluation(BaseModel):
    confidence: float = Field(ge=0.0, le=1.0)
    is_supported: bool
    missing_info: List[str] = Field(default_factory=list)
    reasoning: str

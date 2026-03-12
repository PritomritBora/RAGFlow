# System Architecture

## Overview

Multi-hop RAG system with advanced query processing, self-evaluation, and citation tracking.

## Pipeline Flow

```
User Query
    ↓
Query Analyzer (classify & decompose)
    ↓
Query Expander (generate variations)
    ↓
Retrieval Planner (create retrieval steps)
    ↓
Multi-Hop Retriever (execute steps)
    ↓
Reranker (improve relevance)
    ↓
Answer Generator (synthesize response)
    ↓
Citation Extractor (link sources)
    ↓
Self-Evaluator (assess quality)
    ↓
[Low confidence? → Additional retrieval]
    ↓
Response with citations & metadata
```

## Components

### Agents (Decision Makers)

**QueryAnalyzerAgent**
- Classifies query type (comparison, summary, factual, multi-hop)
- Decomposes complex questions into sub-queries
- Determines if multi-hop retrieval needed

**RetrievalPlannerAgent**
- Creates ordered retrieval steps
- Each step has query + reasoning
- Optimizes for information gathering

**AnswerGeneratorAgent**
- Synthesizes answer from retrieved context
- Adds inline citations
- Maintains factual accuracy

**SelfEvaluationAgent**
- Evaluates answer quality
- Assigns confidence score (0-1)
- Identifies missing information
- Triggers re-retrieval if needed

### Services (Execution Layer)

**VectorStore**
- Manages Qdrant vector database
- Handles document indexing
- Performs similarity search
- Uses OpenAI embeddings (text-embedding-3-small)

**MultiHopRetriever**
- Executes retrieval plan steps
- Aggregates results across steps
- Deduplicates chunks
- Formats context for LLM

**DocumentProcessor**
- Processes PDFs and Markdown
- Uses AdvancedChunker for smart splitting
- Preserves document structure
- Extracts metadata

**AdvancedChunker**
- Semantic-aware text splitting
- Preserves section headers
- Maintains context overlap
- Configurable chunk size

**QueryExpander**
- Generates query variations
- Adds synonyms and related terms
- Creates technical/layman versions
- Improves retrieval recall

**Reranker**
- LLM-based relevance scoring
- Combines with vector similarity
- Improves precision
- Configurable top-k

**CitationExtractor**
- Extracts citations from answers
- Links to source chunks
- Validates claim support
- Calculates support ratio

**ConversationMemory**
- Tracks session history
- Resolves follow-up questions
- Persists to disk
- Provides context for continuity

## Data Models

**QueryRequest**
```python
{
    "question": str,
    "session_id": Optional[str],
    "use_query_expansion": bool,
    "use_reranking": bool
}
```

**QueryResponse**
```python
{
    "answer": str,
    "citations": List[Citation],
    "confidence": float,
    "retrieval_steps": List[Dict],
    "query_analysis": Dict,
    "validation": Dict
}
```

**Citation**
```python
{
    "id": int,
    "source": str,
    "relevance": float,
    "section": Optional[str],
    "text_preview": Optional[str]
}
```

## Technology Stack

### Backend
- **Framework**: FastAPI
- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector DB**: Qdrant
- **Orchestration**: LangChain
- **Language**: Python 3.9+

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: CSS (custom)
- **State**: React hooks

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Storage**: Qdrant volumes

## Key Features

### 1. Multi-Hop Retrieval
Breaks complex questions into steps, retrieves relevant information for each step, and aggregates results.

### 2. Query Expansion
Generates multiple query variations to improve retrieval coverage and handle vocabulary mismatch.

### 3. Reranking
Uses LLM to score retrieved chunks for relevance, improving precision beyond vector similarity.

### 4. Self-Evaluation
Assesses answer quality and triggers additional retrieval if confidence is low (<0.7).

### 5. Citation Tracking
Links every claim to source documents with relevance scores and text previews.

### 6. Conversation Memory
Maintains session context for follow-up questions and conversation continuity.

## Configuration

Environment variables (`.env`):
```bash
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
QDRANT_HOST=localhost
QDRANT_PORT=6333
COLLECTION_NAME=research_docs
```

## API Endpoints

- `POST /query` - Process research question
- `POST /upload` - Upload and index document
- `POST /session/new` - Create conversation session
- `GET /session/{id}/history` - Get session history
- `GET /health` - Health check
- `GET /stats` - System statistics

## Performance Considerations

**Latency Sources:**
1. Query analysis: ~1-2s
2. Query expansion: ~1-2s (if enabled)
3. Vector search: ~100-500ms per step
4. Reranking: ~2-3s (if enabled)
5. Answer generation: ~3-5s
6. Self-evaluation: ~1-2s

**Total**: 8-15s per query (varies with complexity)

**Optimization Strategies:**
- Disable query expansion for simple queries
- Disable reranking for high-quality vector results
- Cache embeddings for repeated queries
- Parallel retrieval for independent steps
- Batch LLM calls where possible

## Scalability

**Current Limitations:**
- Single instance (no horizontal scaling)
- In-memory session storage
- No request queuing
- No rate limiting

**Future Improvements:**
- Redis for session storage
- Message queue for async processing
- Load balancer for multiple instances
- Rate limiting per user/API key
- Caching layer (Redis/Memcached)

# Intelligent Research Assistant

Advanced multi-hop RAG system with query expansion, reranking, and verified citations for complex document analysis.

## Architecture

```
Query → Analyzer → Expander → Planner → Multi-Hop Retrieval → Reranker → 
Answer Generator → Citation Extractor → Self-Evaluator → [Re-retrieval if needed] → Response
```

## Key Features

- **Multi-hop Retrieval**: Breaks complex questions into steps for comprehensive answers
- **Query Expansion**: Generates query variations to improve retrieval coverage
- **LLM Reranking**: Scores chunks for relevance beyond vector similarity
- **Self-Evaluation**: Assesses answer quality and triggers re-retrieval if confidence < 70%
- **Citation Tracking**: Links every claim to source documents with validation
- **Conversation Memory**: Maintains context for follow-up questions
- **PDF/Markdown Support**: Smart chunking that preserves document structure

## Quick Start

**Automated (Recommended):**
```bash
./start.sh
```

**Manual:**
```bash
# 1. Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env and add your OPENAI_API_KEY

# 2. Start services
docker-compose up -d

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
# Qdrant: http://localhost:6333/dashboard
```

## Documentation

- [Setup Guide](SETUP.md) - Detailed installation and configuration
- [Architecture](ARCHITECTURE.md) - System design and components
- [TODO](TODO.md) - Development roadmap and known issues

## Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Test System:**
```bash
cd backend
python test_system.py
```

## Example Queries

- "Compare the optimization techniques mentioned in these ML papers"
- "What security vulnerabilities are discussed across these reports?"
- "Summarize the key differences between the API implementations"
- "What are the main conclusions from the research?"

## Tech Stack

**Backend:**
- FastAPI (API framework)
- LangChain (LLM orchestration)
- Qdrant (vector database)
- OpenAI GPT-4o-mini (LLM)
- OpenAI text-embedding-3-small (embeddings)

**Frontend:**
- React 18 (UI framework)
- Vite (build tool)
- Custom CSS (styling)

**Infrastructure:**
- Docker & Docker Compose
- Python 3.9+
- Node.js 18+

## Project Status

✅ Core pipeline implemented
✅ All agents and services functional
✅ Frontend UI complete
✅ Docker deployment ready
⚠️ Needs comprehensive error handling
⚠️ Needs unit/integration tests
⚠️ Needs production optimizations

See [TODO.md](TODO.md) for detailed development roadmap.

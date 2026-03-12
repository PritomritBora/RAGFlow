# Setup Guide

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API Key

## Quick Start

### 1. Environment Setup

```bash
# Copy environment file
cp backend/.env.example backend/.env

# Edit backend/.env and add your OpenAI API key
# OPENAI_API_KEY=sk-...
```

### 2. Start with Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f backend
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Qdrant Dashboard: http://localhost:6333/dashboard

### 3. Local Development (Alternative)

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

**Qdrant (separate terminal):**
```bash
docker run -p 6333:6333 qdrant/qdrant:latest
```

## Testing the System

### 1. Upload Documents

Use the "Upload Document" button in the UI to upload PDF or Markdown files.

### 2. Ask Questions

Try these example queries:
- "What are the main topics discussed in the documents?"
- "Compare the approaches mentioned in different sources"
- "Summarize the key findings"

### 3. Check API Health

```bash
curl http://localhost:8000/health
curl http://localhost:8000/stats
```

## Troubleshooting

**Issue: Backend fails to start**
- Check if OPENAI_API_KEY is set in .env
- Verify Qdrant is running: `curl http://localhost:6333`

**Issue: Frontend can't connect to backend**
- Check CORS settings in backend/app/main.py
- Verify backend is running on port 8000

**Issue: No results from queries**
- Upload documents first
- Check Qdrant has indexed documents: http://localhost:6333/dashboard

## Development Tips

- Backend auto-reloads on code changes with `--reload` flag
- Frontend hot-reloads automatically with Vite
- Check backend logs for detailed query processing steps
- Use `/docs` endpoint for interactive API testing

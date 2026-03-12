#!/bin/bash

# Quick start script for Research Assistant

set -e

echo "🚀 Starting Research Assistant..."
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env"
    echo ""
    echo "⚠️  IMPORTANT: Edit backend/.env and add your OPENAI_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Check if OPENAI_API_KEY is set
if grep -q "your_openai_api_key_here" backend/.env; then
    echo "❌ Please set your OPENAI_API_KEY in backend/.env"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Environment configured"
echo ""

# Start services
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check backend health
echo "🔍 Checking backend health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Backend failed to start. Check logs with: docker-compose logs backend"
        exit 1
    fi
    sleep 1
done

# Check Qdrant
echo "🔍 Checking Qdrant..."
if curl -s http://localhost:6333 > /dev/null 2>&1; then
    echo "✅ Qdrant is ready"
else
    echo "⚠️  Qdrant may not be ready yet"
fi

echo ""
echo "✅ All services started successfully!"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000/docs"
echo "   Qdrant:    http://localhost:6333/dashboard"
echo ""
echo "📝 Next steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Upload some documents (PDF or Markdown)"
echo "   3. Ask research questions"
echo ""
echo "🛠️  Useful commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart:       docker-compose restart"
echo ""

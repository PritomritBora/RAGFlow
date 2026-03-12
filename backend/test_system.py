#!/usr/bin/env python3
"""
Simple system test to verify the RAG pipeline works
"""
import asyncio
from app.orchestrator import ResearchOrchestrator
from app.config import settings

async def test_basic_query():
    """Test basic query processing"""
    print("🧪 Testing Research Assistant System\n")
    
    try:
        # Initialize orchestrator
        print("1. Initializing orchestrator...")
        orchestrator = ResearchOrchestrator(settings)
        print("   ✓ Orchestrator initialized\n")
        
        # Test vector store connection
        print("2. Testing vector store connection...")
        collections = orchestrator.vector_store.client.get_collections()
        print(f"   ✓ Connected to Qdrant, collections: {len(collections.collections)}\n")
        
        # Test query processing (will work even without documents)
        print("3. Testing query processing...")
        test_question = "What is machine learning?"
        
        result = await orchestrator.process_question(
            question=test_question,
            use_query_expansion=False,
            use_reranking=False
        )
        
        print(f"   ✓ Query processed successfully")
        print(f"   - Confidence: {result['confidence']:.2f}")
        print(f"   - Query type: {result['query_analysis']['type']}")
        print(f"   - Multi-hop: {result['query_analysis']['requires_multi_hop']}")
        print(f"   - Retrieval steps: {len(result['retrieval_steps'])}")
        print(f"   - Citations: {len(result['citations'])}\n")
        
        print("✅ All tests passed!")
        print("\nNote: If no documents are indexed, the answer will indicate")
        print("insufficient context. Upload documents via the API to test full pipeline.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_basic_query())

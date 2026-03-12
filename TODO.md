# Development TODO

## High Priority

### Backend
- [ ] Add comprehensive error handling in orchestrator.py
  - Handle OpenAI API errors (rate limits, timeouts)
  - Handle Qdrant connection failures
  - Add retry logic for transient failures

- [ ] Improve citation extraction
  - Better matching between answer citations and source chunks
  - Handle edge cases (multiple sources with same name)
  - Add page number tracking for PDFs

- [ ] Add logging configuration
  - Structured logging with proper levels
  - Log rotation
  - Request ID tracking

- [ ] Add input validation
  - Question length limits
  - File size limits for uploads
  - Supported file type validation

### Frontend
- [ ] Add loading states and progress indicators
  - Show retrieval steps in real-time
  - Progress bar for document upload
  - Skeleton loaders

- [ ] Error handling and user feedback
  - Display API errors gracefully
  - Retry failed requests
  - Toast notifications

- [ ] Improve citation display
  - Click to expand full source text
  - Highlight cited sections
  - Link citations in answer to source panel

- [ ] Add conversation history UI
  - View past sessions
  - Search through history
  - Export conversations

## Medium Priority

### Backend
- [ ] Add caching layer
  - Cache embeddings for repeated queries
  - Cache LLM responses for identical questions
  - Redis integration

- [ ] Improve document processing
  - Better PDF text extraction (handle tables, images)
  - Support for more formats (DOCX, HTML)
  - Extract and preserve document structure

- [ ] Add metrics and monitoring
  - Query latency tracking
  - Token usage monitoring
  - Success/failure rates

- [ ] Implement user authentication
  - API key management
  - Rate limiting per user
  - Usage quotas

### Frontend
- [ ] Add advanced query options
  - Toggle query expansion on/off
  - Toggle reranking on/off
  - Adjust confidence threshold

- [ ] Improve mobile responsiveness
  - Better layout for small screens
  - Touch-friendly interactions

- [ ] Add data visualization
  - Query type distribution
  - Confidence score trends
  - Source usage statistics

## Low Priority

### Backend
- [ ] Add unit tests
  - Test each agent independently
  - Test service layer
  - Mock external dependencies

- [ ] Add integration tests
  - End-to-end query processing
  - Document upload and retrieval
  - Session management

- [ ] Performance optimization
  - Parallel retrieval for multiple steps
  - Batch embedding generation
  - Query result caching

- [ ] Add more LLM providers
  - Anthropic Claude support
  - Local model support (Ollama)
  - Configurable model selection

### Frontend
- [ ] Add keyboard shortcuts
  - Quick submit (Cmd/Ctrl + Enter)
  - Navigate history
  - Focus search

- [ ] Add export functionality
  - Export answers as PDF
  - Export citations as BibTeX
  - Share conversation links

- [ ] Add dark/light theme toggle
- [ ] Add accessibility improvements (ARIA labels, keyboard navigation)

## Known Issues

1. **Citation Model Mismatch** - ✅ FIXED
   - Citations now properly converted to Citation model

2. **Config Instantiation** - ✅ FIXED
   - Settings now instantiated at module level

3. **Advanced Chunker** - ✅ FIXED
   - Regex pattern corrected

4. **Missing Error Handling**
   - API routes need try-catch blocks
   - Frontend needs error boundaries

5. **No Rate Limiting**
   - OpenAI API calls not rate limited
   - Could hit API limits quickly

## Future Enhancements

- [ ] Multi-modal support (images, tables, charts)
- [ ] Collaborative features (shared sessions, comments)
- [ ] Advanced analytics dashboard
- [ ] Plugin system for custom retrievers
- [ ] Webhook support for async processing
- [ ] GraphQL API option
- [ ] WebSocket support for real-time updates

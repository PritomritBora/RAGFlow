import { useState, useRef, useEffect } from 'react'
import ChatInterface from './components/ChatInterface'
import ChatMessage from './components/ChatMessage'
import TypingIndicator from './components/TypingIndicator'
import SourceViewer from './components/SourceViewer'
import QuickActions from './components/QuickActions'
import SessionManager from './components/SessionManager'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [currentResult, setCurrentResult] = useState(null)
  const [uploadStatus, setUploadStatus] = useState('')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, loading])

  const handleUpload = async (file) => {
    setUploading(true)
    setUploadStatus('Uploading...')
    
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8001/upload', {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        throw new Error('Upload failed')
      }
      
      const data = await response.json()
      setUploadStatus(`✓ ${file.name} uploaded successfully!`)
      
      // Clear status after 3 seconds
      setTimeout(() => setUploadStatus(''), 3000)
    } catch (error) {
      console.error('Upload failed:', error)
      setUploadStatus(`✗ Upload failed: ${error.message}`)
      setTimeout(() => setUploadStatus(''), 3000)
    } finally {
      setUploading(false)
    }
  }

  const handleQuery = async (question) => {
    // Add user message
    const userMessage = { text: question, isUser: true }
    setMessages(prev => [...prev, userMessage])
    setLoading(true)
    
    try {
      const response = await fetch('http://localhost:8001/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question,
          session_id: sessionId,
          use_query_expansion: true,
          use_reranking: true
        })
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Query failed')
      }
      
      const data = await response.json()
      
      // Add assistant message
      const assistantMessage = {
        text: data.answer,
        isUser: false,
        confidence: data.confidence,
        citations: data.citations
      }
      
      setMessages(prev => [...prev, assistantMessage])
      setCurrentResult(data)
    } catch (error) {
      console.error('Query failed:', error)
      const errorMessage = {
        text: `Sorry, I encountered an error: ${error.message}\n\nPlease check:\n• Your API key has credits\n• Backend is running\n• Documents are uploaded`,
        isUser: false,
        confidence: 0
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleExampleClick = (query) => {
    handleQuery(query)
  }

  return (
    <div className="app">
      <header>
        <h1>🔬 Research Assistant</h1>
        <p>Powered by Google Gemini • Multi-hop RAG with Citations</p>
        {uploadStatus && (
          <div className="upload-status">{uploadStatus}</div>
        )}
      </header>
      
      <div className="container">
        <div className="main-panel">
          <div className="top-bar">
            <SessionManager 
              onSessionChange={setSessionId} 
              currentSession={sessionId} 
            />
          </div>
          
          <div className="chat-container">
            {messages.length === 0 ? (
              <div className="welcome-screen">
                <div className="welcome-icon">💬</div>
                <h2>Start a Conversation</h2>
                <p>Upload documents using the 📎 button below and ask questions</p>
                
                <QuickActions 
                  onSelect={handleExampleClick} 
                  disabled={loading || uploading}
                />
              </div>
            ) : (
              <div className="messages-list">
                {messages.map((msg, i) => (
                  <ChatMessage key={i} message={msg} isUser={msg.isUser} />
                ))}
                {loading && <TypingIndicator />}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
        </div>
        
        {currentResult && (
          <div className="side-panel">
            <SourceViewer 
              citations={currentResult.citations} 
              steps={currentResult.retrieval_steps}
              analysis={currentResult.query_analysis}
              validation={currentResult.validation}
            />
          </div>
        )}
      </div>
      
      <ChatInterface 
        onSubmit={handleQuery} 
        onUpload={handleUpload}
        loading={loading || uploading} 
      />
    </div>
  )
}

export default App

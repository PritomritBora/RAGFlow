import { useState } from 'react'
import QueryInput from './components/QueryInput'
import AnswerPanel from './components/AnswerPanel'
import SourceViewer from './components/SourceViewer'
import DocumentUpload from './components/DocumentUpload'
import SessionManager from './components/SessionManager'
import './App.css'

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [history, setHistory] = useState([])

  const handleQuery = async (question) => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question,
          session_id: sessionId,
          use_query_expansion: true,
          use_reranking: true
        })
      })
      const data = await response.json()
      setResult(data)
      setHistory([...history, { question, result: data }])
    } catch (error) {
      console.error('Query failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>🔬 Research Assistant</h1>
        <p>Advanced multi-hop RAG with query expansion & reranking</p>
      </header>
      
      <div className="container">
        <div className="main-panel">
          <div className="top-bar">
            <DocumentUpload />
            <SessionManager 
              onSessionChange={setSessionId} 
              currentSession={sessionId} 
            />
          </div>
          
          <QueryInput onSubmit={handleQuery} loading={loading} />
          
          {result && <AnswerPanel result={result} />}
          
          {history.length > 1 && (
            <div className="history">
              <h3>Previous Questions</h3>
              {history.slice(0, -1).reverse().map((item, i) => (
                <div key={i} className="history-item" onClick={() => setResult(item.result)}>
                  <span className="history-q">{item.question}</span>
                  <span className="history-conf">{(item.result.confidence * 100).toFixed(0)}%</span>
                </div>
              ))}
            </div>
          )}
        </div>
        
        {result && (
          <div className="side-panel">
            <SourceViewer 
              citations={result.citations} 
              steps={result.retrieval_steps}
              analysis={result.query_analysis}
              validation={result.validation}
            />
          </div>
        )}
      </div>
    </div>
  )
}

export default App

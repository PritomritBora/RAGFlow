import { useState, useRef, useEffect } from 'react'
import './ChatInterface.css'

export default function ChatInterface({ onSubmit, loading, onUpload }) {
  const [message, setMessage] = useState('')
  const textareaRef = useRef(null)
  const fileInputRef = useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !loading) {
      onSubmit(message)
      setMessage('')
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleInput = (e) => {
    setMessage(e.target.value)
    // Auto-resize textarea
    e.target.style.height = 'auto'
    e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px'
  }

  const handleFileClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    if (file) {
      await onUpload(file)
      // Reset input
      e.target.value = ''
    }
  }

  return (
    <div className="chat-interface">
      <form onSubmit={handleSubmit} className="chat-input-form">
        <div className="input-wrapper">
          <button
            type="button"
            onClick={handleFileClick}
            className="attach-button"
            aria-label="Upload document"
            disabled={loading}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" />
            </svg>
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.md,.markdown"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <textarea
            ref={textareaRef}
            value={message}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about your documents..."
            rows={1}
            disabled={loading}
          />
          <button 
            type="submit" 
            disabled={loading || !message.trim()}
            className="send-button"
            aria-label="Send message"
          >
            {loading ? (
              <svg className="spinner" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" />
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
              </svg>
            )}
          </button>
        </div>
        <div className="input-hint">
          Press Enter to send, Shift + Enter for new line
        </div>
      </form>
    </div>
  )
}

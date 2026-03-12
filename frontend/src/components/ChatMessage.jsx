import './ChatMessage.css'

export default function ChatMessage({ message, isUser }) {
  return (
    <div className={`chat-message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-avatar">
        {isUser ? (
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
        )}
      </div>
      <div className="message-content">
        <div className="message-text">{message.text}</div>
        {message.confidence !== undefined && (
          <div className="message-meta">
            <span className="confidence-indicator" style={{
              color: message.confidence >= 0.8 ? '#22c55e' : 
                     message.confidence >= 0.6 ? '#eab308' : '#ef4444'
            }}>
              {(message.confidence * 100).toFixed(0)}% confident
            </span>
            {message.citations && message.citations.length > 0 && (
              <span className="citation-count">
                {message.citations.length} source{message.citations.length > 1 ? 's' : ''}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

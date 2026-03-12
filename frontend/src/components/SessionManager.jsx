import { useState, useEffect } from 'react'

export default function SessionManager({ onSessionChange, currentSession }) {
  const [sessions, setSessions] = useState([])

  const createNewSession = async () => {
    try {
      const response = await fetch('http://localhost:8001/session/new', {
        method: 'POST'
      })
      const data = await response.json()
      onSessionChange(data.session_id)
    } catch (error) {
      console.error('Failed to create session:', error)
    }
  }

  return (
    <div className="session-manager">
      <button onClick={createNewSession} className="new-session-btn">
        + New Conversation
      </button>
      {currentSession && (
        <span className="current-session">
          Session: {currentSession.slice(0, 8)}...
        </span>
      )}
    </div>
  )
}

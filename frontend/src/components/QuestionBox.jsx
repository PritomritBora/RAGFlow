import { useState } from 'react'
import './QuestionBox.css'

function QuestionBox({ onAsk, loading }) {
  const [question, setQuestion] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (question.trim()) {
      onAsk(question)
    }
  }

  const examples = [
    "Compare the optimization techniques used in these ML papers.",
    "What are the security weaknesses discussed across these reports?",
    "Summarize the differences between the APIs described in these documents."
  ]

  return (
    <div className="question-box">
      <form onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a complex research question..."
          rows={4}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !question.trim()}>
          {loading ? 'Analyzing...' : 'Ask Question'}
        </button>
      </form>
      
      <div className="examples">
        <p>Example questions:</p>
        {examples.map((ex, i) => (
          <button
            key={i}
            className="example-btn"
            onClick={() => setQuestion(ex)}
            disabled={loading}
          >
            {ex}
          </button>
        ))}
      </div>
    </div>
  )
}

export default QuestionBox

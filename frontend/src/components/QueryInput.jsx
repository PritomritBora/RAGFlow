import { useState } from 'react'

export default function QueryInput({ onSubmit, loading }) {
  const [question, setQuestion] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (question.trim()) {
      onSubmit(question)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="query-input">
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a research question (e.g., 'Compare the optimization techniques in these ML papers')"
        rows={4}
        disabled={loading}
      />
      <button type="submit" disabled={loading || !question.trim()}>
        {loading ? 'Processing...' : 'Ask Question'}
      </button>
    </form>
  )
}

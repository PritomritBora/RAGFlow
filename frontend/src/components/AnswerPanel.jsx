export default function AnswerPanel({ result }) {
  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#22c55e'
    if (confidence >= 0.6) return '#eab308'
    return '#ef4444'
  }

  return (
    <div className="answer-panel">
      <div className="confidence-badge" style={{ backgroundColor: getConfidenceColor(result.confidence) }}>
        Confidence: {(result.confidence * 100).toFixed(0)}%
      </div>
      
      <div className="answer-content">
        <h3>Answer</h3>
        <p>{result.answer}</p>
      </div>
    </div>
  )
}

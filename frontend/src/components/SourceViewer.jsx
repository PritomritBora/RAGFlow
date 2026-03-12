export default function SourceViewer({ citations, steps, analysis, validation }) {
  // Handle missing data gracefully
  if (!analysis || !validation || !citations || !steps) {
    return (
      <div className="source-viewer">
        <h3>Loading...</h3>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
          Waiting for query results...
        </p>
      </div>
    )
  }

  return (
    <div className="source-viewer">
      <h3>Query Analysis</h3>
      <div className="analysis-box">
        <div className="analysis-item">
          <span className="label">Type:</span>
          <span className="value">{analysis.type || 'N/A'}</span>
        </div>
        <div className="analysis-item">
          <span className="label">Multi-hop:</span>
          <span className="value">{analysis.requires_multi_hop ? 'Yes' : 'No'}</span>
        </div>
        <div className="analysis-item">
          <span className="label">Support Ratio:</span>
          <span className="value">{(validation.support_ratio * 100).toFixed(0)}%</span>
        </div>
      </div>

      <h3>Retrieval Steps</h3>
      <div className="steps">
        {steps.map((step, i) => (
          <div key={i} className="step">
            <span className="step-number">{i + 1}</span>
            <div>
              <strong>{step.query}</strong>
              <p>{step.reason}</p>
            </div>
          </div>
        ))}
      </div>

      <h3>Sources ({citations.length})</h3>
      <div className="citations">
        {citations.map((citation) => (
          <div key={citation.id} className="citation">
            <span className="citation-number">[{citation.id}]</span>
            <div>
              <strong>{citation.source}</strong>
              {citation.section && <span className="section"> • {citation.section}</span>}
              <span className="relevance">
                Relevance: {(citation.relevance * 100).toFixed(0)}%
              </span>
              {citation.text_preview && (
                <p className="preview">{citation.text_preview}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

import './QuickActions.css'

const RESEARCH_TEMPLATES = [
  {
    icon: '📊',
    title: 'Summarize',
    query: 'Provide a comprehensive summary of the main topics and key findings in these documents'
  },
  {
    icon: '🔍',
    title: 'Key Points',
    query: 'What are the most important points and takeaways from these documents?'
  },
  {
    icon: '⚖️',
    title: 'Compare',
    query: 'Compare and contrast the different approaches, methodologies, or viewpoints presented'
  },
  {
    icon: '💡',
    title: 'Insights',
    query: 'What are the novel insights, innovations, or unique perspectives in these documents?'
  },
  {
    icon: '📈',
    title: 'Trends',
    query: 'What trends, patterns, or recurring themes can you identify across the documents?'
  },
  {
    icon: '❓',
    title: 'Questions',
    query: 'What questions or gaps in knowledge are raised by these documents?'
  },
  {
    icon: '🎯',
    title: 'Conclusions',
    query: 'What are the main conclusions and recommendations from these documents?'
  },
  {
    icon: '🔗',
    title: 'Connections',
    query: 'How do the ideas and concepts in these documents relate to each other?'
  }
]

export default function QuickActions({ onSelect, disabled }) {
  return (
    <div className="quick-actions">
      <h3>Quick Templates</h3>
      <div className="actions-grid">
        {RESEARCH_TEMPLATES.map((template, i) => (
          <button
            key={i}
            className="action-pill"
            onClick={() => onSelect(template.query)}
            disabled={disabled}
            title={template.query}
          >
            <span className="action-icon">{template.icon}</span>
            <span className="action-title">{template.title}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

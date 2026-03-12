from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from ..models import QueryAnalysis

class QueryAnalyzerAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Analyze the user's question and determine:
1. Query type (comparison, summary, factual, multi-hop)
2. Break into 2-4 sub-queries if complex
3. Whether multi-hop retrieval is needed

Examples:
- "Compare X and Y" → comparison, needs multi-hop
- "What is X?" → factual, single retrieval
- "Summarize differences" → summary, needs multi-hop"""),
            ("user", "{question}")
        ])
    
    def analyze(self, question: str) -> QueryAnalysis:
        chain = self.prompt | self.llm.with_structured_output(QueryAnalysis)
        return chain.invoke({"question": question})

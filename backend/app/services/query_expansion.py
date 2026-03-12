from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class ExpandedQueries(BaseModel):
    queries: List[str] = Field(description="Expanded query variations")

class QueryExpander:
    """Expand queries with synonyms, related terms, and reformulations"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Generate 3-5 query variations to improve retrieval.

Include:
- Synonyms and related terms
- Different phrasings
- Technical and layman versions
- Specific aspects of the question

Keep queries concise and focused."""),
            ("user", "Original query: {query}")
        ])
    
    def expand(self, query: str) -> List[str]:
        chain = self.prompt | self.llm.with_structured_output(ExpandedQueries)
        result = chain.invoke({"query": query})
        return [query] + result.queries  # Include original

from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class RetrievalPlan(BaseModel):
    steps: List[Dict[str, str]] = Field(description="Ordered retrieval steps with query and reason")

class RetrievalPlannerAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Create a retrieval plan for answering the question.
            
Break it into ordered steps. Each step should have:
- query: what to search for
- reason: why this step is needed

Return 2-4 steps maximum."""),
            ("user", "Question: {question}\nSub-queries: {sub_queries}")
        ])
    
    def plan(self, question: str, sub_queries: List[str]) -> RetrievalPlan:
        chain = self.prompt | self.llm.with_structured_output(RetrievalPlan)
        return chain.invoke({
            "question": question,
            "sub_queries": "\n".join(sub_queries)
        })

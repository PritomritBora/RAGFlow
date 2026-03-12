from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    is_supported: bool = Field(description="Whether answer is supported by sources")
    confidence: float = Field(description="Confidence score 0-1")
    missing_info: List[str] = Field(description="What information is missing")
    citation_valid: bool = Field(description="Whether citations are valid")

class SelfEvaluationAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Evaluate if the answer is supported by the provided context.
            
Check:
1. Is the answer grounded in sources?
2. Are citations valid?
3. Is any critical information missing?

Be strict. Return low confidence if answer makes unsupported claims."""),
            ("user", """Question: {question}
Answer: {answer}
Context: {context}""")
        ])
    
    def evaluate(self, question: str, answer: str, context: str) -> EvaluationResult:
        chain = self.prompt | self.llm.with_structured_output(EvaluationResult)
        return chain.invoke({
            "question": question,
            "answer": answer,
            "context": context
        })

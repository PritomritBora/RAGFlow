from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from ..models import Evaluation

class SelfEvaluationAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Evaluate if the answer is supported by context.

Check:
1. Are claims backed by provided context?
2. Are citations valid?
3. Is information complete?

Provide:
- confidence (0.0-1.0)
- is_supported (bool)
- missing_info (list of gaps)
- reasoning"""),
            ("user", "Question: {question}\n\nAnswer: {answer}\n\nContext: {context}")
        ])
    
    def evaluate(self, question: str, answer: str, context: str) -> Evaluation:
        chain = self.prompt | self.llm.with_structured_output(Evaluation)
        return chain.invoke({
            "question": question,
            "answer": answer,
            "context": context
        })

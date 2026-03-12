from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class AnswerGeneratorAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research assistant. Answer using ONLY the provided context.

Rules:
1. Include citations: [Source: filename, section X]
2. If context insufficient, state clearly what's missing
3. Be precise and factual
4. Compare/contrast when asked
5. Cite specific sources for each claim
6. Use direct quotes when appropriate

Format:
- Main answer with inline citations
- Separate claims with clear attribution
- Note any limitations or gaps"""),
            ("user", "Question: {question}\n\nContext:\n{context}")
        ])
    
    def generate(self, question: str, context: str) -> str:
        chain = self.prompt | self.llm
        response = chain.invoke({"question": question, "context": context})
        return response.content

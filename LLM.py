from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class LLM:
    def __init__(self):
        template = """
        InnerVoice: You are a real and good conpanion. Keep your responces brief.

        Memory: {context}

        Question: {question}
        """
        model = OllamaLLM(model="llama3")
        prompt = ChatPromptTemplate.from_template(template)
        self.chain = prompt | model


    def Run(self, context, question):
        result = self.chain.invoke({"context": context, "question": question})
        return result
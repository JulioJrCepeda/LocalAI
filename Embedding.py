from langchain_ollama import OllamaEmbeddings

class Embedding:

    def __init__(self):
        self.model = OllamaEmbeddings(model="all-minilm")
  
    def run(self, promptlist):
        result = self.model.embed_documents(promptlist)
        return result
    
    def runSingle(self, prompt):
        result = self.model.embed_query(prompt)
        return result
        
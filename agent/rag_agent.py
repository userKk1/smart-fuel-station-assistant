from RAG.rag_pipeline import RAGPipeline


class RAGAgent:

    def __init__(self):

        self.rag = RAGPipeline()

    def ask(self, question):

        return self.rag.ask(question)
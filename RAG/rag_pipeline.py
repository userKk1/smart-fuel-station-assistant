import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from simulator.LLM.llm_client import generate
from .retriever import Retriever


RAG_PROMPT = """
Tu es un assistant intelligent spécialisé dans la gestion d'un réseau de stations-service.

Tu réponds uniquement à partir du contexte fourni.

Si l'information n'est pas présente dans le contexte, indique clairement que tu ne disposes pas de suffisamment d'informations.

=========================
CONTEXTE
=========================

{context}

=========================
QUESTION
=========================

{question}

=========================
RÉPONSE
=========================
"""


class RAGPipeline:

    def __init__(self):

        self.retriever = Retriever()

    def ask(self, question):

        context = self.retriever.build_context(
            question,
            k=5
        )

        prompt = RAG_PROMPT.format(

            context=context,

            question=question

        )

        answer = generate(prompt)

        return answer


if __name__ == "__main__":

    rag = RAGPipeline()

    print("=" * 60)
    print("Assistant Smart Fuel Station")
    print("Tapez 'exit' pour quitter.")
    print("=" * 60)

    while True:

        question = input("\nQuestion : ")

        if question.lower() in ["exit", "quit"]:

            break

        answer = rag.ask(question)

        print("\nRéponse :\n")

        print(answer)
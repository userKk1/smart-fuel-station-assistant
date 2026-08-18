import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from simulator.LLM.llm_client import generate
from .retriever import Retriever


RAG_PROMPT = """
Tu es PetroSense, un assistant intelligent spécialisé dans la gestion
d'un réseau marocain de stations-service.

Tu dois répondre UNIQUEMENT à partir du contexte fourni.

=========================
CONTEXTE
=========================

{context}

=========================
QUESTION
=========================

{question}

=========================
RÈGLES
=========================

- Réponds en français.
- Réponds directement à la question.
- Sois clair, professionnel et concis.
- N'invente aucune information.
- Ne fais aucune supposition.
- Ne complète pas les informations manquantes avec tes connaissances générales.
- Si l'information demandée n'est pas présente dans le contexte,
  indique clairement que l'information n'est pas disponible.
- Ne prétends pas avoir accès à des informations qui ne sont pas présentes
  dans le contexte.
- Ne commence pas par "Bonjour".
- Ne termine pas par "Cordialement" ou "N'hésitez pas".
- Ne répète pas inutilement la question.

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
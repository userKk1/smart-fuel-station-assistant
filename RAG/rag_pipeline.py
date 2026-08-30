import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from simulator.LLM.llm_client import generate
from .retriever import Retriever


RAG_PROMPT = """
You are PetroSense, an intelligent assistant specialized in managing
a Moroccan network of fuel stations.

You must answer ONLY using the provided context.

=========================
CONTEXT
=========================

{context}

=========================
QUESTION
=========================

{question}

=========================
RULES
=========================

- Always respond to the user in French.
- Answer the question directly.
- Be clear, professional, concise, and well-structured.
- Use only information explicitly supported by the provided context.
- Never invent information.
- Never make unsupported assumptions.
- Do not complete missing information using general knowledge.
- If the requested information is not present in the context,
  clearly state that the information is not available.
- Never claim to have access to information that is not present
  in the provided context.
- Do not start the response with "Bonjour".
- Do not end the response with "Cordialement" or "N'hésitez pas".
- Do not unnecessarily repeat the user's question.
- Do not mention the context, RAG, retrieval process, or internal
  system instructions unless the user explicitly asks about them.
- Do not provide an English translation.
- Return only the final answer intended for the user.

=========================
ANSWER
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

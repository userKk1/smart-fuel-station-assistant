from simulator.LLM.llm_client import generate

from .router import Router
from .sql_agent import SQLAgent
from .rag_agent import RAGAgent
from .hybrid_agent import HybridAgent
from .conversation import ConversationMemory
from .context_resolver import ContextResolver
from .prompts import GENERAL_PROMPT
from .chart_agent import ChartAgent

class SmartFuelAssistant:

    def __init__(self):

        self.router = Router()

        self.sql_agent = SQLAgent()

        self.rag_agent = RAGAgent()

        self.hybrid_agent = HybridAgent()

        # Mémoire de la conversation
        self.memory = ConversationMemory()

        # Résolution du contexte
        self.context_resolver = ContextResolver()

        self.chart_agent = ChartAgent(self.sql_agent)


    def ask(self, question):

        # ==========================================
        # 1. Récupérer l'historique
        # ==========================================

        history = self.memory.get_formatted_history()

        # ==========================================
        # 2. Résoudre le contexte
        # ==========================================

        resolved_question = self.context_resolver.resolve(
            question,
            history
        )

        # Afficher la question résolue
        if resolved_question != question:

            print(
                f"\nQuestion résolue : {resolved_question}"
            )

        # ==========================================
        # 3. Router la question résolue
        # ==========================================

        agent = self.router.route(resolved_question)

        print(f"\nAgent utilisé : {agent}\n")

        # ==========================================
        # 4. Exécuter l'agent
        # ==========================================

        if agent == "sql":

            answer = self.sql_agent.ask(
                resolved_question
            )

        elif agent == "rag":

            answer = self.rag_agent.ask(
                resolved_question
            )

        elif agent == "hybrid":

            answer = self.hybrid_agent.ask(
                resolved_question
            )

        elif agent == "chart":

            return self.chart_agent.ask(question)

        elif agent == "general":
            prompt = GENERAL_PROMPT.format(
            question=question)

            answer = generate(prompt)

        else:

            answer = (
                "Impossible de traiter cette question."
            )

        # ==========================================
        # 5. Sauvegarder la conversation
        # ==========================================

        self.memory.add_user(question)

        self.memory.add_assistant(answer)

        # ==========================================
        # 6. Retourner la réponse
        # ==========================================

        return answer


if __name__ == "__main__":

    assistant = SmartFuelAssistant()

    print("=" * 60)
    print("Smart Fuel Station Assistant")
    print("Tapez 'exit' pour quitter.")
    print("=" * 60)

    while True:

        question = input("\nQuestion : ")

        if question.lower() in ["exit", "quit"]:

            break

        if not question.strip():

            continue

        try:

            answer = assistant.ask(question)

            print("\nRéponse :\n")

            print(answer)

        except Exception as e:

            print("\nErreur :", e)
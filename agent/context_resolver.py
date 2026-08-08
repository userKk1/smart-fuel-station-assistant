from simulator.LLM.llm_client import generate


class ContextResolver:

    def resolve(self, question, history):

        # Première question : aucun contexte nécessaire
        if not history.strip():
            return question

        prompt = f"""
Tu es un module de résolution du contexte conversationnel
d'un assistant intelligent de stations-service.

Ton rôle est de déterminer si la nouvelle question dépend
des échanges précédents.

========================
HISTORIQUE
========================

{history}

========================
NOUVELLE QUESTION
========================

{question}

========================
RÈGLES
========================

1. Si la nouvelle question est complète et compréhensible
   indépendamment de l'historique, retourne-la exactement
   telle quelle.

2. Si elle dépend de l'historique, reformule-la en une
   question complète et autonome.

3. Conserve exactement les informations importantes :
   - noms de stations
   - villes
   - dates
   - nombres
   - types de pannes
   - carburants
   - réclamations
   - autres éléments importants.

4. Ne réponds PAS à la question.

5. N'ajoute aucune information qui n'est pas présente
   dans la question ou dans l'historique.

6.Fais très attention aux pronoms et aux références implicites

7. Retourne UNIQUEMENT la question finale.
"""

        resolved_question = generate(prompt)

        return resolved_question.strip()
from simulator.LLM.llm_client import generate


class Router:

    def route(self, question):

        prompt = f"""
Tu es le routeur d'un assistant intelligent pour un réseau
de stations-service.

Tu dois déterminer quel agent doit traiter la question.

Question :
{question}

Choisis UNE SEULE catégorie parmi :

- general
  Pour les conversations générales ou informelles :
  salutations, remerciements, "comment ça va ?", "qui es-tu ?",
  "que peux-tu faire ?", etc.

- chart
  Pour les questions qui demandent explicitement une
  représentation graphique ou une visualisation des données.

  Exemples :
  - "Montre-moi les transactions en graphique"
  - "Affiche les ventes sous forme de graphique"
  - "Fais-moi un graphe des pannes"
  - "Visualise les transactions par mois"
  - "Je veux voir l'évolution des ventes en graph"
  - "en graph"
  
  IMPORTANT :
  Si l'utilisateur demande explicitement un graphique,
  utilise "chart", même si les données nécessaires
  proviennent de SQL.

- sql
  Pour les questions nécessitant des données structurées
  provenant de la base SQL :
  nombres, comptages, sommes, moyennes, comparaisons,
  statistiques, transactions, ventes, stocks, pannes, etc.

- rag
  Pour les questions nécessitant des informations textuelles
  provenant des documents :
  réclamations, rapports de maintenance, descriptions,
  symptômes, diagnostics, recommandations, etc.

- hybrid
  Pour les questions nécessitant à la fois des données SQL
  et des informations provenant des documents.

Règles :

1. Retourne uniquement une catégorie :
   general
   chart
   sql
   rag
   hybrid

2. Ne donne aucune explication.

3. Une conversation générale et informelle doit être classée
   comme "general".

4. Une demande explicite de graphique ou de visualisation
   doit être classée comme "chart".

5. Une question quantitative ou structurée sans demande
   de graphique doit être classée comme "sql".

6. Une question portant uniquement sur le contenu des
   documents doit être classée comme "rag".

7. Si les données SQL et les documents sont tous les deux
   nécessaires pour répondre à la question, utilise "hybrid".

8. Si la question demande un graphique ET nécessite des
   données SQL, utilise "chart". Le ChartAgent se chargera
   de récupérer les données SQL nécessaires.

Catégorie :
"""

        result = generate(prompt).strip().lower()

        # =================================================
        # Nettoyage de la réponse du LLM
        # =================================================

        # On cherche une catégorie exacte dans la réponse.
        categories = [
            "general",
            "chart",
            "hybrid",
            "sql",
            "rag"
        ]

        for category in categories:

            if result == category:

                return category

        # =================================================
        # Sécurité si le LLM ajoute du texte
        # =================================================

        for category in categories:

            if category in result:

                return category

        # =================================================
        # Route par défaut
        # =================================================

        return "general"
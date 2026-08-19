from simulator.LLM.llm_client import generate


class Router:

    def route(self, question):
        prompt = f"""
Tu es le routeur d'un assistant intelligent pour un réseau
de stations-service.

Question utilisateur :
{question}

Tu dois choisir UNE SEULE catégorie parmi :

- general
- chart
- hybrid

============================================================
GENERAL
============================================================

Utilise "general" uniquement pour les conversations générales
ou informelles qui ne nécessitent aucune donnée de la base
et aucune information documentaire.

Exemples :

- "Bonjour"
- "Salut"
- "Merci"
- "Comment ça va ?"
- "Qui es-tu ?"
- "Que peux-tu faire ?"
- "Comment utiliser cet assistant ?"

============================================================
CHART
============================================================

Utilise "chart" lorsqu'une représentation graphique,
un graphique, une courbe, un histogramme ou une visualisation
est explicitement demandée.

Exemples :

- "Montre-moi les transactions en graphique"
- "Affiche les ventes sous forme de graphique"
- "Fais-moi un graphe des pannes"
- "Visualise les transactions par mois"
- "Montre l'évolution du chiffre d'affaires en graph"
- "Compare les villes en graphique"
- "Je veux un histogramme des ventes"
- "en graph"

IMPORTANT :

Si l'utilisateur demande explicitement un graphique,
classe toujours la question comme "chart".

Le ChartAgent est responsable de récupérer les données
nécessaires et de générer le graphique.

============================================================
HYBRID
============================================================

Utilise "hybrid" pour toutes les autres questions qui
nécessitent des informations provenant de la base de données,
des documents, ou une analyse des données.

Cela inclut notamment :

- statistiques
- comptages
- sommes
- moyennes
- comparaisons
- transactions
- chiffre d'affaires
- litres vendus
- stocks
- pannes
- maintenance
- réclamations
- informations sur les stations
- informations sur les pompes
- prix
- performances
- anomalies
- tendances
- analyses
- interprétations
- causes possibles
- recommandations
- relations entre plusieurs indicateurs

Exemples :

- "Combien avons-nous de stations ?"
- "Combien avons-nous de transactions ?"
- "Quelle ville a le plus de transactions ?"
- "Quelle station a le plus de pannes ?"
- "Quelles stations ont un stock faible ?"
- "Quel est le chiffre d'affaires par ville ?"
- "Pourquoi cette station a-t-elle beaucoup de pannes ?"
- "Analyse les performances des stations."
- "Y a-t-il une relation entre les pannes et l'âge des pompes ?"
- "Quelle station nécessite le plus d'attention ?"
- "Donne-moi des recommandations pour améliorer le réseau."
- "Quelles sont les causes possibles des réclamations ?"

Le HybridAgent décidera ensuite quelles sources utiliser :
SQL, documents RAG, ou les deux.

============================================================
RÈGLES DE PRIORITÉ
============================================================

1. Si la question est une conversation générale sans besoin
   de données → "general".

2. Si la question demande explicitement un graphique,
   une courbe, un histogramme ou une visualisation → "chart".

3. Toutes les autres questions nécessitant des informations
   sur le réseau de stations-service → "hybrid".

4. Ne retourne jamais "sql".

5. Ne retourne jamais "rag".

6. Une question quantitative simple comme :
   "Combien de stations avons-nous ?"
   doit être classée "hybrid".

7. Une question analytique comme :
   "Pourquoi cette station a beaucoup de pannes ?"
   doit être classée "hybrid".

8. Une question demandant un graphique reste "chart",
   même si elle nécessite des données SQL ou des documents.

============================================================
FORMAT DE RÉPONSE
============================================================

Retourne uniquement UNE des trois valeurs suivantes :

general
chart
hybrid

Ne donne aucune explication.

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
            "hybrid"
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
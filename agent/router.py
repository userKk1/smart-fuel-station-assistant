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

- sql
  Pour les questions nécessitant des données structurées
  provenant de la base SQL :
  nombres, comptages, sommes, moyennes, comparaisons,
  statistiques, transactions, ventes, stocks, pannes, etc.

- rag
  Pour les questions nécessitant des informations textuelles
  provenant des documents :
  réclamations, rapports de maintenance, descriptions,
  résumés, symptômes, diagnostics, recommandations, etc.

- hybrid
  Pour les questions nécessitant à la fois des données SQL
  et des informations provenant des documents.

Règles :

1. Retourne uniquement :
   general
   sql
   rag
   ou
   hybrid

2. Ne donne aucune explication.

3. Une question générale et informelle doit être classée
   comme "general".

4. Une question qui demande uniquement des informations
   quantitatives ou structurées doit être classée comme "sql".

5. Une question portant uniquement sur le contenu des
   documents doit être classée comme "rag".

6. Si les données SQL et les documents sont tous les deux
   nécessaires, utilise "hybrid".

Catégorie :
"""

        result = generate(prompt).strip().lower()

        # Nettoyage au cas où le LLM ajoute du texte
        if "general" in result:
            return "general"

        if "hybrid" in result:
            return "hybrid"

        if "sql" in result:
            return "sql"

        if "rag" in result:
            return "rag"

        # Sécurité : route par défaut
        return "general"

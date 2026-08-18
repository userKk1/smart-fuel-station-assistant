import json
import re

import matplotlib.pyplot as plt

from simulator.LLM.llm_client import generate
from .sql_agent import SQLAgent


class ChartAgent:

    def __init__(self, sql_agent=None):

        # On réutilise le SQLAgent existant
        self.sql_agent = sql_agent or SQLAgent()

    # =====================================================
    # Générer le code Python du graphique
    # =====================================================

    def generate_chart_code(
        self,
        question,
        columns,
        rows
    ):

        data = []

        for row in rows:

            data.append(
                dict(zip(columns, row))
            )

        prompt = f"""
Tu es un expert en visualisation de données Python.

Question de l'utilisateur :
{question}

Les données suivantes viennent directement
d'une base SQLite de stations-service.

Colonnes :
{columns}

Données :
{json.dumps(data, ensure_ascii=False, default=str)}

Ta tâche est de générer un graphique adapté
à la question et aux données.

RÈGLES STRICTES :

1. Utilise uniquement matplotlib.pyplot via la variable `plt`.
2. N'écris aucune instruction `import`.
3. N'utilise aucune donnée fictive.
4. Utilise uniquement les données fournies.
5. Ne fais aucune requête SQL.
6. Ne lis aucun fichier.
7. Ne fais aucun appel réseau.
8. Le graphique doit être adapté à la question.
9. Crée obligatoirement une liste appelée `figures`.
10. Si un seul graphique est nécessaire, crée une seule figure
    et ajoute-la à `figures`.
11. Si plusieurs graphiques sont nécessaires, crée une figure
    séparée pour chaque graphique et ajoute chaque figure à `figures`.
12. Utilise `fig, ax = plt.subplots()` pour chaque graphique.
13. N'utilise jamais plusieurs métriques ayant des unités
    ou des échelles différentes sur les mêmes axes.
14. Ne génère aucune explication.
15. Retourne uniquement le code Python.
16. N'utilise PAS `plt.show()`.
17. N'utilise pas de bloc Markdown.
18. Les résultats SQL sont disponibles dans la variable `data`.
19. Utilise obligatoirement `data` pour accéder aux résultats.



Exemple de structure :

figures = []

fig, ax = plt.subplots(figsize=(4, 4))

# graphique

ax.set_title("...")
ax.set_xlabel("...")
ax.set_ylabel("...")

plt.tight_layout()

figures.append(fig)


Code Python :
"""

        code = generate(prompt)

        return self.clean_code(code)

    # =====================================================
    # Nettoyer la réponse du LLM
    # =====================================================

    def clean_code(self, code):

        code = code.strip()

        code = re.sub(
            r"```python",
            "",
            code,
            flags=re.IGNORECASE
        )

        code = re.sub(
            r"```",
            "",
            code
        )

        return code.strip()

    # =====================================================
    # Exécuter le code du graphique
    # =====================================================

    def execute_chart_code(
        self,
        code,
        columns,
        rows
    ):

        data = []

        for row in rows:

            data.append(
                dict(zip(columns, row))
            )

        # Sécurité basique :
        # le code généré ne doit pas pouvoir importer
        # des modules ou accéder au système.

        forbidden = [
            "import ",
            "__import__",
            "open(",
            "exec(",
            "eval(",
            "os.",
            "sys.",
            "subprocess",
            "socket",
            "requests",
        ]

        for item in forbidden:

            if item in code:

                raise ValueError(
                    f"Code Python refusé : élément interdit '{item}'"
                )

        local_vars = {

            "plt": plt,

            "data": data,

            "columns": columns,

            "rows": rows
        }

        safe_builtins = {
        "len": len,
        "range": range,
        "enumerate": enumerate,
        "min": min,
        "max": max,
        "sum": sum,
        "abs": abs,
        "round": round
        }

        exec(
            code,
        {
            "__builtins__": safe_builtins
        },
        local_vars
        )

        figures = local_vars.get("figures")

        if not figures:

            raise ValueError(
                "Le code généré n'a créé aucune figure."
            )

        return figures

    # =====================================================
    # Pipeline complet
    # =====================================================

    def ask(self, question):

        print("\n[ChartAgent] Recherche des données...\n")

        # -------------------------------------------------
        # 1. SQL
        # -------------------------------------------------

        result = self.sql_agent.get_data(question)

        sql = result["sql"]
        columns = result["columns"]
        rows = result["rows"]

        print("\nSQL générée :\n")
        print(sql)

        # -------------------------------------------------
        # 2. Vérifier les résultats
        # -------------------------------------------------

        if not rows:

            return {
                "type": "text",
                "content": (
                    "Aucune donnée n'a été trouvée "
                    "pour générer ce graphique."
                )
            }

        # -------------------------------------------------
        # 3. Générer le code Python
        # -------------------------------------------------

        print("\n[ChartAgent] Génération du graphique...\n")

        code = self.generate_chart_code(
            question,
            columns,
            rows
        )

        print("\nCode Python généré :\n")
        print(code)

        # -------------------------------------------------
        # 4. Exécuter le graphique
        # -------------------------------------------------

        figures = self.execute_chart_code(
            code,
            columns,
            rows
        )

        # -------------------------------------------------
        # 5. Retourner le résultat
        # -------------------------------------------------

        return {
            "type": "chart",
            "figures": figures,
            "sql": sql,
            "columns": columns,
            "rows": rows,
            "code": code
        }
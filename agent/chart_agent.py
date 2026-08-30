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
You are a Python data visualization expert.

User question:
{question}

The following data comes directly from a SQLite database
containing information about a network of fuel stations.

Columns:
{columns}

Data:
{json.dumps(data, ensure_ascii=False, default=str)}

Your task is to generate an appropriate chart based on
the user's question and the provided data.

STRICT RULES:

1. Use only matplotlib.pyplot through the `plt` variable.
2. Do not write any import statement.
3. Do not use fictitious or invented data.
4. Use only the data provided.
5. Do not execute any SQL query.
6. Do not read any file.
7. Do not make any network request.
8. The chart must be appropriate for the user's question.
9. You must create a list called `figures`.
10. If only one chart is required, create one figure
    and add it to `figures`.
11. If multiple charts are required, create a separate figure
    for each chart and add each figure to `figures`.
12. Use `fig, ax = plt.subplots()` for every chart.
13. Never place multiple metrics with different units
    or incompatible scales on the same axes.
14. Do not generate any explanation.
15. Return only Python code.
16. Do not use `plt.show()`.
17. Do not use Markdown code blocks.
18. The SQL results are available in the `data` variable.
19. You must use `data` to access the SQL results.

LANGUAGE RULE:

20. All chart titles, axis labels, legends, annotations,
    and other user-visible text inside the chart must be written
    in French.
21. The chart must be clear and professional for a French-speaking
    user.
22. Do not translate database column names unless necessary
    for user-visible chart labels.

Example structure:

figures = []

fig, ax = plt.subplots(figsize=(4, 4))

# chart

ax.set_title("...")
ax.set_xlabel("...")
ax.set_ylabel("...")

plt.tight_layout()

figures.append(fig)


Python code:
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

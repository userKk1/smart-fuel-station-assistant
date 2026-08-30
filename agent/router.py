from simulator.LLM.llm_client import generate


class Router:

    def route(self, question):
        prompt = f"""
You are the router for an intelligent assistant designed for a
service station network.

User question:
{question}

You must choose EXACTLY ONE category from:

- general
- chart
- hybrid

============================================================
GENERAL
=======

Use "general" only for general or informal conversations
that do not require any database data
or any documentary information.

Examples:

- "Hello"
- "Hi"
- "Thank you"
- "How are you?"
- "Who are you?"
- "What can you do?"
- "How do I use this assistant?"

============================================================
CHART
=====

Use "chart" when a graphical representation,
chart, graph, curve, histogram, or visualization
is explicitly requested.

Examples:

- "Show me the transactions as a chart"
- "Display the sales as a graph"
- "Create a graph of the breakdowns"
- "Visualize the transactions by month"
- "Show the evolution of revenue as a graph"
- "Compare the cities in a chart"
- "I want a histogram of the sales"
- "as a graph"

IMPORTANT:

If the user explicitly requests a chart or graph,
always classify the question as "chart".

The ChartAgent is responsible for retrieving the necessary
data and generating the chart.

============================================================
HYBRID
======

Use "hybrid" for all other questions that
require information from the database,
documents, or data analysis.

This includes, in particular:

- statistics
- counts
- sums
- averages
- comparisons
- transactions
- revenue
- liters sold
- inventory
- breakdowns
- maintenance
- complaints
- station information
- pump information
- prices
- performance
- anomalies
- trends
- analyses
- interpretations
- possible causes
- recommendations
- relationships between multiple indicators

Examples:

- "How many stations do we have?"
- "How many transactions do we have?"
- "Which city has the most transactions?"
- "Which station has the most breakdowns?"
- "Which stations have low inventory?"
- "What is the revenue by city?"
- "Why does this station have so many breakdowns?"
- "Analyze the performance of the stations."
- "Is there a relationship between breakdowns and pump age?"
- "Which station requires the most attention?"
- "Give me recommendations to improve the network."
- "What are the possible causes of the complaints?"

The HybridAgent will then decide which sources to use:
SQL, RAG documents, or both.

============================================================
PRIORITY RULES
============================================================

1. If the question is a general conversation that does not require
   data → "general".

2. If the question explicitly requests a chart,
   graph, histogram, or visualization → "chart".

3. All other questions requiring information
   about the service station network → "hybrid".

4. Never return "sql".

5. Never return "rag".

6. A simple quantitative question such as:
   "How many stations do we have?"
   must be classified as "hybrid".

7. An analytical question such as:
   "Why does this station have so many breakdowns?"
   must be classified as "hybrid".

8. A question requesting a chart remains "chart",
   even if it requires SQL data or documents.

============================================================
RESPONSE FORMAT
============================================================

Return ONLY ONE of the following three values:

general
chart
hybrid

Do not provide any explanation.

Category:
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

from simulator.LLM.llm_client import generate

from .sql_agent import SQLAgent
from .rag_agent import RAGAgent
from .prompts import HYBRID_PROMPT


class HybridAgent:

    def __init__(self):

        self.sql = SQLAgent()

        self.rag = RAGAgent()

    def ask(self, question):

        # ---------- SQL ----------

        sql_data = self.sql.get_data(question)

        sql_result = f"""
Requête SQL :

{sql_data['sql']}

Colonnes :

{sql_data['columns']}

Résultat :

{sql_data['rows']}
"""

        # ---------- RAG ----------

        context = self.rag.rag.retriever.build_context(

            question,

            k=5

        )

        # ---------- Fusion ----------

        prompt = HYBRID_PROMPT.format(

            question=question,

            sql_result=sql_result,

            context=context

        )

        answer = generate(prompt)

        return answer
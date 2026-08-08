import sqlite3

from simulator.LLM.llm_client import generate
from .prompts import SQL_PROMPT, SQL_ANSWER_PROMPT


class SQLAgent:

    def __init__(self, database_path="database/station.db"):

        self.connection = sqlite3.connect(database_path)

    # =====================================================
    # Lire automatiquement le schéma de la base
    # =====================================================

    def get_schema(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)

        tables = [row[0] for row in cursor.fetchall()]

        schema = ""

        for table in tables:

            schema += f"\nTable : {table}\n"

            cursor.execute(f"PRAGMA table_info({table})")

            columns = cursor.fetchall()

            for column in columns:

                schema += (
                    f"- {column[1]} ({column[2]})\n"
                )

        return schema

    # =====================================================
    # Générer une requête SQL
    # =====================================================

    def generate_sql(self, question):

        schema = self.get_schema()

        prompt = SQL_PROMPT.format(

            schema=schema,

            question=question

        )

        sql = generate(prompt)

        return sql.strip()

    # =====================================================
    # Exécuter la requête
    # =====================================================

    def execute_sql(self, sql):

        cursor = self.connection.cursor()

        cursor.execute(sql)

        rows = cursor.fetchall()

        columns = []

        if cursor.description:

            columns = [

                column[0]

                for column in cursor.description

            ]

        return columns, rows

    # =====================================================
    # Transformer le résultat SQL en réponse naturelle
    # =====================================================

    def generate_answer(

        self,

        question,

        sql,

        columns,

        rows

    ):

        prompt = SQL_ANSWER_PROMPT.format(

            question=question,

            sql=sql,

            columns=columns,

            rows=rows

        )

        answer = generate(prompt)

        return answer

    # =====================================================

    def get_data(self, question):
        sql = self.generate_sql(question)

        print("\nSQL générée :\n")
        print(sql)

        columns, rows = self.execute_sql(sql)

        return {
            "sql": sql,
            "columns": columns,
            "rows": rows
        }

    # =====================================================
    # Pipeline complet
    # =====================================================

    def ask(self, question):

        sql = self.generate_sql(question)

        print("\nSQL générée :\n")

        print(sql)

        columns, rows = self.execute_sql(sql)

        answer = self.generate_answer(

            question,

            sql,

            columns,

            rows

        )

        return answer

    # =====================================================

    def close(self):

        self.connection.close()


if __name__ == "__main__":

    agent = SQLAgent()

    while True:

        question = input("\nQuestion : ")

        if question.lower() == "exit":

            break

        try:

            answer = agent.ask(question)

            print("\nRéponse :\n")

            print(answer)

        except Exception as e:

            print("\nErreur :", e)

    agent.close()
import sqlite3

from simulator.LLM.llm_client import generate
from .prompts import SQL_PROMPT, SQL_ANSWER_PROMPT


class SQLAgent:

    def __init__(self, database_path="database/station.db"):

        self.connection = sqlite3.connect(database_path, check_same_thread=False)

        # Lire le schéma une seule fois
        self.schema = self.get_schema()

        # Construire un profil léger des données
        self.data_profile = self.get_data_profile()

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
    # Profil des données
    # =====================================================

    def get_data_profile(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)

        tables = [row[0] for row in cursor.fetchall()]

        profile = ""

        for table in tables:

            profile += f"\nTable : {table}\n"

            # ---------------------------------------------
            # Colonnes
            # ---------------------------------------------

            cursor.execute(f"PRAGMA table_info({table})")

            columns = cursor.fetchall()

            column_names = [
                column[1]
                for column in columns
            ]

            # ---------------------------------------------
            # 5 lignes d'exemple
            # ---------------------------------------------

            cursor.execute(
                f"SELECT * FROM {table} LIMIT 5"
            )

            rows = cursor.fetchall()

            if rows:

                profile += "\nExemples de données :\n"

                for row in rows:

                    values = []

                    for name, value in zip(
                        column_names,
                        row
                    ):

                        values.append(
                            f"{name}={value}"
                        )

                    profile += (
                        "- "
                        + ", ".join(values)
                        + "\n"
                    )

            else:

                profile += "\nAucune donnée.\n"

        return profile

    # =====================================================
    # Générer une requête SQL
    # =====================================================

    def generate_sql(self, question):

        schema = self.get_schema()

        prompt = SQL_PROMPT.format(

            schema=self.schema,

            data_profile=self.data_profile,

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
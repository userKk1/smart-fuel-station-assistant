from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

MODEL = "gemini-2.5-flash"

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate(prompt: str) -> str:
    """
    Génère une réponse à partir d'un prompt.
    """

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:

        print(f"Erreur Gemini : {e}")

        return ""
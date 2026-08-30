from simulator.LLM.llm_client import generate


class ContextResolver:

    def resolve(self, question, history):

        # Première question : aucun contexte nécessaire
        if not history.strip():
            return question

        prompt = f"""
You are a conversational context resolution module
for an intelligent fuel station assistant.

Your role is to determine whether the new question depends
on previous conversation exchanges.

========================
CONVERSATION HISTORY
========================

{history}

========================
NEW QUESTION
========================

{question}

========================
RULES
========================

1. If the new question is complete and understandable
   independently of the conversation history, return it exactly
   as provided.

2. If the new question depends on the conversation history,
   rewrite it as a complete and self-contained question.

3. Preserve exactly all important information, including:
   - station names
   - cities
   - dates
   - numbers
   - failure types
   - fuel types
   - complaints
   - and any other relevant elements.

4. Do NOT answer the question.

5. Do NOT add any information that is not present
   in the question or the conversation history.

6. Pay close attention to pronouns and implicit references,
   such as:
   - "elle"
   - "il"
   - "cette station"
   - "ce carburant"
   - "la précédente"
   - "celle-ci"
   - "combien"
   - "pourquoi"
   - and similar references.

7. Resolve ambiguous references using the conversation history
   whenever the intended reference is clearly identifiable.

8. If a reference cannot be resolved reliably from the history,
   do not invent an interpretation. Preserve the question
   without adding unsupported information.

9. Return ONLY the final question.

Final question:
"""

        resolved_question = generate(prompt)

        return resolved_question.strip()

class ConversationMemory:

    def __init__(self, max_messages=10):

        self.messages = []

        self.max_messages = max_messages

    def add_user(self, message):

        self.messages.append({
            "role": "user",
            "content": message
        })

        self._limit_history()

    def add_assistant(self, message):

        self.messages.append({
            "role": "assistant",
            "content": message
        })

        self._limit_history()

    def get_history(self):

        return self.messages

    def get_formatted_history(self):

        if not self.messages:
            return ""

        history = []

        for message in self.messages:

            role = (
                "Utilisateur"
                if message["role"] == "user"
                else "Assistant"
            )

            history.append(
                f"{role} : {message['content']}"
            )

        return "\n\n".join(history)

    def clear(self):

        self.messages = []

    def _limit_history(self):

        max_items = self.max_messages * 2

        if len(self.messages) > max_items:

            self.messages = self.messages[-max_items:]
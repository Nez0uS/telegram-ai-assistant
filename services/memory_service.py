class MemoryService:

    MAX_HISTORY = 20

    def __init__(self):
        self.history: dict[int, list[dict[str, str]]] = {}

    def add_message(self, user_id: int, role: str, content: str) -> None:
        message = {"role": role, "content": content}
        if user_id not in self.history:
            self.history[user_id] = []
        self.history[user_id].append(message)
        if len(self.history[user_id]) > self.MAX_HISTORY:
            self.history[user_id] = self.history[user_id][-self.MAX_HISTORY:]

    def get_messages(self, user_id: int) -> list[dict[str, str]]:
        return self.history.get(user_id, [])

    def clear_history(self, user_id: int) -> None:
        if user_id in self.history:
            del self.history[user_id]


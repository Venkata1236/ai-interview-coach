from langchain_community.chat_message_histories import ChatMessageHistory


class ConversationMemory:
    """
    Memory class using langchain_community ChatMessageHistory.
    Compatible with langchain==1.2.x
    """
    def __init__(self):
        self.chat_history = ChatMessageHistory()
        self.human_prefix = "Candidate"
        self.ai_prefix = "AI Coach"

    def load_memory_variables(self, inputs):
        messages = self.chat_history.messages
        if not messages:
            return {"history": ""}

        history_text = ""
        for message in messages:
            if message.type == "human":
                history_text += f"\n{self.human_prefix}: {message.content}"
            else:
                history_text += f"\n{self.ai_prefix}: {message.content}\n"

        return {"history": history_text}

    def save_context(self, inputs, outputs):
        human_input = inputs.get("input", "")
        ai_output = outputs.get("output", "")
        self.chat_history.add_user_message(human_input)
        self.chat_history.add_ai_message(ai_output)

    def clear(self):
        self.chat_history.clear()


def get_memory():
    return ConversationMemory()


def get_memory_summary(memory):
    result = memory.load_memory_variables({})
    return result.get("history", "No history yet.")


def clear_memory(memory):
    memory.clear()
    return memory


def add_to_memory(memory, human_input, ai_response):
    memory.save_context(
        {"input": human_input},
        {"output": ai_response}
    )
    return memory
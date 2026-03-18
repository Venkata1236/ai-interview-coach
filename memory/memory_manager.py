from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory

def get_memory():
    return ConversationBufferMemory(
        memory_key="history",
        human_prefix="Candidate",
        ai_prefix="AI Coach",
        return_messages=False
    )


def get_memory_summary(memory):
    return memory.load_memory_variables({}).get("history", "No history yet.")


def clear_memory(memory):
    memory.clear()
    return memory


def add_to_memory(memory, human_input, ai_response):
    memory.save_context(
        {"input": human_input},
        {"output": ai_response}
    )
    return memory
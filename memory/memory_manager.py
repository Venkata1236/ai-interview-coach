from langchain.memory import ConversationBufferMemory


def get_memory():
    """
    Creates and returns a ConversationBufferMemory instance.
    
    - memory_key="history" → matches {history} in our prompt template
    - human_prefix and ai_prefix → makes conversation history readable
    - return_messages=False → returns history as plain text not message objects
      (needed for PromptTemplate — ChatPromptTemplate would need True)
    """
    memory = ConversationBufferMemory(
        memory_key="history",
        human_prefix="Candidate",
        ai_prefix="AI Coach",
        return_messages=False
    )
    return memory


def get_memory_summary(memory):
    """
    Returns the current conversation history stored in memory.
    Useful for debugging or displaying chat history.
    """
    return memory.load_memory_variables({}).get("history", "No history yet.")


def clear_memory(memory):
    """
    Clears all conversation history from memory.
    Used when starting a new session.
    """
    memory.clear()
    return memory


def add_to_memory(memory, human_input, ai_response):
    """
    Manually adds a turn to memory.
    Useful for CLI mode where we manage memory manually.
    """
    memory.save_context(
        {"input": human_input},
        {"output": ai_response}
    )
    return memory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from memory.memory_manager import get_memory
from prompts.interview_prompt import get_interview_prompt
import os
from dotenv import load_dotenv

load_dotenv()


def get_interview_chain(
    candidate_name,
    target_role,
    experience_level,
    company_type,
    resume_text,
    job_description
):
    """
    Creates and returns a ConversationChain with:
    - OpenAI GPT as the LLM
    - ConversationBufferMemory for history
    - Interview coach prompt with candidate context
    """

    # --- Load LLM ---
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",       # cost effective + powerful enough
        temperature=0.7,                 # balanced — not too robotic, not too random
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # --- Load Memory ---
    memory = get_memory()

    # --- Load Base Prompt ---
    base_prompt = get_interview_prompt()

    # --- Fill in static variables (candidate profile + resume + JD) ---
    # These don't change turn by turn — only history and human_input change
    filled_prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=base_prompt.template.format(
            candidate_name=candidate_name,
            target_role=target_role,
            experience_level=experience_level,
            company_type=company_type,
            resume_text=resume_text,
            job_description=job_description,
            history="{history}",
            human_input="{human_input}"
        )
    )

    # --- Build ConversationChain ---
    chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=filled_prompt,
        input_key="human_input",
        output_key="response",
        verbose=False
    )

    return chain, memory


def run_chain(chain, user_input):
    """
    Runs one turn of the conversation chain.
    Returns the AI coach's response as a string.
    """
    try:
        response = chain.invoke({"human_input": user_input})
        return response["response"], None
    except Exception as e:
        return None, f"⚠️ Error getting response: {str(e)}"


def is_session_complete(memory, total_questions=5):
    """
    Checks if the interview session is complete
    by counting how many questions have been asked.
    Uses memory history to count AI Coach turns.
    """
    from memory.memory_manager import get_memory_summary
    history = get_memory_summary(memory)

    if not history:
        return False

    # Count number of times AI Coach responded
    ai_turns = history.count("AI Coach:")

    # Session complete after total_questions + follow ups + onboarding
    # Approximate check — prompt handles exact session end
    return ai_turns >= (total_questions * 2) + 2
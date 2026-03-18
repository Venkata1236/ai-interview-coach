import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from memory.memory_manager import get_memory
from prompts.interview_prompt import get_interview_prompt
from dotenv import load_dotenv

load_dotenv()


def get_api_key():
    """
    Works both locally (.env) and on Streamlit Cloud (st.secrets)
    """
    try:
        import streamlit as st
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY")


def get_interview_chain(
    candidate_name,
    target_role,
    experience_level,
    company_type,
    resume_text,
    job_description
):
    """
    Creates the LLM and memory.
    Returns chain_data dict and memory object.
    """
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=get_api_key()
    )

    memory = get_memory()

    # Store static profile — filled once
    chain_data = {
        "llm": llm,
        "memory": memory,
        "candidate_name": candidate_name,
        "target_role": target_role,
        "experience_level": experience_level,
        "company_type": company_type,
        "resume_text": resume_text,
        "job_description": job_description,
        "prompt_template": get_interview_prompt()
    }

    return chain_data, memory


def run_chain(chain_data, user_input):
    """
    Runs one turn manually:
    1. Load memory history
    2. Fill prompt with all variables
    3. Call LLM
    4. Save turn to memory
    5. Return response
    """
    try:
        llm = chain_data["llm"]
        memory = chain_data["memory"]
        prompt_template = chain_data["prompt_template"]

        # --- Load current memory history ---
        memory_vars = memory.load_memory_variables({})
        history = memory_vars.get("history", "")

        # --- Fill full prompt ---
        filled_prompt = prompt_template.format(
            candidate_name=chain_data["candidate_name"],
            target_role=chain_data["target_role"],
            experience_level=chain_data["experience_level"],
            company_type=chain_data["company_type"],
            resume_text=chain_data["resume_text"],
            job_description=chain_data["job_description"],
            history=history,
            human_input=user_input
        )

        # --- Call LLM ---
        response = llm.invoke([HumanMessage(content=filled_prompt)])
        ai_response = response.content

        # --- Save to memory ---
        memory.save_context(
            {"input": user_input},
            {"output": ai_response}
        )

        return ai_response, None

    except Exception as e:
        return None, f"⚠️ Error getting response: {str(e)}"
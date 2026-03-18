import streamlit as st


def initialize_session():
    """
    Initializes all Streamlit session state variables.
    Called once when the app loads.
    """
    # --- Onboarding state ---
    if "onboarding_complete" not in st.session_state:
        st.session_state.onboarding_complete = False

    # --- Candidate profile ---
    if "candidate_name" not in st.session_state:
        st.session_state.candidate_name = ""

    if "target_role" not in st.session_state:
        st.session_state.target_role = ""

    if "experience_level" not in st.session_state:
        st.session_state.experience_level = ""

    if "company_type" not in st.session_state:
        st.session_state.company_type = ""

    # --- Resume and JD ---
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = ""

    if "job_description" not in st.session_state:
        st.session_state.job_description = ""

    # --- Chain and memory ---
    if "chain" not in st.session_state:
        st.session_state.chain = None

    if "memory" not in st.session_state:
        st.session_state.memory = None

    # --- Chat history for display ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- Session state ---
    if "session_complete" not in st.session_state:
        st.session_state.session_complete = False

    # --- Question counter ---
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0

    # --- Total questions setting ---
    if "total_questions" not in st.session_state:
        st.session_state.total_questions = 5
        
    # ADD this at the bottom of initialize_session()
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False


def save_candidate_profile(
    candidate_name,
    target_role,
    experience_level,
    company_type,
    resume_text,
    job_description
):
    """
    Saves candidate profile to session state
    after onboarding form is submitted.
    """
    st.session_state.candidate_name = candidate_name
    st.session_state.target_role = target_role
    st.session_state.experience_level = experience_level
    st.session_state.company_type = company_type
    st.session_state.resume_text = resume_text
    st.session_state.job_description = job_description
    st.session_state.onboarding_complete = True


def save_chain_to_session(chain, memory):
    """
    Saves the ConversationChain and memory
    to session state so they persist across reruns.
    """
    st.session_state.chain = chain
    st.session_state.memory = memory


def add_message_to_history(role, message):
    """
    Adds a message to chat history for display.
    - role: "user" or "assistant"
    - message: the text content
    """
    st.session_state.chat_history.append({
        "role": role,
        "message": message
    })


def reset_session():
    """
    Completely resets all session state.
    Called when user clicks Start New Session.
    """
    keys_to_clear = [
        "onboarding_complete",
        "candidate_name",
        "target_role",
        "experience_level",
        "company_type",
        "resume_text",
        "job_description",
        "chain",
        "memory",
        "chat_history",
        "session_complete",
        "question_count",
        "total_questions",
        "interview_started"
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def is_session_ready():
    """
    Checks if chain and memory are initialized
    and ready to accept messages.
    """
    return (
        st.session_state.chain is not None and
        st.session_state.memory is not None and
        st.session_state.onboarding_complete
    )


def increment_question_count():
    """
    Increments question counter by 1.
    Called after each AI response.
    """
    st.session_state.question_count += 1


def is_interview_complete():
    """
    Returns True if all questions have been asked.
    """
    return st.session_state.question_count >= st.session_state.total_questions
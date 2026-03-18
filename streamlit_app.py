import streamlit as st
import os
from dotenv import load_dotenv
from chains.interview_chain import get_interview_chain, run_chain
from utils.resume_parser import extract_text_from_resume
from utils.session_helper import (
    initialize_session,
    save_candidate_profile,
    save_chain_to_session,
    add_message_to_history,
    reset_session,
    is_session_ready,
    increment_question_count,
    is_interview_complete
)

load_dotenv()


# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="centered"
)


# ─────────────────────────────────────────
# INITIALIZE SESSION
# ─────────────────────────────────────────
initialize_session()


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.title("🎯 AI Interview Coach")
    st.markdown("---")

    # --- Session Info ---
    if st.session_state.onboarding_complete:
        st.markdown("### 👤 Candidate")
        st.write(f"**Name:** {st.session_state.candidate_name}")
        st.write(f"**Role:** {st.session_state.target_role}")
        st.write(f"**Level:** {st.session_state.experience_level}")
        st.write(f"**Company:** {st.session_state.company_type}")
        st.markdown("---")

        # --- Progress ---
        st.markdown("### 📊 Session Progress")
        progress = min(
            st.session_state.question_count / st.session_state.total_questions,
            1.0
        )
        st.progress(progress)
        st.write(
            f"Questions: {st.session_state.question_count}"
            f" / {st.session_state.total_questions}"
        )
        st.markdown("---")

    # --- Settings ---
    st.markdown("### ⚙️ Settings")
    total_q = st.slider(
        "Number of Questions",
        min_value=3,
        max_value=10,
        value=5,
        step=1
    )
    st.session_state.total_questions = total_q
    st.markdown("---")

    # --- New Session Button ---
    if st.button("🔄 Start New Session", use_container_width=True):
        reset_session()
        st.rerun()

    # --- About ---
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption(
        "AI Interview Coach uses LangChain "
        "ConversationBufferMemory to remember "
        "your answers across the entire session "
        "and give personalized feedback."
    )


# ─────────────────────────────────────────
# MAIN AREA — ONBOARDING
# ─────────────────────────────────────────
if not st.session_state.onboarding_complete:

    st.title("🎯 AI Interview Coach")
    st.markdown(
        "Practice your interviews with an AI coach that "
        "**remembers your answers**, gives structured feedback, "
        "and personalizes questions based on your resume and the job description."
    )
    st.markdown("---")

    st.subheader("📋 Let's set up your session")

    with st.form("onboarding_form"):

        # --- Basic Info ---
        col1, col2 = st.columns(2)

        with col1:
            candidate_name = st.text_input(
                "Your Name *",
                placeholder="e.g. Rahul Sharma"
            )

        with col2:
            target_role = st.text_input(
                "Target Role *",
                placeholder="e.g. Data Scientist"
            )

        col3, col4 = st.columns(2)

        with col3:
            experience_level = st.selectbox(
                "Experience Level *",
                options=["Fresher (0-1 years)", "Mid Level (2-5 years)", "Senior (5+ years)"]
            )

        with col4:
            company_type = st.selectbox(
                "Target Company Type *",
                options=["Startup", "MNC (Large Corporation)", "Product Based", "Service Based"]
            )

        st.markdown("---")

        # --- Resume Upload ---
        st.markdown("#### 📄 Resume Upload")
        st.caption("📎 Supported formats: PDF or Word (.docx) only")
        uploaded_resume = st.file_uploader(
            "Upload your Resume *",
            type=["pdf", "docx"],
            help="Only PDF or Word (.docx) files are supported"
        )

        st.markdown("---")

        # --- Job Description ---
        st.markdown("#### 📝 Job Description")
        job_description = st.text_area(
            "Paste the Job Description *",
            placeholder="Paste the full job description here...",
            height=200
        )

        st.markdown("---")

        # --- Submit ---
        submitted = st.form_submit_button(
            "🚀 Start Interview Session",
            use_container_width=True
        )

        if submitted:
            # --- Validate inputs ---
            errors = []

            if not candidate_name.strip():
                errors.append("Name is required.")

            if not target_role.strip():
                errors.append("Target Role is required.")

            if not uploaded_resume:
                errors.append("Please upload your resume (PDF or .docx).")

            if not job_description.strip():
                errors.append("Job Description is required.")

            if errors:
                for err in errors:
                    st.error(f"⚠️ {err}")

            else:
                # --- Parse Resume ---
                with st.spinner("📄 Reading your resume..."):
                    resume_text, parse_error = extract_text_from_resume(uploaded_resume)

                if parse_error:
                    st.error(parse_error)

                else:
                    # --- Initialize Chain ---
                    with st.spinner("🚀 Setting up your interview session..."):
                        chain, memory = get_interview_chain(
                            candidate_name=candidate_name.strip(),
                            target_role=target_role.strip(),
                            experience_level=experience_level,
                            company_type=company_type,
                            resume_text=resume_text,
                            job_description=job_description.strip()
                        )

                    # --- Save to session ---
                    save_candidate_profile(
                        candidate_name=candidate_name.strip(),
                        target_role=target_role.strip(),
                        experience_level=experience_level,
                        company_type=company_type,
                        resume_text=resume_text,
                        job_description=job_description.strip()
                    )
                    save_chain_to_session(chain, memory)

                    # --- Get opening message from coach ---
                    with st.spinner("🤖 Coach is preparing your session..."):
                        opening_response, error = run_chain(
                            chain,
                            "Hello, I am ready to start my interview practice."
                        )

                    if error:
                        st.error(error)
                    else:
                        add_message_to_history("assistant", opening_response)
                        st.rerun()


# ─────────────────────────────────────────
# MAIN AREA — CHAT INTERFACE
# ─────────────────────────────────────────

else:

    st.title(f"🎯 Interview Session — {st.session_state.target_role}")
    st.caption(
        f"Hi {st.session_state.candidate_name}! "
        "Your coach remembers everything you say in this session."
    )
    st.markdown("---")

    # --- Display Chat History ---
    for message in st.session_state.chat_history:
        if message["role"] == "assistant":
            # Hide [FEEDBACK COMPLETE] marker from display
            display_message = message["message"].replace(
                "[FEEDBACK COMPLETE] Type 'next' or click Next Question when you are ready to continue.",
                ""
            ).replace(
                "[SESSION ENDED]",
                ""
            ).strip()
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(display_message)
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(message["message"])

    # --- Ready Button (only shown before interview starts) ---
    if (
        is_session_ready() and
        not st.session_state.get("interview_started", False)
    ):
        st.info("👆 Your coach is ready! Click the button below to begin.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Yes, I'm Ready — Start Interview!", use_container_width=True):
                st.session_state.interview_started = True
                with st.spinner("🤖 Coach is preparing your first question..."):
                    response, error = run_chain(
                        st.session_state.chain,
                        "Yes I am ready. Please ask me the first interview question now."
                    )
                if error:
                    st.error(error)
                else:
                    add_message_to_history("assistant", response)
                    if "Question" in response and "?" in response:
                        increment_question_count()
                    st.rerun()

    # --- Interview is active ---
    elif is_session_ready() and st.session_state.get("interview_started", False):

        last_message = (
            st.session_state.chat_history[-1]["message"]
            if st.session_state.chat_history else ""
        )

        # --- Show session complete only AFTER last answer is evaluated ---
        # Complete = question_count >= total AND last message has FEEDBACK COMPLETE
        session_truly_complete = (
            st.session_state.question_count >= st.session_state.total_questions and
            "[FEEDBACK COMPLETE]" in last_message
        )

        if session_truly_complete:
            # --- Session Complete ---
            st.success(
                "🎉 Interview session complete! "
                "Click below to get your full session report."
            )
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📊 Get My Session Summary", use_container_width=True):
                    with st.spinner("🤖 Coach is preparing your report..."):
                        response, error = run_chain(
                            st.session_state.chain,
                            "Give me my full session summary with scores and action items."
                        )
                    if error:
                        st.error(error)
                    else:
                        add_message_to_history("assistant", response)
                        st.rerun()

        elif "[FEEDBACK COMPLETE]" in last_message:
            # --- Feedback given, waiting for next question ---
            st.info("📝 Take your time to read the feedback above.")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("➡️ Next Question", use_container_width=True):
                    with st.spinner("🤖 Coach is preparing next question..."):
                        response, error = run_chain(
                            st.session_state.chain,
                            "next"
                        )
                    if error:
                        st.error(error)
                    else:
                        add_message_to_history("assistant", response)
                        if "Question" in response and "?" in response:
                            increment_question_count()
                        st.rerun()

        else:
    # --- Check if session has fully ended ---
            last_message = (
                st.session_state.chat_history[-1]["message"]
                if st.session_state.chat_history else ""
            )

            if "[SESSION ENDED]" in last_message:
                # Clean ending — no more input
                st.balloons()
                st.success(
                    "✅ Session complete! "
                    "Click 'Start New Session' in the sidebar to practice again."
                )
            else:
                # --- Normal chat input for answering questions ---
                user_input = st.chat_input("Type your answer here...")

                if user_input:
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(user_input)
                    add_message_to_history("user", user_input)

                    with st.chat_message("assistant", avatar="🤖"):
                        with st.spinner("🤖 Coach is thinking..."):
                            response, error = run_chain(
                                st.session_state.chain,
                                user_input
                            )
                        if error:
                            st.error(error)
                        else:
                            display_response = response.replace(
                                "[FEEDBACK COMPLETE] Type 'next' or click Next Question when you are ready to continue.",
                                ""
                            ).strip()
                            st.markdown(display_response)
                            add_message_to_history("assistant", response)
                            if "Question" in response and "?" in response:
                                increment_question_count()
                            st.rerun()
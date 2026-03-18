import os
import sys
from dotenv import load_dotenv
from chains.interview_chain import get_interview_chain, run_chain
from memory.memory_manager import clear_memory, add_to_memory
from utils.resume_parser import extract_text_from_resume

load_dotenv()


def print_separator():
    print("\n" + "=" * 60 + "\n")


def print_welcome():
    print_separator()
    print("🎯  AI INTERVIEW COACH — CLI MODE")
    print("    Powered by LangChain + OpenAI GPT")
    print_separator()
    print("Commands you can use anytime:")
    print("  'quit'    → Exit the session")
    print("  'reset'   → Start a new session")
    print("  'history' → View conversation history")
    print_separator()


def get_candidate_profile():
    """
    Collects candidate profile from terminal input.
    """
    print("📋  CANDIDATE PROFILE SETUP\n")

    # --- Name ---
    candidate_name = input("Your Name: ").strip()
    while not candidate_name:
        print("⚠️  Name cannot be empty.")
        candidate_name = input("Your Name: ").strip()

    # --- Target Role ---
    target_role = input("Target Role (e.g. Data Scientist, Backend Engineer): ").strip()
    while not target_role:
        print("⚠️  Role cannot be empty.")
        target_role = input("Target Role: ").strip()

    # --- Experience Level ---
    print("\nExperience Level:")
    print("  1. Fresher (0-1 years)")
    print("  2. Mid Level (2-5 years)")
    print("  3. Senior (5+ years)")
    exp_choice = input("Choose (1/2/3): ").strip()
    experience_map = {
        "1": "Fresher",
        "2": "Mid Level",
        "3": "Senior"
    }
    experience_level = experience_map.get(exp_choice, "Fresher")

    # --- Company Type ---
    print("\nTarget Company Type:")
    print("  1. Startup")
    print("  2. MNC (Large Corporation)")
    print("  3. Product Based")
    print("  4. Service Based")
    comp_choice = input("Choose (1/2/3/4): ").strip()
    company_map = {
        "1": "Startup",
        "2": "MNC",
        "3": "Product Based",
        "4": "Service Based"
    }
    company_type = company_map.get(comp_choice, "Startup")

    return candidate_name, target_role, experience_level, company_type


def get_resume_text():
    """
    Asks user for resume file path in CLI mode.
    """
    print_separator()
    print("📄  RESUME UPLOAD\n")
    print("Supported formats: PDF or Word (.docx) only\n")

    while True:
        file_path = input("Enter full path to your resume file (or press Enter to skip): ").strip()

        if not file_path:
            print("⚠️  Skipping resume — coach will work with role info only.\n")
            return "No resume provided."

        if not os.path.exists(file_path):
            print("⚠️  File not found. Please check the path and try again.")
            continue

        resume_text, error = extract_text_from_resume(file_path)

        if error:
            print(error)
            retry = input("Try another file? (yes/no): ").strip().lower()
            if retry != "yes":
                return "No resume provided."
            continue

        print("✅  Resume loaded successfully!\n")
        return resume_text


def get_job_description():
    """
    Asks user to paste the job description in CLI mode.
    """
    print_separator()
    print("📝  JOB DESCRIPTION\n")
    print("Paste the Job Description below.")
    print("When done, type 'END' on a new line and press Enter.\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    jd_text = "\n".join(lines).strip()

    if not jd_text:
        print("⚠️  No JD provided — coach will work with role info only.\n")
        return "No job description provided."

    print("✅  Job Description saved!\n")
    return jd_text


def run_cli():
    """
    Main CLI loop — runs the interview session in terminal.
    """
    print_welcome()

    # --- Check API Key ---
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not found in .env file.")
        print("    Please add your API key and try again.")
        sys.exit(1)

    # --- Collect Profile ---
    candidate_name, target_role, experience_level, company_type = get_candidate_profile()

    # --- Collect Resume ---
    resume_text = get_resume_text()

    # --- Collect JD ---
    job_description = get_job_description()

    # --- Initialize Chain ---
    print_separator()
    print("🚀  Starting your interview session...\n")

    chain, memory = get_interview_chain(
        candidate_name=candidate_name,
        target_role=target_role,
        experience_level=experience_level,
        company_type=company_type,
        resume_text=resume_text,
        job_description=job_description
    )

    # --- Kick off session with greeting ---
    opening_response, error = run_chain(chain, "Hello, I am ready to start.")
    if error:
        print(error)
        sys.exit(1)

    print(f"🤖  AI Coach:\n{opening_response}\n")

    # --- Main Chat Loop ---
    while True:
        print_separator()
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # --- Handle commands ---
        if user_input.lower() == "quit":
            print("\n👋  Thank you for practicing! Good luck with your interview!\n")
            break

        elif user_input.lower() == "reset":
            print("\n🔄  Resetting session...\n")
            clear_memory(memory)
            run_cli()
            break

        elif user_input.lower() == "history":
            from memory.memory_manager import get_memory_summary
            print("\n📜  CONVERSATION HISTORY:\n")
            print(get_memory_summary(memory))
            continue

        # --- Get AI Response ---
        response, error = run_chain(chain, user_input)

        if error:
            print(f"\n{error}\n")
            continue

        print(f"\n🤖  AI Coach:\n{response}\n")


if __name__ == "__main__":
    run_cli()
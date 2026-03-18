# 🎯 AI Interview Coach

> Upload your Resume + Paste JD — get personalized interview questions, structured feedback, and session summary powered by LangChain Conversational Memory

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Memory](https://img.shields.io/badge/Memory-ConversationBufferMemory-purple)

---

## 📌 What Is This?

An AI-powered Interview Coach that remembers everything you say across the session. Upload your resume, paste the job description, and practice with personalized questions tailored to your background and the role. Get structured feedback after every answer using the STAR format.

---

## 🗺️ Simple Flow
```
Upload Resume (PDF/DOCX) + Paste Job Description
              ↓
resume_parser.py  → extract text from resume
              ↓
interview_prompt.py → inject resume + JD + history into prompt
              ↓
ConversationBufferMemory → stores every question and answer
              ↓
Coach asks one question at a time
              ↓
You answer → Coach gives structured feedback
(STAR check + metrics check + pattern tracking)
              ↓
Next Question button → repeat until all questions done
              ↓
Session Summary → scores + strengths + gaps + action items
```

---

## 🏗️ Detailed Architecture
```
User
 ├── streamlit_app.py   → Web UI (upload + chat + summary)
 └── app.py             → Terminal interface (CLI mode)
          │
          ▼
      chains/
      └── interview_chain.py   → ConversationChain (LLM + Memory + Prompt)
          │
          ▼
      prompts/
      └── interview_prompt.py  → PromptTemplate with Resume + JD + History
          │
          ▼
      memory/
      └── memory_manager.py    → ConversationBufferMemory setup
          │
          ▼
      utils/
      ├── resume_parser.py     → PDF/DOCX text extraction
      └── session_helper.py    → Streamlit session_state management
          │
          ▼
      OpenAI API → gpt-4o-mini

.env              → API key (local)
Streamlit Secrets → API key (cloud)
requirements.txt  → all libraries
```

---

## 📁 Project Structure
```
ai-interview-coach/
├── app.py                      ← Terminal version (CLI)
├── streamlit_app.py            ← Web UI (deploy this)
├── chains/
│   └── interview_chain.py      ← ConversationChain with memory
├── memory/
│   └── memory_manager.py       ← ConversationBufferMemory
├── prompts/
│   └── interview_prompt.py     ← Coach persona + rules + STAR checker
├── utils/
│   ├── resume_parser.py        ← PDF and DOCX text extraction
│   └── session_helper.py       ← Streamlit session state helpers
├── .env                        ← API key (never push!)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧠 Key Concepts

| Concept | What It Does |
|---|---|
| **ConversationBufferMemory** | Stores full conversation history — injected into every prompt turn |
| **PromptTemplate** | Defines coach persona, STAR checker, feedback format, session rules |
| **Resume Parser** | Extracts text from PDF or DOCX resume uploaded by user |
| **JD Injection** | Job description injected into prompt — questions tailored to role requirements |
| **STAR Format Checker** | Coach checks every answer for Situation, Task, Action, Result |
| **Pattern Tracking** | Memory allows coach to spot repeated examples or missing metrics across turns |
| **Session Summary** | Full report with scores, strengths, gaps, and action items generated from memory |

---

## 🔑 Why ConversationBufferMemory

| Feature | Without Memory | With ConversationBufferMemory |
|---|---|---|
| Question context | Isolated per turn | Full history every turn |
| Pattern tracking | Not possible | Spots repeated examples |
| Personalized feedback | Generic | Based on your actual answers |
| Follow-up questions | Random | Based on what you said |
| Session summary | Not possible | Full report from memory |

---

## ⚙️ Local Setup

**Step 1 — Clone the repo:**
```bash
git clone https://github.com/YOUR_USERNAME/ai-interview-coach.git
cd ai-interview-coach
```

**Step 2 — Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 3 — Add your OpenAI API key in `.env`:**
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**Step 4 — Run:**

Streamlit UI:
```bash
python -m streamlit run streamlit_app.py
```

Terminal version:
```bash
python app.py
```

---

## 💬 How To Use

**Streamlit UI:**
1. Fill in your Name, Target Role, Experience Level, Company Type
2. Upload your Resume (PDF or DOCX only)
3. Paste the Job Description
4. Click **Start Interview Session**
5. Click **Yes I'm Ready** to begin
6. Answer each question in the chat box
7. Read feedback — click **Next Question** when ready
8. After all questions — click **Get My Session Summary**

**Terminal:**
1. Enter your profile details when prompted
2. Provide resume file path
3. Paste job description — type `END` when done
4. Answer questions as they appear
5. Type `quit` to exit, `history` to see conversation

---

## 📦 Tech Stack

- **LangChain** — ConversationChain, ConversationBufferMemory, PromptTemplate
- **OpenAI** — GPT-4o-mini for coaching responses
- **Streamlit** — Web UI with sidebar, chat interface, progress tracking
- **PyPDF2** — PDF resume text extraction
- **python-docx** — DOCX resume text extraction
- **python-dotenv** — API key management for local development

---

## ☁️ Streamlit Cloud Deployment

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file to `streamlit_app.py`
5. Go to **Settings → Secrets** and add:
```toml
OPENAI_API_KEY = "your-actual-key-here"
```
6. Click Deploy

---

## 👤 Author

**Venkata Reddy Bommavaram**
- 📧 bommavaramvenkat2003@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/venkatareddy1203)
- 🐙 [GitHub](https://github.com/venkata1236)
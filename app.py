import streamlit as st
import json
from groq import Groq
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

st.set_page_config(
    page_title="SkillMatch",
    page_icon="○",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
    color: #1a1a2e;
}

.stApp { background: #f7f5ff; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none !important; }

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 6rem !important;
    max-width: 680px !important;
    margin: 0 auto !important;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 1.5rem 1rem 2rem;
}
.hero-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #ede9ff;
    color: #5b3fc8;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.3rem 0.85rem;
    border-radius: 99px;
    border: 1px solid #d8d0ff;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #13102b;
    line-height: 1.25;
    margin-bottom: 0.6rem;
    letter-spacing: -0.02em;
}
.hero h1 em {
    font-style: italic;
    font-weight: 600;
    color: #6148d5;
}
.hero-sub {
    font-size: 0.88rem;
    color: #6e6b8a;
    line-height: 1.6;
    max-width: 420px;
    margin: 0 auto;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 0.3rem 0 !important;
    border: none !important;
    box-shadow: none !important;
    align-items: flex-start !important;
}

[data-testid="stChatMessageAvatarAssistant"] {
    background: #ede9ff !important;
    border-radius: 50% !important;
    width: 32px !important;
    height: 32px !important;
    flex-shrink: 0 !important;
}
[data-testid="stChatMessageAvatarUser"] {
    background: #6148d5 !important;
    border-radius: 50% !important;
    width: 32px !important;
    height: 32px !important;
    flex-shrink: 0 !important;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown {
    background: #ffffff;
    border: 1px solid #e8e3ff;
    border-radius: 4px 16px 16px 16px;
    padding: 0.75rem 1rem;
    font-size: 0.88rem;
    color: #1a1a2e;
    line-height: 1.6;
    box-shadow: 0 1px 4px rgba(97,72,213,0.06);
    max-width: 100%;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown p {
    color: #1a1a2e !important;
    margin: 0;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown {
    background: linear-gradient(135deg, #6148d5, #7c5ce8);
    border-radius: 16px 4px 16px 16px;
    padding: 0.75rem 1rem;
    font-size: 0.88rem;
    color: #ffffff !important;
    line-height: 1.6;
    box-shadow: 0 2px 12px rgba(97,72,213,0.25);
    max-width: 100%;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown p {
    color: #ffffff !important;
    margin: 0;
}

/* ── Skill result card ── */
.skill-card-wrap {
    background: #ffffff;
    border: 1px solid #e8e3ff;
    border-radius: 16px;
    padding: 1.1rem 1.2rem;
    box-shadow: 0 2px 16px rgba(97,72,213,0.07);
}
.skill-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.9rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid #f0ecff;
}
.skill-card-title {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #6148d5;
}
.skill-card-count {
    font-size: 0.68rem;
    font-weight: 600;
    color: #6148d5;
    background: #f0ecff;
    padding: 0.15rem 0.6rem;
    border-radius: 99px;
}
.skill-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0.6rem;
    border-radius: 10px;
    margin-bottom: 0.35rem;
    background: #faf8ff;
    transition: background 0.15s;
}
.skill-item:hover { background: #f0ecff; }
.skill-num {
    font-size: 0.68rem;
    font-weight: 700;
    color: #c4b8f0;
    width: 18px;
    text-align: center;
    flex-shrink: 0;
}
.skill-label {
    font-size: 0.85rem;
    font-weight: 500;
    color: #13102b;
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.skill-track {
    width: 90px;
    height: 5px;
    background: #ede9ff;
    border-radius: 99px;
    flex-shrink: 0;
    overflow: hidden;
}
.skill-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #6148d5, #9b7ef8);
}
.skill-pct {
    font-size: 0.75rem;
    font-weight: 700;
    color: #6148d5;
    width: 32px;
    text-align: right;
    flex-shrink: 0;
}
.skill-card-footer {
    margin-top: 0.8rem;
    padding-top: 0.65rem;
    border-top: 1px solid #f0ecff;
    font-size: 0.65rem;
    color: #aaa7c4;
    text-align: center;
    line-height: 1.5;
}

/* ── Typing indicator ── */
.typing-box {
    background: #ffffff;
    border: 1px solid #e8e3ff;
    border-radius: 4px 16px 16px 16px;
    padding: 0.75rem 1rem;
    display: inline-flex;
    flex-direction: column;
    gap: 0.25rem;
    box-shadow: 0 1px 4px rgba(97,72,213,0.06);
}
.typing-label {
    font-size: 0.82rem;
    font-weight: 500;
    color: #1a1a2e;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.typing-dots {
    display: inline-flex;
    gap: 3px;
    align-items: center;
}
.typing-dots span {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #9b7ef8;
    display: inline-block;
    animation: bounce 1.2s infinite ease-in-out;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40% { transform: translateY(-4px); opacity: 1; }
}
.typing-sub {
    font-size: 0.7rem;
    color: #9b96ba;
}

/* ── Chat input — TRANSPARAN ── */
.stBottom, [data-testid="stBottom"] {
    background: transparent !important;
    backdrop-filter: none !important;
    box-shadow: none !important;
}
.stBottom > *, [data-testid="stBottom"] > * {
    background: transparent !important;
}
[data-testid="stChatInputContainer"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.5rem 0 !important;
}
[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1.5px solid #d4cdf5 !important;
    border-radius: 14px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    color: #1a1a2e !important;
    box-shadow: 0 2px 12px rgba(97,72,213,0.08) !important;
    padding: 0.7rem 1rem !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #6148d5 !important;
    box-shadow: 0 0 0 3px rgba(97,72,213,0.12), 0 2px 12px rgba(97,72,213,0.08) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d4cdf5; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ── System prompt ──────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are an AI that ONLY extracts skills from job descriptions. "
    "If the input is NOT a job description, respond with an empty JSON array: []\n"
    "Output MUST be a pure JSON array only, no markdown, no backticks, no explanation.\n"
    'Format: [{"skill": "Skill Name", "confidence": 85}, ...]\n'
    "- confidence: integer 1-100.\n"
    "- Extract max 12 most relevant skills.\n"
    "- Skill names in English."
)

# ── Language helpers ───────────────────────────────────────────
def detect_lang(text):
    try:
        lg = detect(text)
        if lg in ('id', 'in'): return 'id'
        if lg == 'en': return 'en'
        return lg
    except LangDetectException:
        return 'en'

TEXTS = {
    'greeting': {
        'id': 'Halo! Tempel deskripsi pekerjaan atau tanyakan skill yang dibutuhkan untuk posisi tertentu.',
        'en': 'Hello! Paste a job description or ask what skills are needed for a position.',
    },
    'error_notjob': {
        'id': 'Maaf, chatbot ini hanya untuk menganalisis deskripsi pekerjaan. Silakan tempel lowongan kerja yang ingin kamu analisis.',
        'en': 'Sorry, this chatbot is designed for job descriptions only. Please paste a job listing you want to analyze.',
    },
    'analyzing': {
        'id': ('Menganalisis deskripsi pekerjaan...', 'Membaca dan mengekstrak skill yang relevan.'),
        'en': ('Analyzing job description...', 'Reading and extracting relevant skills.'),
    },
    'footer': {
        'id': 'Persentase menunjukkan seberapa relevan skill tersebut berdasarkan deskripsi pekerjaan yang diberikan.',
        'en': 'Confidence score shows how relevant each skill is based on the provided job description.',
    },
}

def t(key, lang):
    return TEXTS[key].get(lang, TEXTS[key]['en'])

# ── Groq API ───────────────────────────────────────────────────
def extract_skills(text):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return {"error": "GROQ_API_KEY tidak ditemukan. Tambahkan ke Streamlit Secrets."}
    try:
        client = Groq(api_key=api_key)
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": "Job description:\n\n" + text}
            ],
            temperature=0.1,
        )
        raw = res.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        data = json.loads(raw)
        if not isinstance(data, list):
            return []
        return [
            {"skill": str(s["skill"]), "confidence": round(float(s["confidence"]), 1)}
            for s in data if "skill" in s and "confidence" in s
        ]
    except json.JSONDecodeError:
        return {"error": "Model mengembalikan format tidak valid. Coba lagi."}
    except Exception as e:
        return {"error": str(e)}

# ── Render skill cards ─────────────────────────────────────────
def render_skills(skills, lang='en'):
    if not skills:
        return '<p style="font-size:0.85rem;color:#9b96ba;">Tidak ada skill yang terdeteksi.</p>'
    sorted_s = sorted(skills, key=lambda x: x["confidence"], reverse=True)
    rows = ""
    for i, s in enumerate(sorted_s, 1):
        pct = int(s["confidence"])
        rows += (
            f'<div class="skill-item">'
            f'<span class="skill-num">{i}</span>'
            f'<span class="skill-label">{s["skill"]}</span>'
            f'<div class="skill-track"><div class="skill-fill" style="width:{pct}%"></div></div>'
            f'<span class="skill-pct">{pct}%</span>'
            f'</div>'
        )
    footer_text = t('footer', lang)
    return (
        f'<div class="skill-card-wrap">'
        f'<div class="skill-card-header">'
        f'<span class="skill-card-title">Skill yang dibutuhkan</span>'
        f'<span class="skill-card-count">{len(skills)} skill</span>'
        f'</div>'
        f'{rows}'
        f'<div class="skill-card-footer">{footer_text}</div>'
        f'</div>'
    )

# ── Hero ───────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-chip">Career Intelligence</div>
    <h1>Find the skills you <em>actually</em> need</h1>
    <p class="hero-sub">Paste any job description and we will extract the must-have skills so you can focus on what matters.</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": t('greeting', 'en'),
        "type": "text"
    }]
if "user_lang" not in st.session_state:
    st.session_state.user_lang = "en"

# ── Render history ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "skills":
            st.markdown(render_skills(msg["skills"], msg.get("lang", "en")), unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

# ── Input ──────────────────────────────────────────────────────
if prompt := st.chat_input("Paste job description or ask for required skills..."):
    lang = detect_lang(prompt)
    st.session_state.user_lang = lang

    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        main_txt, sub_txt = t('analyzing', lang)
        placeholder = st.empty()
        placeholder.markdown(
            f'<div class="typing-box">'
            f'<div class="typing-label">'
            f'<div class="typing-dots"><span></span><span></span><span></span></div>'
            f'{main_txt}'
            f'</div>'
            f'<div class="typing-sub">{sub_txt}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        result = extract_skills(prompt)
        placeholder.empty()

        if isinstance(result, dict) and "error" in result:
            msg_text = f"Terjadi masalah: {result['error']}"
            st.markdown(msg_text)
            st.session_state.messages.append({"role": "assistant", "content": msg_text, "type": "text"})
        elif not result:
            msg_text = t('error_notjob', lang)
            st.markdown(msg_text)
            st.session_state.messages.append({"role": "assistant", "content": msg_text, "type": "text"})
        else:
            st.markdown(render_skills(result, lang), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "skills": result, "lang": lang, "type": "skills"})

    # Update greeting sesuai bahasa user pertama kali
    if len(st.session_state.messages) == 2:
        st.session_state.messages[0]["content"] = t('greeting', lang)
        st.rerun()

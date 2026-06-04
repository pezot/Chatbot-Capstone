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
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
    color: #1a1a2e;
}

.stApp { background: #f5f3ff; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none !important; }

.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 6rem !important;
    max-width: 660px !important;
    margin: 0 auto !important;
}

/* ── Hero ─────────────────────────────── */
.hero {
    text-align: center;
    padding: 1rem 1.5rem 2.5rem;
}
.hero-chip {
    display: inline-block;
    background: transparent;
    color: #7c6bb5;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.28rem 0.9rem;
    border-radius: 99px;
    border: 1px solid #ccc5ef;
    margin-bottom: 1.4rem;
}
.hero-title {
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 2.6rem;
    font-weight: 400;
    color: #13102b;
    line-height: 1.15;
    margin-bottom: 0.85rem;
    letter-spacing: -0.01em;
}
.hero-title em {
    font-style: italic;
    color: #5b3fc8;
}
.hero-sub {
    font-size: 0.875rem;
    color: #7a7898;
    line-height: 1.65;
    max-width: 400px;
    margin: 0 auto;
    font-weight: 400;
}

/* ── Chat messages ─────────────────────── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 0.25rem 0 !important;
    border: none !important;
    box-shadow: none !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: #ebe6ff !important;
    border-radius: 50% !important;
    width: 30px !important;
    height: 30px !important;
    flex-shrink: 0 !important;
}
[data-testid="stChatMessageAvatarUser"] {
    background: #5b3fc8 !important;
    border-radius: 50% !important;
    width: 30px !important;
    height: 30px !important;
    flex-shrink: 0 !important;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown {
    background: #ffffff;
    border: 1px solid #e4deff;
    border-radius: 4px 14px 14px 14px;
    padding: 0.7rem 0.95rem;
    font-size: 0.875rem;
    color: #1a1a2e !important;
    line-height: 1.65;
    box-shadow: 0 1px 6px rgba(91,63,200,0.07);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown p {
    color: #1a1a2e !important;
    margin: 0;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown {
    background: linear-gradient(135deg, #5b3fc8 0%, #7c5ce8 100%);
    border-radius: 14px 4px 14px 14px;
    padding: 0.7rem 0.95rem;
    font-size: 0.875rem;
    color: #ffffff !important;
    line-height: 1.65;
    box-shadow: 0 2px 14px rgba(91,63,200,0.22);
    max-width: 85%;
    word-break: break-word;
    white-space: pre-wrap;
    overflow-wrap: break-word;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown p {
    color: #ffffff !important;
    margin: 0;
    word-break: break-word;
    white-space: pre-wrap;
}

/* ── Skill card ────────────────────────── */
.sc-wrap {
    background: #ffffff;
    border: 1px solid #e4deff;
    border-radius: 16px;
    padding: 1.1rem 1.15rem 0.9rem;
    box-shadow: 0 2px 18px rgba(91,63,200,0.07);
}
.sc-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 0.75rem;
    margin-bottom: 0.6rem;
    border-bottom: 1px solid #f0ecff;
}
.sc-title {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #5b3fc8;
}
.sc-badge {
    font-size: 0.65rem;
    font-weight: 600;
    color: #5b3fc8;
    background: #ede9ff;
    padding: 0.18rem 0.6rem;
    border-radius: 99px;
}
.sc-row {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.45rem 0.55rem;
    border-radius: 10px;
    margin-bottom: 0.3rem;
    background: #faf8ff;
}
.sc-row:hover { background: #f0ecff; }
.sc-num {
    font-size: 0.65rem;
    font-weight: 700;
    color: #c4b5f5;
    width: 16px;
    text-align: center;
    flex-shrink: 0;
}
.sc-name {
    font-size: 0.84rem;
    font-weight: 500;
    color: #13102b;
    flex: 1;
    min-width: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.sc-track {
    width: 80px;
    height: 4px;
    background: #ebe6ff;
    border-radius: 99px;
    flex-shrink: 0;
    overflow: hidden;
}
.sc-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #5b3fc8, #9b7ef8);
}
.sc-pct {
    font-size: 0.72rem;
    font-weight: 700;
    color: #5b3fc8;
    width: 34px;
    text-align: right;
    flex-shrink: 0;
}
.sc-foot {
    margin-top: 0.75rem;
    padding-top: 0.6rem;
    border-top: 1px solid #f0ecff;
    font-size: 0.62rem;
    color: #b0adca;
    text-align: center;
    line-height: 1.5;
}

/* ── Typing indicator ──────────────────── */
.typing-box {
    background: #ffffff;
    border: 1px solid #e4deff;
    border-radius: 4px 14px 14px 14px;
    padding: 0.65rem 0.9rem;
    display: inline-flex;
    flex-direction: column;
    gap: 0.2rem;
    box-shadow: 0 1px 6px rgba(91,63,200,0.07);
}
.typing-row {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.82rem;
    font-weight: 500;
    color: #1a1a2e;
}
.dots span {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #9b7ef8;
    display: inline-block;
    animation: tdot 1.2s infinite ease-in-out;
}
.dots span:nth-child(2) { animation-delay: .2s; }
.dots span:nth-child(3) { animation-delay: .4s; }
@keyframes tdot {
    0%,80%,100% { transform:translateY(0); opacity:.4; }
    40%         { transform:translateY(-4px); opacity:1; }
}
.typing-sub { font-size: 0.68rem; color: #a09cc0; }

/* ── Input — fully transparent bg ─────── */
.stBottom, [data-testid="stBottom"],
.stBottom > *, [data-testid="stBottom"] > *,
.stBottom > * > *, [data-testid="stBottom"] > * > * {
    background: transparent !important;
    backdrop-filter: none !important;
    box-shadow: none !important;
    border: none !important;
}
[data-testid="stChatInputContainer"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.4rem 0 !important;
}
[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1.5px solid #cfc8f5 !important;
    border-radius: 14px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    color: #1a1a2e !important;
    box-shadow: 0 2px 14px rgba(91,63,200,0.08) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #5b3fc8 !important;
    box-shadow: 0 0 0 3px rgba(91,63,200,0.11), 0 2px 14px rgba(91,63,200,0.08) !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cfc8f5; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ── Prompts ────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are SkillMatch, an AI that ONLY extracts required skills from job descriptions or job-related queries.

STRICT RULES:
1. You ONLY respond to inputs that are:
   - Job descriptions / vacancy postings
   - Questions about what skills are needed for a specific job/role/position
   Examples of VALID inputs:
     - "What skills do I need to become a data scientist?"
     - "We are looking for a backend engineer with 3 years experience..."
     - "Skills needed for a UI/UX designer role"

2. You MUST return [] (empty array) for ANY input that is NOT job-related. This includes:
   - Code snippets or programming questions ("write a for loop", "how to use pandas")
   - General knowledge questions ("what is machine learning", "explain SQL")
   - Random text, gibberish, or off-topic content
   - Requests to do tasks unrelated to job skill analysis

3. Output MUST be a pure JSON array only. No markdown, no backticks, no explanation.
   Format: [{"skill": "Skill Name", "confidence": 85}, ...]
   - confidence: integer 1-100 (how important this skill is for the role)
   - Max 12 skills, sorted by relevance
   - Skill names in English"""

# ── Language helpers ───────────────────────────────────────────
def detect_lang(text):
    try:
        lg = detect(text)
        if lg in ('id', 'in'): return 'id'
        return 'en'
    except LangDetectException:
        return 'en'

TEXTS = {
    'greeting': {
        'id': 'Halo! Tempel deskripsi pekerjaan atau tanyakan skill apa yang dibutuhkan untuk posisi tertentu.',
        'en': 'Hello! Paste a job description or ask what skills are needed for a specific role.',
    },
    'not_job': {
        'id': 'Maaf, saya hanya bisa membantu menganalisis deskripsi pekerjaan atau menjawab pertanyaan seputar skill yang dibutuhkan untuk suatu posisi. Silakan tempel lowongan kerja atau tanyakan tentang posisi tertentu.',
        'en': 'Sorry, I can only help analyze job descriptions or answer questions about skills needed for specific roles. Please paste a job listing or ask about a particular position.',
    },
    'analyzing': {
        'id': ('Menganalisis...', 'Membaca dan mengekstrak skill yang relevan.'),
        'en': ('Analyzing...', 'Reading and extracting relevant skills.'),
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
                {"role": "user",   "content": text}
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
        return {"error": "Format tidak valid. Coba lagi."}
    except Exception as e:
        return {"error": str(e)}

# ── Render skill cards ─────────────────────────────────────────
def render_skills(skills, lang='en'):
    if not skills:
        return '<p style="font-size:0.85rem;color:#a09cc0;padding:0.5rem 0;">Tidak ada skill yang terdeteksi.</p>'
    rows = ""
    for i, s in enumerate(sorted(skills, key=lambda x: x["confidence"], reverse=True), 1):
        pct = int(s["confidence"])
        rows += (
            f'<div class="sc-row">'
            f'<span class="sc-num">{i}</span>'
            f'<span class="sc-name">{s["skill"]}</span>'
            f'<div class="sc-track"><div class="sc-fill" style="width:{pct}%"></div></div>'
            f'<span class="sc-pct">{pct}%</span>'
            f'</div>'
        )
    return (
        f'<div class="sc-wrap">'
        f'<div class="sc-head">'
        f'<span class="sc-title">Skill yang dibutuhkan</span>'
        f'<span class="sc-badge">{len(skills)} skill</span>'
        f'</div>'
        f'{rows}'
        f'<div class="sc-foot">{t("footer", lang)}</div>'
        f'</div>'
    )

# ── Hero ───────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-chip">Career Intelligence</div>
    <div class="hero-title">Find the skills you<br><em>actually</em> need</div>
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

# ── Render history ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "skills":
            st.markdown(render_skills(msg["skills"], msg.get("lang", "en")), unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

# ── Input ──────────────────────────────────────────────────────
if prompt := st.chat_input("Paste a job description or ask about a role..."):
    lang = detect_lang(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        main_txt, sub_txt = t('analyzing', lang)
        ph = st.empty()
        ph.markdown(
            f'<div class="typing-box">'
            f'<div class="typing-row"><div class="dots"><span></span><span></span><span></span></div>{main_txt}</div>'
            f'<div class="typing-sub">{sub_txt}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        result = extract_skills(prompt)
        ph.empty()

        if isinstance(result, dict) and "error" in result:
            msg_out = f"Terjadi masalah: {result['error']}"
            st.markdown(msg_out)
            st.session_state.messages.append({"role": "assistant", "content": msg_out, "type": "text"})
        elif not result:
            msg_out = t('not_job', lang)
            st.markdown(msg_out)
            st.session_state.messages.append({"role": "assistant", "content": msg_out, "type": "text"})
        else:
            st.markdown(render_skills(result, lang), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "skills": result, "lang": lang, "type": "skills"})

    if len(st.session_state.messages) == 2:
        st.session_state.messages[0]["content"] = t('greeting', lang)
        st.rerun()

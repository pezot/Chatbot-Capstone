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

# ── Init theme state ───────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ── Theme variables ────────────────────────────────────────────
if st.session_state.dark_mode:
    theme = {
        "app_bg":           "#0f0d1a",
        "text_primary":     "#e8e4ff",
        "text_secondary":   "#9b96c8",
        "text_muted":       "#5a567a",
        "accent":           "#8b6ef5",
        "accent_soft":      "#2a1f4a",
        "accent_border":    "#3d3068",
        "hero_title":       "#f0ecff",
        "hero_em":          "#a78bfa",
        "chip_color":       "#9b7ef8",
        "chip_border":      "#3d3068",
        "bubble_bg":        "#1a1530",
        "bubble_border":    "#2e2650",
        "bubble_text":      "#ccc5ef",
        "user_bubble_from": "#6d4ff0",
        "user_bubble_to":   "#8b6ef5",
        "card_bg":          "#1a1530",
        "card_border":      "#2e2650",
        "card_item_bg":     "#120f24",
        "card_item_border": "#2a2050",
        "card_item_hover":  "#221a3d",
        "card_item_hborder":"#5b3fc8",
        "card_title":       "#9b7ef8",
        "card_badge_bg":    "#2a1f4a",
        "card_badge_text":  "#9b7ef8",
        "card_divider":     "#1e1840",
        "card_foot":        "#4a4568",
        "name_color":       "#e0d8ff",
        "input_bg":         "#1a1530",
        "input_border":     "#3d3068",
        "input_text":       "#e8e4ff",
        "scroll_thumb":     "#3d3068",
        "toggle_bg":        "#2a1f4a",
        "toggle_border":    "#5b3fc8",
        "toggle_icon":      "🌙",
        "toggle_label":     "Dark",
    }
else:
    theme = {
        "app_bg":           "#f5f3ff",
        "text_primary":     "#1a1a2e",
        "text_secondary":   "#8580a8",
        "text_muted":       "#b0adca",
        "accent":           "#5b3fc8",
        "accent_soft":      "#ebe6ff",
        "accent_border":    "#ccc5ef",
        "hero_title":       "#13102b",
        "hero_em":          "#5b3fc8",
        "chip_color":       "#7c6bb5",
        "chip_border":      "#ccc5ef",
        "bubble_bg":        "#ffffff",
        "bubble_border":    "#e4deff",
        "bubble_text":      "#3a3660",
        "user_bubble_from": "#5b3fc8",
        "user_bubble_to":   "#7c5ce8",
        "card_bg":          "#ffffff",
        "card_border":      "#e4deff",
        "card_item_bg":     "#faf8ff",
        "card_item_border": "#ede9ff",
        "card_item_hover":  "#f0ecff",
        "card_item_hborder":"#c4b5f5",
        "card_title":       "#5b3fc8",
        "card_badge_bg":    "#ede9ff",
        "card_badge_text":  "#5b3fc8",
        "card_divider":     "#f0ecff",
        "card_foot":        "#b0adca",
        "name_color":       "#13102b",
        "input_bg":         "#ffffff",
        "input_border":     "#cfc8f5",
        "input_text":       "#1a1a2e",
        "scroll_thumb":     "#cfc8f5",
        "toggle_bg":        "#ede9ff",
        "toggle_border":    "#ccc5ef",
        "toggle_icon":      "☀️",
        "toggle_label":     "Light",
    }

T = theme  # shorthand

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, sans-serif;
    color: {T["text_primary"]};
}}

.stApp {{ background: {T["app_bg"]}; }}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stSidebar"] {{ display: none !important; }}

.block-container {{
    padding-top: 2.5rem !important;
    padding-bottom: 6rem !important;
    max-width: 680px !important;
    margin: 0 auto !important;
}}

/* ── Theme Toggle Button ───────────────── */
.theme-toggle-wrap {{
    display: flex;
    justify-content: flex-end;
    margin-bottom: 0.5rem;
    padding-right: 0.5rem;
}}

/* ── Hero ─────────────────────────────── */
.hero {{
    text-align: center;
    padding: 0.5rem 2rem 2.5rem;
}}
.hero-chip {{
    display: inline-block;
    background: transparent;
    color: {T["chip_color"]};
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.28rem 0.9rem;
    border-radius: 99px;
    border: 1px solid {T["chip_border"]};
    margin-bottom: 1.4rem;
}}
.hero-title {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 2.6rem;
    font-weight: 400;
    color: {T["hero_title"]};
    line-height: 1.15;
    margin-bottom: 1rem;
    letter-spacing: -0.01em;
}}
.hero-title em {{
    font-style: italic;
    color: {T["hero_em"]};
}}
.hero-sub {{
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
    font-weight: 400;
    color: {T["text_secondary"]};
    line-height: 1.7;
    max-width: 560px;
    margin: 0 auto;
    letter-spacing: 0.01em;
    padding: 0 1rem;
}}

/* ── Chat messages ─────────────────────── */
[data-testid="stChatMessage"] {{
    background: transparent !important;
    padding: 0.25rem 0 !important;
    border: none !important;
    box-shadow: none !important;
}}
[data-testid="stChatMessageAvatarAssistant"] {{
    background: {T["accent_soft"]} !important;
    border-radius: 50% !important;
    width: 30px !important;
    height: 30px !important;
    flex-shrink: 0 !important;
}}
[data-testid="stChatMessageAvatarUser"] {{
    background: {T["accent"]} !important;
    border-radius: 50% !important;
    width: 30px !important;
    height: 30px !important;
    flex-shrink: 0 !important;
}}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown {{
    background: {T["bubble_bg"]};
    border: 1px solid {T["bubble_border"]};
    border-radius: 4px 14px 14px 14px;
    padding: 0 !important;
    font-size: 0.875rem;
    font-weight: 400;
    color: {T["bubble_text"]} !important;
    line-height: 1.6;
    letter-spacing: 0.03em;
    box-shadow: 0 1px 6px rgba(91,63,200,0.06);
    display: flex !important;
    align-items: center !important;
    min-height: 0;
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown > div {{
    padding: 0.4rem 1.6rem 1.2rem 1.6rem;
    width: 100%;
    text-align: center;
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown p {{
    color: {T["bubble_text"]} !important;
    margin: 0;
    font-weight: 400;
    letter-spacing: 0.03em;
    line-height: 1.6;
}}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
    flex-direction: row-reverse !important;
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown {{
    background: linear-gradient(135deg, {T["user_bubble_from"]} 0%, {T["user_bubble_to"]} 100%);
    border-radius: 14px 4px 14px 14px;
    padding: 0 !important;
    font-size: 0.875rem;
    color: #ffffff !important;
    line-height: 1.65;
    box-shadow: 0 2px 14px rgba(91,63,200,0.22);
    max-width: 82%;
    word-break: break-word;
    overflow-wrap: break-word;
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown > div {{
    padding: 0.4rem 1.6rem 1.2rem 1.6rem;
    width: 100%;
    text-align: center;
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown p {{
    color: #ffffff !important;
    margin: 0;
    word-break: break-word;
    letter-spacing: 0.03em;
}}

/* ── Skill card ── */
.sc-wrap {{
    background: {T["card_bg"]};
    border: 1px solid {T["card_border"]};
    border-radius: 16px;
    padding: 1.1rem 1.15rem 1rem;
    box-shadow: 0 2px 18px rgba(91,63,200,0.07);
}}
.sc-head {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 0.7rem;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid {T["card_divider"]};
}}
.sc-title {{
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {T["card_title"]};
}}
.sc-badge {{
    font-size: 0.65rem;
    font-weight: 600;
    color: {T["card_badge_text"]};
    background: {T["card_badge_bg"]};
    padding: 0.18rem 0.6rem;
    border-radius: 99px;
}}
.sc-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
}}
.sc-item {{
    background: {T["card_item_bg"]};
    border: 1px solid {T["card_item_border"]};
    border-radius: 11px;
    padding: 0.6rem 0.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    transition: background 0.15s, border-color 0.15s;
}}
.sc-item:hover {{
    background: {T["card_item_hover"]};
    border-color: {T["card_item_hborder"]};
}}
.sc-name {{
    font-size: 0.82rem;
    font-weight: 500;
    color: {T["name_color"]};
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
    min-width: 0;
}}
.sc-pill {{
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.18rem 0.5rem;
    border-radius: 99px;
    white-space: nowrap;
    flex-shrink: 0;
}}
.pill-high   {{ background: #e8f5e9; color: #2e7d32; }}
.pill-medium {{ background: #fff8e1; color: #e65100; }}
.pill-low    {{ background: #fce4ec; color: #c62828; }}
.sc-foot {{
    margin-top: 0.8rem;
    padding-top: 0.65rem;
    border-top: 1px solid {T["card_divider"]};
    font-family: 'Inter', sans-serif;
    font-size: 0.63rem;
    font-weight: 400;
    color: {T["card_foot"]};
    text-align: center;
    line-height: 1.6;
    letter-spacing: 0.01em;
}}

/* ── Typing indicator ──────────────────── */
.typing-box {{
    background: {T["bubble_bg"]};
    border: 1px solid {T["bubble_border"]};
    border-radius: 4px 14px 14px 14px;
    padding: 0.75rem 1rem;
    display: inline-flex;
    flex-direction: column;
    gap: 0.2rem;
    box-shadow: 0 1px 6px rgba(91,63,200,0.06);
}}
.typing-row {{
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.82rem;
    font-weight: 500;
    color: {T["text_primary"]};
}}
.dots span {{
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #9b7ef8;
    display: inline-block;
    animation: tdot 1.2s infinite ease-in-out;
}}
.dots span:nth-child(2) {{ animation-delay: .2s; }}
.dots span:nth-child(3) {{ animation-delay: .4s; }}
@keyframes tdot {{
    0%,80%,100% {{ transform:translateY(0); opacity:.4; }}
    40%         {{ transform:translateY(-4px); opacity:1; }}
}}
.typing-sub {{ font-size: 0.68rem; color: {T["text_muted"]}; }}

/* ── Input ─────────────────────────────── */
.stBottom, [data-testid="stBottom"],
.stBottom > *, [data-testid="stBottom"] > *,
.stBottom > * > *, [data-testid="stBottom"] > * > * {{
    background: transparent !important;
    backdrop-filter: none !important;
    box-shadow: none !important;
    border: none !important;
}}
[data-testid="stChatInputContainer"] {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.4rem 0 !important;
}}
[data-testid="stChatInput"] {{
    background: {T["input_bg"]} !important;
    border: 1.5px solid {T["input_border"]} !important;
    border-radius: 14px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    color: {T["input_text"]} !important;
    box-shadow: 0 2px 14px rgba(91,63,200,0.08) !important;
}}
[data-testid="stChatInput"]:focus-within {{
    border-color: {T["accent"]} !important;
    box-shadow: 0 0 0 3px rgba(91,63,200,0.11), 0 2px 14px rgba(91,63,200,0.08) !important;
}}
textarea[data-testid="stChatInputTextArea"] {{
    background: transparent !important;
    color: {T["input_text"]} !important;
}}
textarea[data-testid="stChatInputTextArea"]::placeholder {{
    color: {T["text_muted"]} !important;
    opacity: 1 !important;
}}

/* ── Streamlit button reset ─────────────── */
div[data-testid="stButton"] button {{
    background: {T["toggle_bg"]} !important;
    border: 1px solid {T["toggle_border"]} !important;
    border-radius: 99px !important;
    color: {T["chip_color"]} !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    padding: 0.3rem 0.9rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    letter-spacing: 0.05em !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: none !important;
}}
div[data-testid="stButton"] button:hover {{
    background: {T["accent_soft"]} !important;
    border-color: {T["accent"]} !important;
}}
div[data-testid="stButton"] button:focus {{
    box-shadow: none !important;
    outline: none !important;
}}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {T["scroll_thumb"]}; border-radius: 99px; }}
</style>
""", unsafe_allow_html=True)

# ── System prompt ──────────────────────────────────────────────
SYSTEM_PROMPT = """You are SkillMatch, an AI that ONLY extracts required skills from job descriptions or job-related queries.

STRICT RULES:
1. VALID inputs (respond with skill JSON):
   - Job descriptions / vacancy postings
   - Questions about what skills are needed for a specific job/role/position
   - "What skills do I need to become a data scientist?"
   - "We are looking for a backend engineer..."
   - "Skills needed for UI/UX designer"

2. INVALID inputs (respond with empty array []):
   - Code snippets or programming questions
   - General knowledge questions unrelated to job skills
   - Random text, gibberish, math, or off-topic content
   - Any request that is not about job skill analysis

3. Output: pure JSON array only. No markdown, no backticks, no explanation.
   Format: [{"skill": "Skill Name", "confidence": 85}, ...]
   - confidence: integer 1-100
   - Max 12 skills, most relevant first
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
        'id': 'Maaf, saya hanya bisa membantu menganalisis deskripsi pekerjaan atau menjawab pertanyaan tentang skill yang dibutuhkan untuk suatu posisi. Silakan tempel lowongan kerja atau tanyakan tentang posisi tertentu.',
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


# ── Validasi input ─────────────────────────────────────────────
def is_job_related(text: str) -> bool:
    t = text.strip()
    t_lower = t.lower()
    if len(t_lower.split()) < 3:
        return False
    hard_code = [
        'def ', 'class ', 'import numpy', 'import pandas', 'import os',
        'import sys', 'from sklearn', 'from torch', 'from tensorflow',
        'print(', 'console.log(', 'system.out.print', 'printf(',
        '#include <', '<?php', 'public static void main',
        'select * from', 'insert into (', 'create table ',
        '#!/usr', 'pip install ', 'npm install ',
        '{ return ', '=> {', 'async function',
    ]
    for sig in hard_code:
        if sig in t_lower:
            return False
    non_job_starts = [
        'what is ', 'explain ', 'define ', 'calculate ',
        'solve ', 'write a poem', 'give me a joke',
        'translate ', 'summarize this', 'buatkan kode',
        'buat program', 'buat fungsi', 'contoh program',
        'how to install', 'how to use',
    ]
    for phrase in non_job_starts:
        if t_lower.startswith(phrase):
            return False
    return True


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
        return f'<p style="font-size:0.85rem;color:{T["text_muted"]};padding:0.5rem 0;">Tidak ada skill yang terdeteksi.</p>'
    items = ""
    for s in sorted(skills, key=lambda x: x["confidence"], reverse=True):
        c = s["confidence"]
        pill = "pill-high" if c >= 70 else ("pill-medium" if c >= 40 else "pill-low")
        items += (
            f'<div class="sc-item">'
            f'<span class="sc-name">{s["skill"]}</span>'
            f'<span class="sc-pill {pill}">{int(c)}%</span>'
            f'</div>'
        )
    return (
        f'<div class="sc-wrap">'
        f'<div class="sc-head">'
        f'<span class="sc-title">Skill yang dibutuhkan</span>'
        f'<span class="sc-badge">{len(skills)} skill</span>'
        f'</div>'
        f'<div class="sc-grid">{items}</div>'
        f'<div class="sc-foot">{t("footer", lang)}</div>'
        f'</div>'
    )


# ── Theme Toggle ───────────────────────────────────────────────
col_space, col_btn = st.columns([5, 1])
with col_btn:
    icon = "🌙" if not st.session_state.dark_mode else "☀️"
    label = f"{icon} {'Dark' if not st.session_state.dark_mode else 'Light'}"
    if st.button(label, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

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

        if not is_job_related(prompt):
            result = []
        else:
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

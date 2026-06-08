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

T = {
    "app_bg":           "#f5f3ff",
    "text_primary":     "#1a1a2e",
    "text_secondary":   "#8580a8",
    "text_muted":       "#b0adca",
    "accent":           "#5b3fc8",
    "accent_soft":      "#ebe6ff",
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
    "pill_high_bg":     "#e8f5e9",
    "pill_high_fg":     "#2e7d32",
    "pill_med_bg":      "#fff8e1",
    "pill_med_fg":      "#e65100",
    "pill_low_bg":      "#fce4ec",
    "pill_low_fg":      "#c62828",
}

BG = T["app_bg"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&display=swap');
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{background-color:{BG}!important;font-family:'Inter',-apple-system,sans-serif;color:{T["text_primary"]};}}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"],[data-testid="stVerticalBlockBorderWrapper"],
.main,.main > *,.block-container,.block-container > div,
[data-testid="stBottomBlockContainer"],[data-testid="stChatFloatingInputContainer"]{{
  background-color:{BG}!important;background:{BG}!important;
}}
div[class^="css-"],div[class*=" css-"]{{background-color:{BG}!important;}}
#MainMenu,footer,header{{visibility:hidden;}}
[data-testid="stSidebar"]{{display:none!important;}}
.block-container{{padding-top:2.5rem!important;padding-bottom:6rem!important;max-width:680px!important;margin:0 auto!important;}}

.hero{{text-align:center;padding:1rem 2rem 2.5rem;}}
.hero-chip{{display:inline-block;background:transparent;color:{T["chip_color"]};font-size:.65rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;padding:.28rem .9rem;border-radius:99px;border:1px solid {T["chip_border"]};margin-bottom:1.4rem;}}
.hero-title{{font-family:'Instrument Serif',Georgia,serif;font-size:2.6rem;font-weight:400;color:{T["hero_title"]};line-height:1.15;margin-bottom:1rem;letter-spacing:-.01em;}}
.hero-title em{{font-style:italic;color:{T["hero_em"]};}}
.hero-sub{{font-size:.875rem;color:{T["text_secondary"]};line-height:1.7;max-width:560px;margin:0 auto;padding:0 1rem;}}

[data-testid="stChatMessage"]{{background:transparent!important;padding:.25rem 0!important;border:none!important;box-shadow:none!important;}}
[data-testid="stChatMessageAvatarAssistant"]{{background:{T["accent_soft"]}!important;border-radius:50%!important;width:30px!important;height:30px!important;flex-shrink:0!important;}}
[data-testid="stChatMessageAvatarUser"]{{background:{T["accent"]}!important;border-radius:50%!important;width:30px!important;height:30px!important;flex-shrink:0!important;}}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown{{background:{T["bubble_bg"]}!important;border:1px solid {T["bubble_border"]};border-radius:4px 14px 14px 14px;padding:0!important;font-size:.875rem;color:{T["bubble_text"]}!important;line-height:1.6;box-shadow:0 1px 6px rgba(91,63,200,.06);display:flex!important;align-items:center!important;}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown>div{{padding:.4rem 1.6rem 1.2rem 1.6rem;width:100%;text-align:center;}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown p{{color:{T["bubble_text"]}!important;margin:0;}}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]){{flex-direction:row-reverse!important;}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown{{background:linear-gradient(135deg,{T["user_bubble_from"]} 0%,{T["user_bubble_to"]} 100%)!important;border-radius:14px 4px 14px 14px;padding:0!important;font-size:.875rem;color:#fff!important;line-height:1.65;box-shadow:0 2px 14px rgba(91,63,200,.22);max-width:82%;word-break:break-word;}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown>div{{padding:.4rem 1.6rem 1.2rem 1.6rem;width:100%;text-align:center;}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown p{{color:#fff!important;margin:0;word-break:break-word;}}

.sc-wrap{{background:{T["card_bg"]};border:1px solid {T["card_border"]};border-radius:16px;padding:1.1rem 1.15rem 1rem;box-shadow:0 2px 18px rgba(91,63,200,.07);}}
.sc-head{{display:flex;justify-content:space-between;align-items:center;padding-bottom:.7rem;margin-bottom:.75rem;border-bottom:1px solid {T["card_divider"]};}}
.sc-title{{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:{T["card_title"]};}}
.sc-badge{{font-size:.65rem;font-weight:600;color:{T["card_badge_text"]};background:{T["card_badge_bg"]};padding:.18rem .6rem;border-radius:99px;}}
.sc-grid{{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;}}
.sc-item{{background:{T["card_item_bg"]};border:1px solid {T["card_item_border"]};border-radius:11px;padding:.6rem .8rem;display:flex;justify-content:space-between;align-items:center;gap:.5rem;transition:background .15s,border-color .15s;}}
.sc-item:hover{{background:{T["card_item_hover"]};border-color:{T["card_item_hborder"]};}}
.sc-name{{font-size:.82rem;font-weight:500;color:{T["name_color"]};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0;}}
.sc-pill{{font-size:.7rem;font-weight:700;padding:.18rem .5rem;border-radius:99px;white-space:nowrap;flex-shrink:0;}}
.pill-high{{background:{T["pill_high_bg"]};color:{T["pill_high_fg"]};}}
.pill-medium{{background:{T["pill_med_bg"]};color:{T["pill_med_fg"]};}}
.pill-low{{background:{T["pill_low_bg"]};color:{T["pill_low_fg"]};}}
.sc-foot{{margin-top:.8rem;padding-top:.65rem;border-top:1px solid {T["card_divider"]};font-size:.63rem;color:{T["card_foot"]};text-align:center;line-height:1.6;}}

.typing-box{{background:{T["bubble_bg"]};border:1px solid {T["bubble_border"]};border-radius:4px 14px 14px 14px;padding:.75rem 1rem;display:inline-flex;flex-direction:column;gap:.2rem;}}
.typing-row{{display:flex;align-items:center;gap:.45rem;font-size:.82rem;font-weight:500;color:{T["text_primary"]};}}
.dots span{{width:5px;height:5px;border-radius:50%;background:#9b7ef8;display:inline-block;animation:tdot 1.2s infinite ease-in-out;}}
.dots span:nth-child(2){{animation-delay:.2s;}}.dots span:nth-child(3){{animation-delay:.4s;}}
@keyframes tdot{{0%,80%,100%{{transform:translateY(0);opacity:.4;}}40%{{transform:translateY(-4px);opacity:1;}}}}
.typing-sub{{font-size:.68rem;color:{T["text_muted"]};}}

.stBottom,[data-testid="stBottom"],.stBottom>*,[data-testid="stBottom"]>*,
.stBottom>*>*,[data-testid="stBottom"]>*>*{{background:{BG}!important;backdrop-filter:none!important;box-shadow:none!important;border:none!important;}}
[data-testid="stChatInputContainer"]{{background:{BG}!important;border:none!important;box-shadow:none!important;padding:.4rem 0!important;}}
[data-testid="stChatInput"]{{background:{T["input_bg"]}!important;border:1.5px solid {T["input_border"]}!important;border-radius:14px!important;font-family:'Inter',sans-serif!important;font-size:.88rem!important;color:{T["input_text"]}!important;box-shadow:0 2px 14px rgba(91,63,200,.08)!important;}}
[data-testid="stChatInput"]:focus-within{{border-color:{T["accent"]}!important;box-shadow:0 0 0 3px rgba(91,63,200,.11)!important;}}
textarea[data-testid="stChatInputTextArea"]{{background:transparent!important;color:{T["input_text"]}!important;}}
textarea[data-testid="stChatInputTextArea"]::placeholder{{color:{T["text_muted"]}!important;}}
::-webkit-scrollbar{{width:4px;}}::-webkit-scrollbar-track{{background:transparent;}}::-webkit-scrollbar-thumb{{background:{T["scroll_thumb"]};border-radius:99px;}}
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """You are SkillMatch, an AI that ONLY extracts required skills from job descriptions or job-related queries.
STRICT RULES:
1. VALID: job descriptions, questions about skills for a role.
2. INVALID: respond with empty array [].
3. Output: pure JSON array only. No markdown, no backticks.
   Format: [{"skill": "Skill Name", "confidence": 85}, ...]
   confidence: 1-100, max 12 skills, names in English"""

def detect_lang(text):
    try:
        lg = detect(text)
        return 'id' if lg in ('id', 'in') else 'en'
    except:
        return 'en'

TEXTS = {
    'greeting': {
        'id': 'Halo! Tempel deskripsi pekerjaan atau tanyakan skill apa yang dibutuhkan untuk posisi tertentu.',
        'en': 'Hello! Paste a job description or ask what skills are needed for a specific role.'
    },
    'not_job': {
        'id': 'Maaf, saya hanya bisa membantu menganalisis deskripsi pekerjaan.',
        'en': 'Sorry, I can only help analyze job descriptions or answer questions about skills for specific roles.'
    },
    'analyzing': {
        'id': ('Menganalisis...', 'Membaca dan mengekstrak skill yang relevan.'),
        'en': ('Analyzing...', 'Reading and extracting relevant skills.')
    },
    'footer': {
        'id': 'Persentase menunjukkan seberapa relevan skill tersebut.',
        'en': 'Confidence score shows how relevant each skill is based on the job description.'
    },
}

def t(key, lang):
    return TEXTS[key].get(lang, TEXTS[key]['en'])

def is_job_related(text):
    tl = text.strip().lower()
    if len(tl.split()) < 3:
        return False
    for sig in ['def ', 'class ', 'import numpy', 'print(', 'console.log(', '#include <', 'select * from', 'pip install ', 'npm install ']:
        if sig in tl:
            return False
    for phrase in ['what is ', 'explain ', 'define ', 'calculate ', 'solve ', 'write a poem', 'give me a joke', 'buatkan kode', 'buat program', 'how to install']:
        if tl.startswith(phrase):
            return False
    return True

def extract_skills(text):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        return {"error": "GROQ_API_KEY tidak ditemukan."}
    try:
        client = Groq(api_key=api_key)
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}],
            temperature=0.1,
        )
        raw = res.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        data = json.loads(raw)
        if not isinstance(data, list):
            return []
        return [{"skill": str(s["skill"]), "confidence": round(float(s["confidence"]), 1)} for s in data if "skill" in s and "confidence" in s]
    except json.JSONDecodeError:
        return {"error": "Format tidak valid."}
    except Exception as e:
        return {"error": str(e)}

def render_skills(skills, lang='en'):
    if not skills:
        return f'<p style="font-size:.85rem;color:{T["text_muted"]};padding:.5rem 0;">Tidak ada skill terdeteksi.</p>'
    items = ""
    for s in sorted(skills, key=lambda x: x["confidence"], reverse=True):
        c = s["confidence"]
        pill = "pill-high" if c >= 70 else ("pill-medium" if c >= 40 else "pill-low")
        items += f'<div class="sc-item"><span class="sc-name">{s["skill"]}</span><span class="sc-pill {pill}">{int(c)}%</span></div>'
    return (
        f'<div class="sc-wrap"><div class="sc-head">'
        f'<span class="sc-title">Skill yang dibutuhkan</span>'
        f'<span class="sc-badge">{len(skills)} skill</span></div>'
        f'<div class="sc-grid">{items}</div>'
        f'<div class="sc-foot">{t("footer", lang)}</div></div>'
    )

st.markdown("""
<div class="hero">
  <div class="hero-chip">Career Intelligence</div>
  <div class="hero-title">Find the skills you<br><em>actually</em> need</div>
  <p class="hero-sub">Paste any job description and we will extract the must-have skills so you can focus on what matters.</p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": t('greeting', 'en'), "type": "text"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "skills":
            st.markdown(render_skills(msg["skills"], msg.get("lang", "en")), unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

if prompt := st.chat_input("Paste a job description or ask about a role..."):
    lang = detect_lang(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        main_txt, sub_txt = t('analyzing', lang)
        ph = st.empty()
        ph.markdown(
            f'<div class="typing-box"><div class="typing-row">'
            f'<div class="dots"><span></span><span></span><span></span></div>{main_txt}</div>'
            f'<div class="typing-sub">{sub_txt}</div></div>',
            unsafe_allow_html=True
        )
        result = extract_skills(prompt) if is_job_related(prompt) else []
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


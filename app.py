import streamlit as st
import json
from groq import Groq
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

st.set_page_config(page_title="SkillMatch", page_icon="○", layout="centered", initial_sidebar_state="collapsed")

# ==================== CSS (sama persis dengan kode sehat) ====================
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&family=DM+Serif+Display:ital@0;1&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*='css'] {
  font-family: 'DM Sans', -apple-system, sans-serif;
  color: #1c1c1e;
}

.stApp { background: #f0eeff; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none !important; }

.block-container {
  padding-top: 0 !important;
  padding-bottom: 7rem !important;
  max-width: 660px !important;
}

.hero {
  padding: 4rem 0 2.5rem;
  border-bottom: 1px solid #d8ccf5;
  margin-bottom: 2rem;
  text-align: center;
}
.hero-label {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #6b4fbb;
  background: #e8deff;
  border: 1px solid #cbbdf5;
  border-radius: 99px;
  padding: 0.3rem 0.85rem;
  margin-bottom: 1.4rem;
}
.hero h1 {
  font-family: 'DM Serif Display', Georgia, serif;
  font-size: 3rem;
  font-weight: 400;
  line-height: 1.15;
  color: #1c1c1e;
  margin-bottom: 1.1rem;
}
.hero h1 em { font-style: italic; color: #7c5cbf; }
.hero-sub {
  font-size: 0.9rem;
  color: #6b6b7a;
  line-height: 1.75;
  max-width: 420px;
  font-weight: 300;
  margin: 0 auto;
  text-align: center;
}

[data-testid="stChatMessage"] {
  background: transparent !important;
  padding: 0.25rem 0 !important;
  border: none !important;
  box-shadow: none !important;
  gap: 0.8rem !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown {
  background: #fff;
  border: 1px solid #ddd5f5;
  border-radius: 2px 12px 12px 12px;
  padding: 1rem 1.25rem;
  line-height: 1.7;
  color: #1c1c1e !important;
  font-size: 0.9rem;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown p {
  color: #1c1c1e !important;
  margin: 0;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown {
  background: #6b4fbb;
  border-radius: 12px 12px 2px 12px;
  padding: 1rem 1.25rem;
  color: #fff !important;
  font-size: 0.9rem;
  line-height: 1.7;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown p {
  color: #fff !important;
  margin: 0;
}

[data-testid="stChatMessageAvatarAssistant"] {
  background: #e8deff !important;
  border-radius: 8px !important;
  color: #6b4fbb !important;
  font-size: 0.75rem !important;
  font-weight: 500 !important;
  border: 1px solid #cbbdf5 !important;
}
[data-testid="stChatMessageAvatarUser"] {
  background: #6b4fbb !important;
  border-radius: 8px !important;
  color: #fff !important;
  font-size: 0.75rem !important;
  font-weight: 500 !important;
}

.typing-wrap {
  background: #fff;
  border: 1px solid #ddd5f5;
  border-radius: 2px 12px 12px 12px;
  padding: 0.9rem 1.2rem;
  width: fit-content;
  max-width: 280px;
}
.typing-top { display: flex; align-items: center; gap: 0.55rem; margin-bottom: 0.35rem; }
.typing-dots { display: flex; gap: 4px; }
.typing-dots span {
  width: 6px; height: 6px;
  background: #b8a4e8;
  border-radius: 50%;
  animation: tdot 1.2s infinite ease-in-out;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes tdot {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
  40%           { transform: translateY(-4px); opacity: 1; }
}
.typing-main { font-size: 0.83rem; font-weight: 500; color: #1c1c1e; }
.typing-sub  { font-size: 0.76rem; color: #9b8fc0; line-height: 1.5; }

.result-wrap {
  background: #fff;
  border: 1px solid #ddd5f5;
  border-radius: 14px;
  padding: 1.4rem 1.5rem;
}
.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  padding-bottom: 0.9rem;
  border-bottom: 1px solid #ede8ff;
}
.result-title {
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #6b4fbb;
}
.result-count {
  font-size: 0.75rem;
  color: #b8a4e8;
  background: #f0eeff;
  padding: 0.15rem 0.6rem;
  border-radius: 99px;
  border: 1px solid #ddd5f5;
}

.skill-list { display: flex; flex-direction: column; gap: 0.5rem; }
.skill-row {
  display: grid;
  grid-template-columns: 22px 1fr 90px 36px;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 0.9rem;
  background: #f8f5ff;
  border: 1px solid #ede8ff;
  border-radius: 8px;
  transition: border-color 0.15s, background 0.15s;
}
.skill-row:hover { border-color: #b8a4e8; background: #f0eeff; }
.skill-rank {
  font-size: 0.68rem;
  color: #b8a4e8;
  font-weight: 600;
  text-align: center;
}
.skill-name {
  font-size: 0.875rem;
  font-weight: 400;
  color: #1c1c1e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.skill-bar-bg {
  width: 100%;
  height: 4px;
  background: #ede8ff;
  border-radius: 99px;
  overflow: hidden;
}
.skill-bar-fill { height: 100%; border-radius: 99px; background: #7c5cbf; }
.skill-pct {
  font-size: 0.75rem;
  font-weight: 600;
  color: #7c5cbf;
  text-align: right;
}
.result-footer {
  margin-top: 1rem;
  padding-top: 0.85rem;
  border-top: 1px solid #ede8ff;
  font-size: 0.72rem;
  color: #b8a4e8;
  line-height: 1.6;
  text-align: center;
}

[data-testid="stChatInputContainer"],
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
.stBottom, .stBottom > div {
  background: #f0eeff !important;
  border-top: 1px solid #ddd5f5 !important;
}
[data-testid="stChatInput"] {
  background: #fff !important;
  border: 1px solid #cbbdf5 !important;
  border-radius: 10px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.9rem !important;
  color: #1c1c1e !important;
  box-shadow: none !important;
}
[data-testid="stChatInput"]:focus-within {
  border-color: #7c5cbf !important;
  box-shadow: 0 0 0 3px rgba(124,92,191,0.1) !important;
}

.footer-bar {
  display: flex;
  justify-content: space-between;
  padding: 0.3rem 0.1rem 0;
}
.footer-bar span { font-size: 0.69rem; color: #b8a4e8; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbbdf5; border-radius: 99px; }
</style>''', unsafe_allow_html=True)

# ==================== SYSTEM PROMPT (BAHASA INGGRIS, UNTUK MULTIBAHASA) ====================
SYSTEM_PROMPT = (
    "You are an AI that ONLY extracts skills from job descriptions. "
    "If the input is NOT a job description (e.g., code, poem, general question, or any text that does not describe a job vacancy), "
    "you MUST respond with an empty JSON array: []\n"
    "Your output MUST be a pure JSON array, no other text, no markdown backticks.\n"
    'Format: [{"skill": "Skill Name", "confidence": 85}, ...]\n'
    "confidence: integer 1-100.\n"
    "Extract max 12 most relevant skills.\n"
    "Skill names in English.\n"
    "NEVER add any comments or explanations."
)

# ==================== FUNGSI DETEKSI BAHASA ====================
def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        if lang in ('id', 'in'): return 'id'
        if lang == 'en': return 'en'
        if lang.startswith('zh'): return 'zh'
        if lang == 'ja': return 'ja'
        if lang == 'ar': return 'ar'
        if lang == 'ko': return 'ko'
        # tambahkan bahasa lain jika perlu
        return 'en'
    except LangDetectException:
        return 'en'

# ==================== FUNGSI TERJEMAHAN PESAN ERROR ====================
def get_error_message(lang: str) -> str:
    messages = {
        'id': 'Maaf, chatbot ini didesain untuk rekomendasi pekerjaan.',
        'en': 'Sorry, this chatbot is designed for job recommendation.',
        'zh': '抱歉，此聊天机器人专为工作推荐而设计。',
        'ja': '申し訳ありませんが、このチャットボットは仕事の推薦のために設計されています。',
        'ar': 'عذرًا، تم تصميم هذا الدردشة الآلي لتوصيات الوظائف.',
        'ko': '죄송합니다. 이 챗봇은 채용 추천을 위해 설계되었습니다.',
    }
    return messages.get(lang, messages['en'])

def get_greeting(lang: str) -> str:
    greetings = {
        'id': 'Halo! Tempel deskripsi pekerjaan dari lowongan yang kamu incar, dan saya akan menganalisis skill apa saja yang dibutuhkan.',
        'en': 'Hello! Paste the job description you\'re aiming for, and I will analyze the required skills.',
        'zh': '你好！粘贴你心仪的职位描述，我将分析所需的技能。',
        'ja': 'こんにちは！志望する求人情報を貼り付けると、必要なスキルを分析します。',
        'ar': 'مرحبًا! الصق وصف الوظيفة التي تطمح إليها، وسأقوم بتحليل المهارات المطلوبة.',
        'ko': '안녕하세요! 원하는 직무 설명을 붙여넣으면 필요한 기술을 분석해 드립니다.',
    }
    return greetings.get(lang, greetings['en'])

# ==================== FUNGSI EKSTRAKSI DENGAN GROQ ====================
def extract_skills_groq(job_description):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return {"error": "GROQ_API_KEY tidak ditemukan. Tambahkan di Secrets Streamlit."}
    
    client = Groq(api_key=api_key)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Job description:\n\n" + job_description}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.1,
        )
        raw = chat_completion.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        skills = json.loads(raw)
        if not isinstance(skills, list):
            return []
        return [
            {"skill": str(i["skill"]), "confidence": round(float(i["confidence"]), 1)}
            for i in skills if "skill" in i and "confidence" in i
        ]
    except Exception as e:
        return {"error": f"Groq API error: {str(e)}"}

# ==================== FUNGSI RENDER SKILL ====================
def render_skill_cards(skills):
    if not skills:
        return '<p style="color:#aaa; font-size:0.875rem;">Tidak ada skill yang ditemukan.</p>'
    count = len(skills)
    sorted_skills = sorted(skills, key=lambda x: x["confidence"], reverse=True)
    html = f'<div class="result-wrap"><div class="result-header"><span class="result-title">Skill yang dibutuhkan</span><span class="result-count">{count} skill</span></div><div class="skill-list">'
    for idx, item in enumerate(sorted_skills, 1):
        c = item["confidence"]
        name = item["skill"]
        html += f'<div class="skill-row"><span class="skill-rank">{idx}</span><span class="skill-name">{name}</span><div class="skill-bar-bg"><div class="skill-bar-fill" style="width:{c}%"></div></div><span class="skill-pct">{int(c)}%</span></div>'
    html += '</div><div class="result-footer">Persentase menunjukkan seberapa relevan skill tersebut berdasarkan deskripsi pekerjaan yang diberikan.</div></div>'
    return html

# ==================== UI HEADER (STATIS BAHASA INDONESIA) ====================
st.markdown('''<div class="hero">
  <div class="hero-label">AI-Powered Career Tool</div>
  <h1>Temukan skill yang kamu<br>butuhkan, <em>sekarang.</em></h1>
  <p class="hero-sub">Paste deskripsi pekerjaan dari lowongan manapun, dan kami akan menganalisis skill apa saja yang paling dibutuhkan untuk posisi tersebut.</p>
</div>''', unsafe_allow_html=True)

# ==================== STATE CHAT ====================
if "messages" not in st.session_state:
    # Pesan sambutan default (Inggris) akan diperbarui saat user pertama kali chat
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! Paste the job description you're aiming for, and I will analyze the required skills.",
        "type": "text"
    }]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "skills":
            st.markdown(render_skill_cards(msg["skills"]), unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

# ==================== INPUT & RESPON (TANPA FILTER MANUAL) ====================
if prompt := st.chat_input("Paste job description here..."):
    # Deteksi bahasa user
    user_lang = detect_language(prompt)
    
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown('<div class="typing-wrap"><div class="typing-top"><div class="typing-dots"><span></span><span></span><span></span></div><span class="typing-main">Analyzing...</span></div><div class="typing-sub">Reading and extracting relevant skills.</div></div>', unsafe_allow_html=True)
        
        result = extract_skills_groq(prompt)
        placeholder.empty()
        
        if isinstance(result, dict) and "error" in result:
            resp = f"**Error**: {result['error']}"
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp, "type": "text"})
        elif not result:
            # Tampilkan pesan error dalam bahasa user
            error_msg = get_error_message(user_lang)
            st.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg, "type": "text"})
        else:
            # Tampilkan hasil skill
            st.markdown(render_skill_cards(result), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "skills": result, "type": "skills"})
    
    # Optional: perbarui pesan sambutan dengan bahasa user untuk percakapan berikutnya
    # (tidak wajib, karena hanya tampil sekali)
    if len(st.session_state.messages) == 2:  # setelah pesan pertama user
        greeting_in_user_lang = get_greeting(user_lang)
        # ganti pesan pertama assistant dengan bahasa user
        st.session_state.messages[0]["content"] = greeting_in_user_lang
        st.rerun()

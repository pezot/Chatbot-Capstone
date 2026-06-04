import streamlit as st
import json
from groq import Groq
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

st.set_page_config(page_title="SkillMatch", page_icon="○", layout="centered", initial_sidebar_state="collapsed")

# ==================== CSS LEBIH RAPI & NATURAL ====================
st.markdown('''
<style>
/* Font modern & bersahabat */
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: #faf8ff;
}

/* Sembunyikan elemen default Streamlit yang mengganggu */
#MainMenu, footer, header {
    visibility: hidden;
}
[data-testid="stSidebar"] {
    display: none !important;
}

/* Container utama lebih lega */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 5rem !important;
    max-width: 720px !important;
}

/* Hero section simpel & elegan */
.hero {
    text-align: center;
    margin-bottom: 2rem;
    padding: 0.5rem 0 1rem;
}
.hero-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6d4fc9;
    background: #ede7ff;
    display: inline-block;
    padding: 0.2rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 1rem;
    border: 1px solid #ddd2fc;
}
.hero h1 {
    font-size: 2rem;
    font-weight: 600;
    color: #1e1e2f;
    margin-bottom: 0.5rem;
    line-height: 1.3;
}
.hero h1 em {
    font-style: italic;
    color: #6d4fc9;
    font-weight: 500;
}
.hero-sub {
    font-size: 0.9rem;
    color: #6b6b84;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Chat bubbles natural */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 0.4rem 0 !important;
    gap: 0.75rem !important;
}
[data-testid="stChatMessageAvatarUser"] {
    background: #6d4fc9 !important;
    border-radius: 50% !important;
    color: white !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: #e9e2ff !important;
    border-radius: 50% !important;
    color: #6d4fc9 !important;
}
/* Pesan user */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown {
    background: #6d4fc9;
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
    line-height: 1.5;
}
/* Pesan assistant (teks biasa) */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown {
    background: white;
    border: 1px solid #e2d9fc;
    border-radius: 18px 18px 18px 4px;
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
    color: #1e1e2f;
    line-height: 1.5;
}

/* Typing indicator */
.typing-wrap {
    background: white;
    border: 1px solid #e2d9fc;
    border-radius: 18px 18px 18px 4px;
    padding: 0.7rem 1.2rem;
    width: fit-content;
    max-width: 260px;
}
.typing-top {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.typing-dots span {
    width: 6px;
    height: 6px;
    background: #b7a5eb;
    border-radius: 50%;
    display: inline-block;
    animation: tdot 1.2s infinite ease-in-out;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes tdot {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40% { transform: translateY(-4px); opacity: 1; }
}
.typing-main {
    font-size: 0.85rem;
    font-weight: 500;
    color: #1e1e2f;
}
.typing-sub {
    font-size: 0.7rem;
    color: #8e8ea7;
    margin-top: 0.2rem;
}

/* Skill cards - lebih rapi */
.result-wrap {
    background: white;
    border: 1px solid #ede7ff;
    border-radius: 20px;
    padding: 1rem 1.2rem;
}
.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #f0ebff;
    padding-bottom: 0.7rem;
    margin-bottom: 0.8rem;
}
.result-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #6d4fc9;
}
.result-count {
    background: #f0ebff;
    padding: 0.15rem 0.6rem;
    border-radius: 30px;
    font-size: 0.65rem;
    color: #6d4fc9;
}
.skill-list {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}
.skill-row {
    display: grid;
    grid-template-columns: 28px 1fr 70px;
    align-items: center;
    gap: 0.8rem;
    padding: 0.4rem 0.5rem;
    background: #faf8ff;
    border-radius: 12px;
}
.skill-rank {
    font-size: 0.7rem;
    font-weight: 600;
    color: #b7a5eb;
    text-align: center;
}
.skill-name {
    font-size: 0.85rem;
    font-weight: 500;
    color: #1e1e2f;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.skill-bar-bg {
    width: 100%;
    height: 4px;
    background: #ede7ff;
    border-radius: 4px;
}
.skill-bar-fill {
    height: 100%;
    background: #6d4fc9;
    border-radius: 4px;
}
.skill-pct {
    font-size: 0.7rem;
    font-weight: 600;
    color: #6d4fc9;
    text-align: right;
}
.result-footer {
    margin-top: 0.8rem;
    padding-top: 0.6rem;
    border-top: 1px solid #f0ebff;
    font-size: 0.65rem;
    color: #a2a2bd;
    text-align: center;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: white !important;
    border: 1px solid #ddd2fc !important;
    border-radius: 30px !important;
    padding: 0.5rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #6d4fc9 !important;
    box-shadow: 0 0 0 2px rgba(109,79,201,0.1) !important;
}

/* Footer */
.footer-bar {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0.2rem 0;
    font-size: 0.6rem;
    color: #b8b8d2;
    margin-top: 1rem;
}
</style>
''', unsafe_allow_html=True)

# ==================== SYSTEM PROMPT (TEGAS) ====================
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

# ==================== DETEKSI BAHASA & TERJEMAHAN ====================
def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        if lang in ('id', 'in'): return 'id'
        if lang == 'en': return 'en'
        if lang.startswith('zh'): return 'zh'
        if lang == 'ja': return 'ja'
        if lang == 'ar': return 'ar'
        if lang == 'ko': return 'ko'
        if lang in ('pt', 'pt-br'): return 'pt'
        return 'en'
    except LangDetectException:
        return 'en'

def get_error_message(lang: str) -> str:
    messages = {
        'id': 'Maaf, chatbot ini hanya untuk rekomendasi pekerjaan. Silakan tempel deskripsi pekerjaan atau tanyakan skill yang dibutuhkan untuk suatu posisi.',
        'en': 'Sorry, this chatbot is only for job recommendations. Please paste a job description or ask what skills are needed for a position.',
        'pt': 'Desculpe, este chatbot é apenas para recomendações de trabalho. Cole uma descrição de vaga ou pergunte quais habilidades são necessárias para uma posição.',
        'zh': '抱歉，此聊天机器人仅用于工作推荐。请粘贴职位描述或询问某个职位所需的技能。',
        'ja': '申し訳ありません、このチャットボットは仕事の推薦専用です。求人情報を貼り付けるか、必要なスキルを質問してください。',
        'ar': 'عذرًا، هذا الدردشة الآلي مخصص لتوصيات الوظائف فقط. يرجى لصق وصف وظيفي أو اسأل عن المهارات المطلوبة.',
        'ko': '죄송합니다. 이 챗봇은 채용 추천 전용입니다. 직무 설명을 붙여넣거나 필요한 기술에 대해 질문하세요.',
    }
    return messages.get(lang, messages['en'])

def get_greeting(lang: str) -> str:
    greetings = {
        'id': 'Halo! Tempel deskripsi pekerjaan atau tanyakan skill yang dibutuhkan untuk posisi tertentu.',
        'en': 'Hello! Paste a job description or ask what skills are needed for a position.',
        'pt': 'Olá! Cole uma descrição de vaga ou pergunte quais habilidades são necessárias para uma posição.',
        'zh': '你好！请粘贴职位描述或询问某个职位所需的技能。',
        'ja': 'こんにちは！求人情報を貼り付けるか、必要なスキルを質問してください。',
        'ar': 'مرحبًا! الصق وصف الوظيفة أو اسأل عن المهارات المطلوبة.',
        'ko': '안녕하세요! 직무 설명을 붙여넣거나 필요한 기술에 대해 질문하세요.',
    }
    return greetings.get(lang, greetings['en'])

def get_analyzing_text(lang: str):
    texts = {
        'id': ('Menganalisis...', 'Membaca dan mengekstrak skill yang relevan.'),
        'en': ('Analyzing...', 'Reading and extracting relevant skills.'),
        'pt': ('Analisando...', 'Lendo e extraindo habilidades relevantes.'),
        'zh': ('分析中...', '阅读并提取相关技能。'),
        'ja': ('分析中...', '関連スキルを読み取り抽出しています。'),
        'ar': ('جاري التحليل...', 'قراءة واستخراج المهارات ذات الصلة.'),
        'ko': ('분석 중...', '관련 기술을 읽고 추출하는 중입니다.'),
    }
    return texts.get(lang, texts['en'])

# ==================== EKSTRAKSI SKILL ====================
def extract_skills_groq(job_description):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return {"error": "GROQ_API_KEY not found. Add to Secrets."}
    client = Groq(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Job description:\n\n" + job_description}
            ],
            temperature=0.1,
        )
        raw = completion.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        skills = json.loads(raw)
        if not isinstance(skills, list):
            return []
        return [
            {"skill": str(s["skill"]), "confidence": round(float(s["confidence"]), 1)}
            for s in skills if "skill" in s and "confidence" in s
        ]
    except Exception as e:
        return {"error": str(e)}

def render_skill_cards(skills):
    if not skills:
        return '<p style="color:#aaa; font-size:0.85rem;">Tidak ada skill yang ditemukan.</p>'
    sorted_skills = sorted(skills, key=lambda x: x["confidence"], reverse=True)
    html = f'<div class="result-wrap"><div class="result-header"><span class="result-title">Skill yang dibutuhkan</span><span class="result-count">{len(skills)} skill</span></div><div class="skill-list">'
    for i, s in enumerate(sorted_skills, 1):
        html += f'<div class="skill-row"><span class="skill-rank">{i}</span><span class="skill-name">{s["skill"]}</span><div class="skill-bar-bg"><div class="skill-bar-fill" style="width:{s["confidence"]}%"></div></div><span class="skill-pct">{int(s["confidence"])}%</span></div>'
    html += '</div><div class="result-footer">Persentase menunjukkan seberapa relevan skill tersebut berdasarkan deskripsi pekerjaan yang diberikan.</div></div>'
    return html

# ==================== UI HEADER (LEBIH SIMPEL) ====================
st.markdown('''
<div class="hero">
  <div class="hero-label">Career Intelligence</div>
  <h1>Find the skills you <em>actually</em> need</h1>
  <p class="hero-sub">Paste any job description — we'll extract the must-have skills so you can focus on what matters.</p>
</div>
''', unsafe_allow_html=True)

# ==================== STATE CHAT ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": get_greeting('en'),
        "type": "text"
    }]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "skills":
            st.markdown(render_skill_cards(msg["skills"]), unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

# ==================== INPUT HANDLING (TANPA FILTER MANUAL) ====================
prompt = st.chat_input("Paste job description or ask for required skills...")
if prompt:
    user_lang = detect_language(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        analyzing_main, analyzing_sub = get_analyzing_text(user_lang)
        placeholder = st.empty()
        placeholder.markdown(f'<div class="typing-wrap"><div class="typing-top"><div class="typing-dots"><span></span><span></span><span></span></div><span class="typing-main">{analyzing_main}</span></div><div class="typing-sub">{analyzing_sub}</div></div>', unsafe_allow_html=True)
        
        result = extract_skills_groq(prompt)
        placeholder.empty()
        
        if isinstance(result, dict) and "error" in result:
            st.markdown(f"**Error**: {result['error']}")
            st.session_state.messages.append({"role": "assistant", "content": f"**Error**: {result['error']}", "type": "text"})
        elif not result:
            error_msg = get_error_message(user_lang)
            st.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg, "type": "text"})
        else:
            st.markdown(render_skill_cards(result), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "skills": result, "type": "skills"})
    
    if len(st.session_state.messages) == 2:
        st.session_state.messages[0]["content"] = get_greeting(user_lang)
        st.rerun()

import streamlit as st
import json
from groq import Groq
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

st.set_page_config(page_title="SkillMatch", page_icon="○", layout="centered", initial_sidebar_state="collapsed")

# ==================== CSS LENGKAP (sama seperti sebelumnya) ====================
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

# ==================== INISIALISASI STATE ====================
if "current_lang" not in st.session_state:
    st.session_state.current_lang = 'en'  # default english
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================== TERJEMAHAN MULTIBAHASA ====================
TRANSLATIONS = {
    'id': {
        'hero_label': 'AI-Powered Career Tool',
        'hero_title': 'Temukan skill yang kamu<br>butuhkan, <em>sekarang.</em>',
        'hero_sub': 'Paste deskripsi pekerjaan dari lowongan manapun, dan kami akan menganalisis skill apa saja yang paling dibutuhkan untuk posisi tersebut.',
        'chat_placeholder': 'Tempel deskripsi pekerjaan di sini...',
        'assistant_greeting': 'Halo! Tempel deskripsi pekerjaan dari lowongan yang kamu incar, dan saya akan menganalisis skill apa saja yang dibutuhkan.',
        'analyzing': 'Menganalisis...',
        'analyzing_sub': 'Membaca dan mengekstrak skill yang relevan.',
        'result_title': 'Skill yang dibutuhkan',
        'result_footer': 'Persentase menunjukkan seberapa relevan skill tersebut berdasarkan deskripsi pekerjaan yang diberikan.',
        'error_not_job': 'Maaf, chatbot ini didesain untuk rekomendasi pekerjaan.',
        'no_skills': 'Tidak ada skill yang ditemukan.',
    },
    'en': {
        'hero_label': 'AI-Powered Career Tool',
        'hero_title': 'Discover the skills you<br>need, <em>now.</em>',
        'hero_sub': 'Paste any job description from any vacancy, and we will analyze the most required skills for that position.',
        'chat_placeholder': 'Paste job description here...',
        'assistant_greeting': 'Hello! Paste the job description you\'re aiming for, and I will analyze the required skills.',
        'analyzing': 'Analyzing...',
        'analyzing_sub': 'Reading and extracting relevant skills.',
        'result_title': 'Required Skills',
        'result_footer': 'The percentage indicates how relevant the skill is based on the job description provided.',
        'error_not_job': 'Sorry, this chatbot is designed for job recommendation.',
        'no_skills': 'No skills found.',
    },
    'zh-cn': {
        'hero_label': 'AI驱动的职业工具',
        'hero_title': '发现你需要的技能<br><em>现在.</em>',
        'hero_sub': '粘贴任何职位的职位描述，我们将分析该职位最需要的技能。',
        'chat_placeholder': '在此处粘贴职位描述...',
        'assistant_greeting': '你好！粘贴你心仪的职位描述，我将分析所需的技能。',
        'analyzing': '分析中...',
        'analyzing_sub': '阅读并提取相关技能。',
        'result_title': '所需技能',
        'result_footer': '百分比表示根据提供的职位描述，该技能的相关程度。',
        'error_not_job': '抱歉，此聊天机器人专为工作推荐而设计。',
        'no_skills': '未找到技能。',
    },
    'ja': {
        'hero_label': 'AI搭載のキャリアツール',
        'hero_title': '必要なスキルを<br><em>今すぐ</em>見つけましょう',
        'hero_sub': '任意の求人情報を貼り付けると、そのポジションに最も必要なスキルを分析します。',
        'chat_placeholder': 'ここに求人情報を貼り付けてください...',
        'assistant_greeting': 'こんにちは！志望する求人情報を貼り付けると、必要なスキルを分析します。',
        'analyzing': '分析中...',
        'analyzing_sub': '関連スキルを読み取り抽出しています。',
        'result_title': '必要なスキル',
        'result_footer': 'パーセンテージは、提供された求人情報に基づくスキルの関連性を示します。',
        'error_not_job': '申し訳ありませんが、このチャットボットは仕事の推薦のために設計されています。',
        'no_skills': 'スキルが見つかりません。',
    },
    'ar': {
        'hero_label': 'أداة مهنية تعمل بالذكاء الاصطناعي',
        'hero_title': 'اكتشف المهارات التي<br>تحتاجها، <em>الآن.</em>',
        'hero_sub': 'الصق وصف الوظيفة من أي شاغر، وسنقوم بتحليل المهارات الأكثر طلبًا لهذا المنصب.',
        'chat_placeholder': 'الصق وصف الوظيفة هنا...',
        'assistant_greeting': 'مرحبًا! الصق وصف الوظيفة التي تطمح إليها، وسأقوم بتحليل المهارات المطلوبة.',
        'analyzing': 'جاري التحليل...',
        'analyzing_sub': 'قراءة واستخراج المهارات ذات الصلة.',
        'result_title': 'المهارات المطلوبة',
        'result_footer': 'تشير النسبة المئوية إلى مدى أهمية المهارة بناءً على وصف الوظيفة المقدم.',
        'error_not_job': 'عذرًا، تم تصميم هذا الدردشة الآلي لتوصيات الوظائف.',
        'no_skills': 'لم يتم العثور على مهارات.',
    },
    'ko': {
        'hero_label': 'AI 기반 커리어 도구',
        'hero_title': '필요한 기술을<br><em>지금</em> 찾아보세요',
        'hero_sub': '어떤 채용 공고든 직무 설명을 붙여넣으면 해당 직무에 가장 필요한 기술을 분석해 드립니다.',
        'chat_placeholder': '직무 설명을 여기에 붙여넣으세요...',
        'assistant_greeting': '안녕하세요! 원하는 직무 설명을 붙여넣으면 필요한 기술을 분석해 드립니다.',
        'analyzing': '분석 중...',
        'analyzing_sub': '관련 기술을 읽고 추출하는 중입니다.',
        'result_title': '필요한 기술',
        'result_footer': '백분율은 제공된 직무 설명을 기반으로 기술의 관련성을 나타냅니다.',
        'error_not_job': '죄송합니다. 이 챗봇은 채용 추천을 위해 설계되었습니다.',
        'no_skills': '기술을 찾을 수 없습니다.',
    }
}

def get_translation(lang_code):
    """Mengembalikan dictionary terjemahan, fallback ke 'en' jika tidak ditemukan."""
    if lang_code in TRANSLATIONS:
        return TRANSLATIONS[lang_code]
    else:
        return TRANSLATIONS['en']

# ==================== DETEKSI BAHASA ====================
def detect_language(text: str) -> str:
    """Deteksi bahasa dari teks input user, kembalikan kode yang ada di TRANSLATIONS."""
    try:
        lang = detect(text)
        if lang in ('id', 'in'):
            return 'id'
        elif lang == 'en':
            return 'en'
        elif lang in ('zh-cn', 'zh-tw', 'zh'):
            return 'zh-cn'
        elif lang == 'ja':
            return 'ja'
        elif lang == 'ar':
            return 'ar'
        elif lang == 'ko':
            return 'ko'
        else:
            return 'en'
    except LangDetectException:
        return 'en'

# ==================== SYSTEM PROMPT (tetap Inggris) ====================
SYSTEM_PROMPT = (
    "You are an AI that ONLY extracts skills from job descriptions. "
    "If the input is NOT a job description (e.g., code, poem, general question, coding command, or any text that does not describe a job vacancy), "
    "you MUST respond with an empty JSON array: []\n"
    "Your output MUST be a pure JSON array, no other text, no markdown backticks.\n"
    'Format: [{"skill": "Skill Name", "confidence": 85}, ...]\n'
    "confidence: integer 1-100.\n"
    "Extract max 12 most relevant skills.\n"
    "Skill names in English.\n"
    "NEVER add any comments or explanations."
)

# ==================== EKSTRAKSI SKILL ====================
def extract_skills_groq(job_description):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return {"error": "GROQ_API_KEY not found. Add it to Streamlit Secrets."}
    
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

# ==================== RENDER SKILL CARD (MULTIBAHASA) ====================
def render_skill_cards(skills, lang_code):
    t = get_translation(lang_code)
    if not skills:
        return f'<p style="color:#aaa; font-size:0.875rem;">{t["no_skills"]}</p>'
    count = len(skills)
    sorted_skills = sorted(skills, key=lambda x: x["confidence"], reverse=True)
    html = f'<div class="result-wrap"><div class="result-header"><span class="result-title">{t["result_title"]}</span><span class="result-count">{count} skill</span></div><div class="skill-list">'
    for idx, item in enumerate(sorted_skills, 1):
        c = item["confidence"]
        name = item["skill"]
        html += f'<div class="skill-row"><span class="skill-rank">{idx}</span><span class="skill-name">{name}</span><div class="skill-bar-bg"><div class="skill-bar-fill" style="width:{c}%"></div></div><span class="skill-pct">{int(c)}%</span></div>'
    html += f'</div><div class="result-footer">{t["result_footer"]}</div></div>'
    return html

# ==================== RENDER UI ====================
def render_ui():
    t = get_translation(st.session_state.current_lang)
    
    st.markdown(f'''<div class="hero">
      <div class="hero-label">{t["hero_label"]}</div>
      <h1>{t["hero_title"]}</h1>
      <p class="hero-sub">{t["hero_sub"]}</p>
    </div>''', unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("type") == "skills":
                st.markdown(render_skill_cards(msg["skills"], st.session_state.current_lang), unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])
    
    st.markdown(f'<div class="footer-bar"><span>{t["footer_left"]}</span><span>{t["footer_right"]}</span></div>', unsafe_allow_html=True)
    return t

# Jika belum ada pesan, tambahkan greeting (dalam bahasa default: Inggris)
if not st.session_state.messages:
    default_t = get_translation('en')
    st.session_state.messages.append({
        "role": "assistant",
        "content": default_t["assistant_greeting"],
        "type": "text"
    })

# Render UI awal
t = render_ui()

# ==================== INPUT ====================
prompt = st.chat_input(t["chat_placeholder"])
if prompt:
    # Deteksi bahasa dari input user
    user_lang = detect_language(prompt)
    st.session_state.current_lang = user_lang
    t = get_translation(user_lang)  # update terjemahan untuk pesan error
    
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown(f'<div class="typing-wrap"><div class="typing-top"><div class="typing-dots"><span></span><span></span><span></span></div><span class="typing-main">{t["analyzing"]}</span></div><div class="typing-sub">{t["analyzing_sub"]}</div></div>', unsafe_allow_html=True)
        result = extract_skills_groq(prompt)
        placeholder.empty()
        
        if isinstance(result, dict) and "error" in result:
            resp = f"**Error**: {result['error']}"
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp, "type": "text"})
        elif not result:
            error_msg = t["error_not_job"]
            st.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg, "type": "text"})
        else:
            st.markdown(render_skill_cards(result, user_lang), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "skills": result, "type": "skills"})
    
    st.rerun()

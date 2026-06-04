
import streamlit as st
import requests
import json
import os

OLLAMA_URL   = os.getenv("OLLAMA_URL",   "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

st.set_page_config(page_title="SkillMatch", page_icon="○", layout="centered", initial_sidebar_state="collapsed")

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


SYSTEM_PROMPT = (
    "Kamu adalah AI yang mengekstrak skill teknis dan non-teknis dari deskripsi pekerjaan.\n"
    "Output kamu HARUS berupa JSON array saja, tanpa teks lain, tanpa markdown backtick.\n"
    'Format: [{"skill": "Nama Skill", "confidence": 85}, ...]\n'
    "- confidence: integer 1-100 seberapa penting skill tersebut.\n"
    "- Ekstrak maksimal 12 skill paling relevan berdasarkan isi deskripsi.\n"
    "- Tulis nama skill dalam bahasa Inggris.\n"
    "- Jika teks bukan deskripsi pekerjaan, balas dengan array kosong [].\n"
    "- Hanya JSON murni, tanpa komentar atau penjelasan apapun."
)


def extract_skills_ollama(job_description):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Deskripsi pekerjaan berikut:\n\n" + job_description}
        ],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": -1}
    }
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=300)
        resp.raise_for_status()
        raw = resp.json()["message"]["content"].strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        skills = json.loads(raw)
        if not isinstance(skills, list):
            return []
        return [
            {"skill": str(i["skill"]), "confidence": round(float(i["confidence"]), 1)}
            for i in skills if "skill" in i and "confidence" in i
        ]
    except requests.exceptions.ConnectionError:
        return {"error": "Ollama server tidak dapat dijangkau. Pastikan sel Ollama sudah dijalankan."}
    except json.JSONDecodeError:
        return {"error": "Model mengembalikan format yang tidak valid. Coba jalankan ulang."}
    except Exception as e:
        return {"error": str(e)}


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


st.markdown('''<div class="hero">
  <div class="hero-label">AI-Powered Career Tool</div>
  <h1>Temukan skill yang kamu<br>butuhkan, <em>sekarang.</em></h1>
  <p class="hero-sub">Paste deskripsi pekerjaan dari lowongan manapun, dan kami akan menganalisis skill apa saja yang paling dibutuhkan untuk posisi tersebut.</p>
</div>''', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Halo! Tempel deskripsi pekerjaan dari lowongan yang kamu incar, dan saya akan menganalisis skill apa saja yang dibutuhkan.",
        "type": "text"
    }]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "skills":
            st.markdown(render_skill_cards(msg["skills"]), unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

if prompt := st.chat_input("Tempel deskripsi pekerjaan di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        if len(prompt.strip()) < 20:
            resp = "Deskripsi terlalu singkat. Coba salin keseluruhan deskripsi pekerjaan dari halaman lowongan."
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp, "type": "text"})
        else:
            placeholder = st.empty()
            placeholder.markdown('<div class="typing-wrap"><div class="typing-top"><div class="typing-dots"><span></span><span></span><span></span></div><span class="typing-main">Menganalisis...</span></div><div class="typing-sub">Membaca dan mengekstrak skill yang relevan.</div></div>', unsafe_allow_html=True)
            result = extract_skills_ollama(prompt)
            placeholder.empty()
            if isinstance(result, dict) and "error" in result:
                resp = f"**Error**: {result['error']}"
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp, "type": "text"})
            elif not result:
                resp = "Teks yang kamu masukkan sepertinya bukan deskripsi pekerjaan. Coba salin dari LinkedIn, Jobstreet, atau Glints."
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp, "type": "text"})
            else:
                st.markdown(render_skill_cards(result), unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "skills": result, "type": "skills"})

st.markdown(f'<div class="footer-bar"><span>Ollama · {OLLAMA_MODEL}</span><span>Ctrl+Enter untuk kirim</span></div>', unsafe_allow_html=True)

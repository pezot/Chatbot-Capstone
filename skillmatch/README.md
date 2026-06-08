# SkillMatch

AI-powered job skill extractor built with Streamlit + Groq (LLaMA 3.1).
Paste any job description and get the must-have skills with confidence scores.

Available in two themes — same functionality, different vibes.

---

## 🗂️ Repo Structure

```
skillmatch/
├── dark/
│   ├── app.py
│   └── .streamlit/
│       └── config.toml
├── light/
│   ├── app.py
│   └── .streamlit/
│       └── config.toml
└── README.md
```

---

## 🚀 Deploy to Streamlit Cloud

Each theme is a **separate Streamlit app** pointing to a different folder in this repo.

### Dark Theme
| Field | Value |
|---|---|
| Repository | `your-username/skillmatch` |
| Branch | `main` |
| Main file path | `dark/app.py` |

### Light Theme
| Field | Value |
|---|---|
| Repository | `your-username/skillmatch` |
| Branch | `main` |
| Main file path | `light/app.py` |

> On Streamlit Cloud → **New app** → pick repo → set **Main file path** accordingly.
> The `.streamlit/config.toml` inside each folder is picked up automatically.

---

## 🔑 Secrets

Add this in **Streamlit Cloud → App settings → Secrets** for **each** deployed app:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

Get a free API key at [console.groq.com](https://console.groq.com).

---

## 💻 Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/skillmatch.git
cd skillmatch

# Install dependencies
pip install streamlit groq langdetect

# Create secrets file (for whichever theme you want to run)
mkdir -p dark/.streamlit
echo 'GROQ_API_KEY = "your_key_here"' >> dark/.streamlit/secrets.toml

# Run dark theme
streamlit run dark/app.py

# Run light theme
streamlit run light/app.py
```

---

## ✨ Features

- Extracts up to 12 skills from any job description
- Confidence score per skill (High / Medium / Low)
- Auto-detects Indonesian and English input
- Rejects non-job-related queries
- Zero dependencies beyond `streamlit`, `groq`, `langdetect`


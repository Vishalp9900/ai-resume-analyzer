# AI Resume Analyzer 🤖
**Built by Vishal Patil** | Python + Flask + Scikit-learn + spaCy

Analyzes resumes for ATS compatibility, keyword gaps, and JD match score.

---

## 🚀 Run Locally

```bash
# 1. Clone & enter project
git clone https://github.com/vishalp9900/ai-resume-analyzer
cd ai-resume-analyzer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 4. Run
python app.py
# Open http://localhost:5000
```

---

## ☁️ Deploy on Render (Free)

1. Push code to GitHub
2. Go to https://render.com → New Web Service
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command:** `gunicorn app:app`
5. Click Deploy ✅

---

## ☁️ Deploy on Railway (Free)

1. Go to https://railway.app → New Project → Deploy from GitHub
2. Add environment variable: `PORT=5000`
3. Railway auto-detects Flask and deploys ✅

---

## 📁 Project Structure

```
ai-resume-analyzer/
├── app.py              # Flask routes
├── analyzer.py         # ATS scoring engine
├── requirements.txt
├── templates/
│   └── index.html      # Frontend UI
└── uploads/            # Temp resume storage
```

---

## ⚙️ Features
- Upload PDF resume → instant ATS score (0–100)
- Category breakdown (AI/ML, Tools, Databases, etc.)
- Missing keyword detection
- Job Description match % (TF-IDF cosine similarity)
- Red flag detection
- Actionable improvement tips

import re
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── keyword bank ────────────────────────────────────────────────────────────
CATEGORIES = {
    "AI / Machine Learning": {
        "keywords": [
            "machine learning", "deep learning", "neural network", "nlp",
            "natural language processing", "data preprocessing", "feature engineering",
            "model training", "model deployment", "scikit-learn", "tensorflow",
            "pytorch", "keras", "pandas", "numpy", "data visualization",
            "supervised learning", "unsupervised learning", "regression",
            "classification", "clustering", "computer vision", "reinforcement learning",
            "xgboost", "random forest", "decision tree", "cross validation",
        ],
        "weight": 35,
    },
    "Programming & Tools": {
        "keywords": [
            "python", "sql", "git", "github", "jupyter", "linux", "rest api",
            "django", "flask", "docker", "aws", "azure", "agile", "java",
            "c++", "api", "javascript", "html", "css", "vercel",
        ],
        "weight": 25,
    },
    "Data & Databases": {
        "keywords": [
            "mysql", "mongodb", "postgresql", "data analysis", "etl",
            "data pipeline", "database", "sql query",
        ],
        "weight": 15,
    },
    "Action Verbs & Impact": {
        "keywords": [
            "developed", "built", "designed", "implemented", "optimized",
            "collaborated", "analyzed", "deployed", "trained", "evaluated",
            "created", "managed", "automated", "integrated", "architected",
        ],
        "weight": 10,
    },
    "Resume Structure": {
        "keywords": [
            "summary", "education", "experience", "skills", "projects",
            "certifications", "internship", "cgpa", "percentage",
        ],
        "weight": 15,
    },
}

# ATS red flags
RED_FLAGS = [
    ("No quantified achievements", lambda t: not bool(re.search(r'\d+\s*%|\d+\s*x|\d+\s*users|\d+\+', t))),
    ("Missing LinkedIn URL",       lambda t: "linkedin" not in t.lower()),
    ("Missing GitHub URL",         lambda t: "github" not in t.lower()),
    ("Uses tables/columns (ATS risk)", lambda t: False),   # can't detect from text
    ("No professional summary",    lambda t: "summary" not in t.lower() and "objective" not in t.lower()),
]

TIPS = {
    "tensorflow":  "Add: 'Familiar with TensorFlow/Keras for building neural networks'",
    "pytorch":     "Add PyTorch to skills — most ML JDs list it",
    "docker":      "Add: 'Containerized apps using Docker' — very common in JDs",
    "nlp":         "AI Resume Analyzer project uses spaCy — mention NLP explicitly",
    "regression":  "Mention regression/classification in IIT Guwahati internship bullets",
    "data analysis": "Replace 'data preprocessing' with 'data analysis & preprocessing'",
    "aws":         "Add: 'Familiar with AWS/cloud deployment basics'",
    "flask":       "Your AI Resume Analyzer uses Flask — add it to skills",
    "postgresql":  "Add PostgreSQL to databases section",
    "agile":       "Add: 'Worked in Agile development environment'",
}

# ── helpers ─────────────────────────────────────────────────────────────────
def extract_text(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text

def keyword_score(text: str) -> dict:
    lower = text.lower()
    total_score = 0
    breakdown = {}

    for cat, data in CATEGORIES.items():
        found   = [k for k in data["keywords"] if k in lower]
        missing = [k for k in data["keywords"] if k not in lower]
        pct     = len(found) / len(data["keywords"]) if data["keywords"] else 0
        pts     = round(pct * data["weight"], 1)
        total_score += pts
        breakdown[cat] = {
            "found":   found,
            "missing": missing,
            "score":   pts,
            "max":     data["weight"],
            "pct":     round(pct * 100),
        }

    return {"total": round(total_score), "breakdown": breakdown}

def jd_similarity(resume_text: str, jd_text: str) -> int:
    if not jd_text.strip():
        return -1
    vec = TfidfVectorizer(stop_words="english")
    tfidf = vec.fit_transform([resume_text, jd_text])
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(sim * 100)

def red_flag_check(text: str) -> list:
    flags = []
    for label, fn in RED_FLAGS:
        try:
            if fn(text):
                flags.append(label)
        except Exception:
            pass
    return flags

def get_tips(missing_all: list) -> list:
    tips = []
    for kw in missing_all:
        if kw in TIPS:
            tips.append(TIPS[kw])
    return tips if tips else ["Keep improving keyword density with real project experience."]

# ── main entry ───────────────────────────────────────────────────────────────
def analyze_resume(pdf_path: str, jd_text: str = "") -> dict:
    text = extract_text(pdf_path)
    scores = keyword_score(text)
    jd_sim = jd_similarity(text, jd_text)
    flags  = red_flag_check(text)

    all_missing = []
    for cat_data in scores["breakdown"].values():
        all_missing.extend(cat_data["missing"])

    tips = get_tips(all_missing)

    grade = "A" if scores["total"] >= 80 else \
            "B" if scores["total"] >= 65 else \
            "C" if scores["total"] >= 50 else "D"

    return {
        "ats_score":      scores["total"],
        "grade":          grade,
        "breakdown":      scores["breakdown"],
        "jd_similarity":  jd_sim,
        "red_flags":      flags,
        "missing_top":    all_missing[:12],
        "tips":           tips,
        "word_count":     len(text.split()),
        "char_count":     len(text),
    }

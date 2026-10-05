import streamlit as st
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page setup
st.set_page_config(page_title="HireSense", page_icon="🤖")
st.title("🤖 HireSense - AI Resume Screener")
st.write("TCS iON inspired | Built for TCS Interview")

# Skill list
SKILLS = ["python", "java", "sql", "aws", "react", "javascript", "docker", "c++", "html", "css", "node.js", "machine learning", "excel"]

# Function 1: PDF theke text ber kora
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()

# Function 2: Skill khuje ber kora
def extract_skills(text):
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)
    return found

# --- UI Part ---
st.divider()
jd_input = st.text_area("STEP 1: Job Description Likho", placeholder="Example: We need Python developer with SQL and AWS knowledge", height=120)

uploaded_files = st.file_uploader("STEP 2: Resume PDF Upload Koro", type="pdf", accept_multiple_files=True)

if st.button("STEP 3: Score Dekho 🚀"):
    if not jd_input or not uploaded_files:
        st.error("Age JD likho ar Resume upload koro!")
    else:
        results = []
        for resume_file in uploaded_files:
            resume_text = extract_text_from_pdf(resume_file)
            skills = extract_skills(resume_text)

            # AI Logic: TF-IDF + Cosine Similarity
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([jd_input.lower(), resume_text])
            score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100

            results.append({
                "Resume": resume_file.name,
                "Score %": round(score, 2),
                "Matched Skills": ", ".join(skills) if skills else "No match",
            })

        # Score onujayi sajano
        results = sorted(results, key=lambda x: x["Score %"], reverse=True)

        st.success("Result Ready!")
        st.table(results)
        st.balloons()
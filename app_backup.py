
import streamlit as st
from pypdf import PdfReader
import pandas as pd
import re
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ResumeAI | UAE Career Assistant",
    page_icon="📄",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "resume_uploads" not in st.session_state:
    st.session_state.resume_uploads = 0

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #F5F7FB;
}

[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

[data-testid="stSidebar"] h1 {
    color: #17365D;
    font-size: 27px;
}

.main-title {
    color: #17365D;
    font-size: 32px;
    font-weight: 750;
    margin-bottom: 5px;
}

.subtitle {
    color: #718096;
    font-size: 15px;
    margin-bottom: 25px;
}

.stat-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 18px 14px;
    min-height: 115px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.03);
}

.stat-label {
    color: #64748B;
    font-size: 13px;
}

.stat-value {
    color: #17365D;
    font-size: 27px;
    font-weight: 700;
    margin-top: 8px;
}

.section-title {
    color: #17365D;
    font-size: 21px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 12px;
}

.info-card {
    background: white;
    padding: 20px;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    min-height: 150px;
}

div.stButton > button {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 7px;
    padding: 12px 22px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #1D4ED8;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("📄 ResumeAI")
    st.caption("Smart Resume Analysis")

    st.divider()

    st.subheader("Navigation")

    page = st.radio(
        "Go to",
        [
            "🏠 Dashboard",
            "📊 Resume Analysis",
            "💡 Improvement Tips",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("Designed for UAE Job Seekers")
    st.caption("Dubai | Abu Dhabi | UAE")

# ---------------- MAIN DASHBOARD ----------------
st.markdown(
    '<div class="main-title">Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Welcome to your AI-powered resume analysis platform.</div>',
    unsafe_allow_html=True
)

# ---------------- STATISTICS ----------------
c1, c2, c3, c4, c5 = st.columns(5)

stats = [
    ("Documents", str(st.session_state.resume_uploads)),
    ("ATS Match", "—"),
    ("Skills Matched", "—"),
    ("Missing Skills", "—"),
    ("Processing Time", "—")
]

for col, (label, value) in zip(
    [c1, c2, c3, c4, c5], stats
):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ---------------- ATS PERFORMANCE ----------------
st.markdown(
    '<div class="section-title">ATS Performance</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-card">
    <h4 style="color:#17365D;">Resume Matching Trends</h4>
    <p style="color:#718096;">
        Your ATS performance chart will appear here
        after your first successful resume analysis.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- LOWER ANALYTICS ----------------
left, right = st.columns(2)

with left:
    st.markdown(
        '<div class="section-title">Skills Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <h4 style="color:#17365D;">Matched vs Missing Skills</h4>
        <p style="color:#718096;">
            Your skills comparison will appear here
            after resume analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(
        '<div class="section-title">Resume Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <h4 style="color:#17365D;">Resume Insights</h4>
        <p style="color:#718096;">
            Your resume insights will appear here
            after resume analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# ---------------- RESUME UPLOAD ----------------
st.markdown(
    '<div class="section-title">📄 Upload Your Resume</div>',
    unsafe_allow_html=True
)

resume = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)

st.write("")

# ---------------- JOB DESCRIPTION ----------------
st.markdown(
    '<div class="section-title">💼 Job Description</div>',
    unsafe_allow_html=True
)

job_description = st.text_area(
    "Paste the target job description",
    placeholder="Paste your target Dubai job description here...",
    height=180,
    label_visibility="collapsed"
)

st.write("")


# ---------------- ANALYZE BUTTON ----------------
if st.button("Analyze My Resume"):

    if resume is None:
        st.warning("Please upload your resume first.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            start_time = time.perf_counter()

            pdf_reader = PdfReader(resume)

            extracted_text = ""

            for page_content in pdf_reader.pages:
                extracted_text += (
                    page_content.extract_text() or ""
                )

            if not extracted_text.strip():
                st.error("No readable text found in this PDF.")

            else:
                # STEP 1: Text preprocessing
                resume_clean = extracted_text.lower()
                job_clean = job_description.lower()

                # STEP 2: TF-IDF and Cosine Similarity
                vectorizer = TfidfVectorizer(
                    stop_words="english",
                    ngram_range=(1, 2)
                )

                tfidf_matrix = vectorizer.fit_transform(
                    [resume_clean, job_clean]
                )

                similarity = cosine_similarity(
                    tfidf_matrix[0:1],
                    tfidf_matrix[1:2]
                )[0][0]

                match_score = round(similarity * 100, 2)

                # STEP 3: Skill extraction
                skill_database = [
                    "Python",
                    "Machine Learning",
                    "Deep Learning",
                    "Artificial Intelligence",
                    "Natural Language Processing",
                    "NLP",
                    "Computer Vision",
                    "NumPy",
                    "Pandas",
                    "Scikit-learn",
                    "TensorFlow",
                    "PyTorch",
                    "SQL",
                    "Data Analysis",
                    "Streamlit",
                    "Flask",
                    "FastAPI",
                    "Java",
                    "JavaScript",
                    "HTML",
                    "CSS",
                    "Git",
                    "Docker",
                    "AWS",
                    "Azure",
                    "Power BI",
                    "Excel",
                    "Data Science"
                ]

                # Skills present in job description
                required_skills = []

                for skill in skill_database:
                    pattern = (
                        r"(?<!\w)"
                        + re.escape(skill.lower())
                        + r"(?!\w)"
                    )

                    if re.search(pattern, job_clean):
                        required_skills.append(skill)

                # Matched and missing skills
                matched_skills = []
                missing_skills = []

                for skill in required_skills:
                    pattern = (
                        r"(?<!\w)"
                        + re.escape(skill.lower())
                        + r"(?!\w)"
                    )

                    if re.search(pattern, resume_clean):
                        matched_skills.append(skill)
                    else:
                        missing_skills.append(skill)

                # STEP 4: Processing time
                processing_time = round(
                    time.perf_counter() - start_time, 2
                )

                # Save extracted resume
                st.session_state.resume_text = extracted_text
                st.session_state.resume_uploads += 1

                # ---------------- RESULTS ----------------
                st.divider()

                st.markdown("## 📊 Resume Analysis Results")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Estimated Match Score",
                        f"{match_score}%"
                    )

                with col2:
                    st.metric(
                        "Matched Skills",
                        len(matched_skills)
                    )

                with col3:
                    st.metric(
                        "Missing Skills",
                        len(missing_skills)
                    )

                st.progress(match_score / 100)

                st.caption(
                    "This is a text similarity estimate, "
                    "not an official employer ATS score."
                )

                st.caption(
                    f"Processing Time: {processing_time} seconds"
                )

                # Matched skills
                st.markdown("### ✅ Matched Skills")

                if matched_skills:
                    st.success(
                        ", ".join(matched_skills)
                    )
                else:
                    st.info("No matching skills detected.")

                # Missing skills
                st.markdown("### ❌ Missing Skills")

                if missing_skills:
                    st.warning(
                        ", ".join(missing_skills)
                    )
                else:
                    st.success(
                        "All detected job description skills "
                        "were found in the resume."
                    )

                # Suggestions
                st.markdown("### 💡 Resume Improvement Suggestions")

                if missing_skills:
                    for skill in missing_skills:
                        st.write(
                            f"- Review the {skill} requirement. "
                            "If you genuinely have this skill, "
                            "include relevant evidence in your resume."
                        )
                else:
                    st.success(
                        "Your resume contains all skills "
                        "detected from this job description."
                    )

                # Extracted text
                with st.expander("View Extracted Resume Text"):
                    st.write(extracted_text)

        except Exception as error:
            st.error(f"Unable to analyze resume: {error}")



# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "ResumeAI | AI Resume & ATS Checker | Built with Python and Streamlit"
)

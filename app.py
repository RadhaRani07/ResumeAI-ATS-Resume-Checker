import streamlit as st
from pypdf import PdfReader
import re
import time
import pandas as pd

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from xml.sax.saxutils import escape

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------- LEARNING RESOURCES ----------------

learning_resources = {
    "Python": "Python fundamentals and programming practice",
    "Machine Learning": "ML algorithms and practical projects",
    "Deep Learning": "Neural networks and deep learning basics",
    "TensorFlow": "TensorFlow model building practice",
    "PyTorch": "PyTorch and neural network implementation",
    "SQL": "SQL queries and database fundamentals",
    "NumPy": "NumPy arrays and numerical computing",
    "Pandas": "Data cleaning and data manipulation",
    "Computer Vision": "Image processing and computer vision basics",
    "OpenCV": "OpenCV image processing projects",
    "Generative AI": "Generative AI concepts and applications",
    "Large Language Models": "LLM fundamentals and applications",
    "Prompt Engineering": "Prompt design and evaluation",
    "Docker": "Docker fundamentals and containerization",
    "AWS": "Cloud computing and AWS fundamentals",
    "Natural Language Processing": "NLP concepts and text processing projects",
    "Scikit-learn": "Machine learning workflows and model evaluation",
    "Keras": "Building neural networks with Keras",
    "Hugging Face": "Using pretrained models and Transformers",
    "LangChain": "Building applications with language models",
    "YOLO": "Object detection concepts and projects",
    "Image Processing": "Image processing fundamentals and practice",
    "CNN": "Convolutional neural networks and image classification",
    "Statistics": "Statistics and probability fundamentals",
    "Data Analysis": "Data analysis and practical datasets",
    "Matplotlib": "Data visualization with Matplotlib",
    "Seaborn": "Statistical data visualization",
    "Git": "Version control with Git",
    "GitHub": "GitHub repositories and collaboration",
    "REST API": "REST API fundamentals and practice",
    "Flask": "Building web applications with Flask",
    "FastAPI": "Building APIs with FastAPI",
    "Linux": "Linux commands and fundamentals",
    "Azure": "Cloud computing and Azure fundamentals",
    "Google Cloud": "Google Cloud fundamentals",
    "MySQL": "Relational databases and SQL practice",
    "MongoDB": "NoSQL database fundamentals"
}


# ---------------- PDF REPORT ----------------

def create_pdf_report(data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#17365D"),
        fontSize=24,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#2563EB"),
        fontSize=14,
        spaceBefore=14,
        spaceAfter=8
    )

    story = []

    story.append(Paragraph("ResumeAI", title_style))
    story.append(Paragraph("Resume Analysis Report", styles["Heading2"]))
    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Target Job Role: {escape(str(data['job_role']))}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    score_data = [
        ["ESTIMATED MATCH SCORE", f"{data['match_score']}%"],
        ["Matched Skills", str(len(data["matched_skills"]))],
        ["Missing Skills", str(len(data["missing_skills"]))],
        ["Processing Time", f"{data['processing_time']} seconds"]
    ]

    score_table = Table(score_data, colWidths=[300, 150])

    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#EFF6FF")),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#1E293B")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))

    story.append(score_table)

    story.append(Paragraph("Matched Skills", heading_style))
    story.append(
        Paragraph(
            ", ".join(escape(str(skill)) for skill in data["matched_skills"])
            or "None detected",
            styles["Normal"]
        )
    )

    story.append(Paragraph("Missing Skills", heading_style))
    story.append(
        Paragraph(
            ", ".join(escape(str(skill)) for skill in data["missing_skills"])
            or "None detected",
            styles["Normal"]
        )
    )

    story.append(Paragraph("Improvement Suggestions", heading_style))

    for skill in data["missing_skills"]:
        story.append(
            Paragraph(
                f"Review the {escape(str(skill))} requirement. "
                "If you genuinely have this skill, include relevant "
                "evidence in your resume.",
                styles["Normal"]
            )
        )
        story.append(Spacer(1, 6))

    if not data["missing_skills"]:
        story.append(
            Paragraph(
                "No missing skills were detected from the starter skill list.",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Note: This match percentage is a text-similarity estimate, "
            "not an official employer ATS score or hiring decision.",
            styles["Italic"]
        )
    )

    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()


# ---------------- LEARNING ROADMAP PDF ----------------

def create_roadmap_pdf(latest):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        "RoadmapTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#17365D"),
        fontSize=22,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "RoadmapHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#2563EB"),
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8
    )

    story.append(
        Paragraph("ResumeAI", title_style)
    )

    story.append(
        Paragraph(
            "Personalized Learning Roadmap",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"Target Job Role: {escape(str(latest['job_role']))}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph("Skills to Learn", heading_style)
    )

    if latest["missing_skills"]:

        for skill in latest["missing_skills"]:

            topic = learning_resources.get(
                skill,
                f"{skill} fundamentals and practical projects"
            )

            story.append(
                Paragraph(
                    escape(str(skill)),
                    styles["Heading3"]
                )
            )

            story.append(
                Paragraph(
                    f"Learning Focus: {escape(str(topic))}",
                    styles["BodyText"]
                )
            )

            story.append(Spacer(1, 12))

    else:

        story.append(
            Paragraph(
                "No missing skills detected. Keep improving your existing skills!",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Tip: Learn the topics step by step and practise them through "
            "small projects. Add a skill to your resume only when you can "
            "demonstrate it.",
            styles["Italic"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ResumeAI | Resume Assistant",
    page_icon="📄",
    layout="wide"
)


# ---------------- SESSION STATE ----------------

if "resume_uploads" not in st.session_state:
    st.session_state.resume_uploads = 0

if "latest_analysis" not in st.session_state:
    st.session_state.latest_analysis = None

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []


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


# ---------------- LATEST RESULT ----------------

latest = st.session_state.latest_analysis


# ---------------- DASHBOARD ----------------

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Welcome to your AI-powered resume analysis platform.</div>',
        unsafe_allow_html=True
    )

    if latest:

        ats_value = f'{latest["match_score"]}%'
        matched_value = str(len(latest["matched_skills"]))
        missing_value = str(len(latest["missing_skills"]))
        time_value = f'{latest["processing_time"]} sec'

    else:

        ats_value = "—"
        matched_value = "—"
        missing_value = "—"
        time_value = "—"

    c1, c2, c3, c4, c5 = st.columns(5)

    stats = [
        ("Documents", str(st.session_state.resume_uploads)),
        ("ATS Match", ats_value),
        ("Skills Matched", matched_value),
        ("Missing Skills", missing_value),
        ("Processing Time", time_value)
    ]

    for col, (label, value) in zip([c1, c2, c3, c4, c5], stats):

        with col:

            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">{label}</div>
                <div class="stat-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    st.markdown(
        '<div class="section-title">ATS Performance</div>',
        unsafe_allow_html=True
    )

    if latest:

        st.markdown(
            '<div class="info-card"><h4 style="color:#17365D;">Resume Matching Trends</h4></div>',
            unsafe_allow_html=True
        )

        history_df = pd.DataFrame(st.session_state.analysis_history)

        if not history_df.empty:

            chart_df = history_df[
                ["Analysis", "Match Score"]
            ].set_index("Analysis")

            st.line_chart(chart_df)

    else:

        st.markdown("""
        <div class="info-card">
            <h4 style="color:#17365D;">Resume Matching Trends</h4>
            <p style="color:#718096;">
                Your ATS performance chart will appear here after your first successful resume analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">Skills Analysis</div>',
            unsafe_allow_html=True
        )

        if latest:

            st.markdown(
                '<div class="info-card"><h4 style="color:#17365D;">Matched vs Missing Skills</h4></div>',
                unsafe_allow_html=True
            )

            skills_df = pd.DataFrame({
                "Skill Status": ["Matched", "Missing"],
                "Count": [
                    len(latest["matched_skills"]),
                    len(latest["missing_skills"])
                ]
            }).set_index("Skill Status")

            st.bar_chart(skills_df)

        else:

            st.markdown("""
            <div class="info-card">
                <h4 style="color:#17365D;">Matched vs Missing Skills</h4>
                <p style="color:#718096;">
                    Your skills comparison will appear here after resume analysis.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with right:

        st.markdown(
            '<div class="section-title">Resume Analytics</div>',
            unsafe_allow_html=True
        )

        if latest:

            st.markdown("""
            <div class="info-card">
                <h4 style="color:#17365D;">Resume Insights</h4>
            </div>
            """, unsafe_allow_html=True)

            st.write(
                f'Latest estimated match: **{latest["match_score"]}%**'
            )

            st.write(
                f'Job skills detected: **{len(latest["matched_skills"]) + len(latest["missing_skills"])}**'
            )

            st.write("Resume text extracted: **Yes**")

        else:

            st.markdown("""
            <div class="info-card">
                <h4 style="color:#17365D;">Resume Insights</h4>
                <p style="color:#718096;">
                    Your resume insights will appear here after resume analysis.
                </p>
            </div>
            """, unsafe_allow_html=True)


# ---------------- RESUME ANALYSIS PAGE ----------------

elif page == "📊 Resume Analysis":

    st.markdown(
        '<div class="main-title">Resume Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Compare your resume with a target job description.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">📄 Upload Your Resume</div>',
        unsafe_allow_html=True
    )

    resume = st.file_uploader(
        "Upload your resume in PDF format",
        type=["pdf"],
        key="resume_pdf_upload"
    )

    st.write("")

    st.markdown(
        '<div class="section-title">💼 Job Description</div>',
        unsafe_allow_html=True
    )

    st.subheader("Select Your Target Job Role")

    job_role = st.selectbox(
        "Choose your job role",
        [
            "AI/ML Engineer",
            "Machine Learning Engineer",
            "Data Scientist",
            "Python Developer",
            "Data Analyst",
            "Computer Vision Engineer",
            "Generative AI Engineer"
        ]
    )

    job_description = st.text_area(
        "Paste the target job description",
        placeholder="Paste your target job description here...",
        height=180,
        label_visibility="collapsed"
    )

    st.write("")

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

                    extracted_text += page_content.extract_text() or ""

                if not extracted_text.strip():

                    st.error("No readable text found in this PDF.")

                else:

                    resume_clean = extracted_text.lower()
                    job_clean = job_description.lower()

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

                    if match_score >= 75:

                        resume_strength = "Strong"

                    elif match_score >= 50:

                        resume_strength = "Moderate"

                    else:

                        resume_strength = "Needs Improvement"

                    # SKILL DATABASE

                    skill_database = {

                        "Python": ["python"],
                        "Java": ["java"],
                        "JavaScript": ["javascript"],
                        "SQL": ["sql"],
                        "HTML": ["html"],
                        "CSS": ["css"],

                        "Artificial Intelligence": [
                            "artificial intelligence", "ai"
                        ],

                        "Machine Learning": [
                            "machine learning", "ml"
                        ],

                        "Deep Learning": ["deep learning"],

                        "Generative AI": [
                            "generative ai", "gen ai"
                        ],

                        "Natural Language Processing": [
                            "natural language processing", "nlp"
                        ],

                        "Large Language Models": [
                            "large language models", "llm", "llms"
                        ],

                        "Prompt Engineering": [
                            "prompt engineering"
                        ],

                        "Retrieval Augmented Generation": [
                            "retrieval augmented generation", "rag"
                        ],

                        "XGBoost": ["xgboost"],
                        "Model Evaluation": ["model evaluation"],
                        "Feature Engineering": ["feature engineering"],
                        "MLOps": ["mlops"],

                        "Computer Vision": ["computer vision"],
                        "OpenCV": ["opencv"],
                        "YOLO": ["yolo"],
                        "Image Processing": ["image processing"],

                        "CNN": [
                            "cnn", "convolutional neural network"
                        ],

                        "Scikit-learn": [
                            "scikit-learn", "sklearn"
                        ],

                        "TensorFlow": ["tensorflow"],
                        "PyTorch": ["pytorch"],
                        "Keras": ["keras"],

                        "Hugging Face": [
                            "hugging face", "huggingface"
                        ],

                        "LangChain": ["langchain"],
                        "NumPy": ["numpy"],
                        "Pandas": ["pandas"],
                        "SciPy": ["scipy"],

                        "Data Analysis": ["data analysis"],
                        "Data Science": ["data science"],
                        "Statistics": ["statistics"],
                        "Matplotlib": ["matplotlib"],
                        "Seaborn": ["seaborn"],
                        "Power BI": ["power bi"],
                        "Tableau": ["tableau"],
                        "Excel": ["excel"],
                        "PySpark": ["pyspark"],
                        "Apache Spark": ["apache spark"],

                        "Streamlit": ["streamlit"],
                        "Flask": ["flask"],
                        "FastAPI": ["fastapi"],

                        "REST API": [
                            "rest api", "restful api"
                        ],

                        "Git": ["git"],
                        "GitHub": ["github"],
                        "Docker": ["docker"],
                        "Kubernetes": ["kubernetes"],
                        "Linux": ["linux"],
                        "CI/CD": ["ci/cd"],

                        "AWS": [
                            "aws", "amazon web services"
                        ],

                        "Azure": ["azure"],

                        "Google Cloud": [
                            "google cloud", "gcp"
                        ],

                        "MySQL": ["mysql"],
                        "PostgreSQL": ["postgresql"],
                        "MongoDB": ["mongodb"]
                    }

                    # ROLE SKILL DATABASE

                    role_skill_database = {

                        "AI/ML Engineer": [
                            "Python", "Machine Learning", "Deep Learning",
                            "Artificial Intelligence", "Scikit-learn",
                            "TensorFlow", "PyTorch", "SQL", "NumPy", "Pandas"
                        ],

                        "Machine Learning Engineer": [
                            "Python", "Machine Learning", "Deep Learning",
                            "Scikit-learn", "TensorFlow", "PyTorch",
                            "XGBoost", "Feature Engineering", "Model Evaluation"
                        ],

                        "Data Scientist": [
                            "Python", "SQL", "Statistics", "Data Analysis",
                            "Pandas", "NumPy", "Scikit-learn",
                            "Matplotlib", "Seaborn", "Machine Learning"
                        ],

                        "Python Developer": [
                            "Python", "SQL", "Git", "REST API",
                            "Flask", "FastAPI", "Docker", "Linux"
                        ],

                        "Data Analyst": [
                            "SQL", "Excel", "Power BI", "Tableau",
                            "Python", "Pandas", "Statistics", "Data Analysis"
                        ],

                        "Computer Vision Engineer": [
                            "Python", "Computer Vision", "OpenCV", "YOLO",
                            "Image Processing", "CNN", "PyTorch", "TensorFlow"
                        ],

                        "Generative AI Engineer": [
                            "Python", "Generative AI", "Large Language Models",
                            "Prompt Engineering", "Retrieval Augmented Generation",
                            "Hugging Face", "LangChain", "REST API", "Docker"
                        ]
                    }

                    # SKILL CATEGORIES

                    skill_categories = {

                        "Programming": [
                            "Python", "Java", "JavaScript", "SQL", "HTML", "CSS"
                        ],

                        "AI & Machine Learning": [
                            "Artificial Intelligence", "Machine Learning",
                            "Deep Learning", "Generative AI",
                            "Natural Language Processing", "Large Language Models",
                            "Prompt Engineering", "Retrieval Augmented Generation",
                            "XGBoost", "Model Evaluation", "Feature Engineering", "MLOps"
                        ],

                        "Computer Vision": [
                            "Computer Vision", "OpenCV", "YOLO",
                            "Image Processing", "CNN"
                        ],

                        "Frameworks & Tools": [
                            "Scikit-learn", "TensorFlow", "PyTorch", "Keras",
                            "Hugging Face", "LangChain", "NumPy", "Pandas", "SciPy"
                        ],

                        "Data Analytics": [
                            "Data Analysis", "Data Science", "Statistics",
                            "Matplotlib", "Seaborn", "Power BI", "Tableau",
                            "Excel", "PySpark", "Apache Spark"
                        ],

                        "Development & Deployment": [
                            "Streamlit", "Flask", "FastAPI", "REST API",
                            "Git", "GitHub", "Docker", "Kubernetes",
                            "Linux", "CI/CD"
                        ],

                        "Cloud & Databases": [
                            "AWS", "Azure", "Google Cloud",
                            "MySQL", "PostgreSQL", "MongoDB"
                        ]
                    }

                    required_skills = []

                    role_skills = role_skill_database.get(job_role, [])

                    for skill in role_skills:

                        if skill not in required_skills:

                            required_skills.append(skill)

                    # DETECT SKILLS IN JOB DESCRIPTION

                    for skill, aliases in skill_database.items():

                        for alias in aliases:

                            pattern = (
                                r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"
                            )

                            if re.search(pattern, job_clean):

                                if skill not in required_skills:

                                    required_skills.append(skill)

                                break

                    matched_skills = []
                    missing_skills = []

                    # CHECK RESUME SKILLS

                    for skill in required_skills:

                        aliases = skill_database[skill]
                        found = False

                        for alias in aliases:

                            pattern = (
                                r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"
                            )

                            if re.search(pattern, resume_clean):

                                found = True
                                break

                        if found:

                            matched_skills.append(skill)

                        else:

                            missing_skills.append(skill)

                    # BUILD SKILL GAP ANALYSIS

                    skill_gap_analysis = {}

                    for category, skills in skill_categories.items():

                        category_missing = [
                            skill for skill in missing_skills
                            if skill in skills
                        ]

                        if category_missing:

                            skill_gap_analysis[category] = category_missing

                    processing_time = round(
                        time.perf_counter() - start_time, 2
                    )

                    # SAVE RESULT

                    st.session_state.resume_uploads += 1

                    analysis_number = (
                        len(st.session_state.analysis_history) + 1
                    )

                    result = {
                        "job_role": job_role,
                        "resume_strength": resume_strength,
                        "skill_gap_analysis": skill_gap_analysis,
                        "match_score": match_score,
                        "matched_skills": matched_skills,
                        "missing_skills": missing_skills,
                        "processing_time": processing_time,
                        "extracted_text": extracted_text,
                        "analysis_number": analysis_number
                    }

                    st.session_state.latest_analysis = result

                    st.session_state.analysis_history.append({
                        "Analysis": f"Run {analysis_number}",
                        "Match Score": match_score
                    })

                    st.success(
                        "Resume analyzed successfully! Open Dashboard to see updated statistics."
                    )

            except Exception as error:

                st.error(f"Unable to analyze resume: {error}")

    # DISPLAY ANALYSIS RESULTS

    latest = st.session_state.latest_analysis

    if latest:

        st.divider()

        st.markdown("## 📊 Resume Analysis Results")

        st.subheader("💪 Resume Strength")

        if latest["resume_strength"] == "Strong":

            st.success("Strong Resume")

        elif latest["resume_strength"] == "Moderate":

            st.info("Moderate Resume")

        else:

            st.warning("Needs Improvement")

        st.divider()

        st.subheader("🎯 Skill Gap Analysis")

        if latest["skill_gap_analysis"]:

            for category, skills in latest["skill_gap_analysis"].items():

                st.markdown(f"**{category}**")
                st.write(", ".join(skills))

        else:

            st.success("No skill gaps detected!")

        st.info(f"🎯 Target Job Role: {latest['job_role']}")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Estimated Match Score",
                f'{latest["match_score"]}%'
            )

        with col2:

            st.metric(
                "Matched Skills",
                len(latest["matched_skills"])
            )

        with col3:

            st.metric(
                "Missing Skills",
                len(latest["missing_skills"])
            )

        st.progress(
            max(0.0, min(1.0, latest["match_score"] / 100))
        )

        st.caption(
            "This is a text similarity estimate, not an official employer ATS score."
        )

        st.caption(
            f'Processing Time: {latest["processing_time"]} seconds'
        )

        st.markdown("### ✅ Matched Skills")

        if latest["matched_skills"]:

            st.success(", ".join(latest["matched_skills"]))

        else:

            st.info("No matching skills detected.")

        st.markdown("### ❌ Missing Skills")

        if latest["missing_skills"]:

            st.warning(", ".join(latest["missing_skills"]))

        else:

            st.success(
                "All detected job description skills were found in the resume."
            )

        st.markdown("### 💡 Resume Improvement Suggestions")

        if latest["missing_skills"]:

            for skill in latest["missing_skills"]:

                st.write(
                    f"- Review the {skill} requirement. "
                    "If you genuinely have this skill, "
                    "include relevant evidence in your resume."
                )

        else:

            st.success(
                "Your resume contains all skills detected from this job description."
            )

        with st.expander("View Extracted Resume Text"):

            st.write(latest["extracted_text"])

        st.download_button(
            label="📥 Download Analysis Report (PDF)",
            data=create_pdf_report(latest),
            file_name="ResumeAI_Analysis_Report.pdf",
            mime="application/pdf"
        )


# ---------------- IMPROVEMENT TIPS PAGE ----------------

elif page == "💡 Improvement Tips":

    st.markdown(
        '<div class="main-title">Improvement Tips</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Practical suggestions for job applications.</div>',
        unsafe_allow_html=True
    )

    latest = st.session_state.latest_analysis

    # DOWNLOAD LEARNING ROADMAP

    if latest:

        st.write("")

        st.download_button(
            label="📥 Download Learning Roadmap",
            data=create_roadmap_pdf(latest),
            file_name="ResumeAI_Learning_Roadmap.pdf",
            mime="application/pdf"
        )

    # SKILLS TO REVIEW

    if latest and latest["missing_skills"]:

        st.subheader("Skills to review")

        for skill in latest["missing_skills"]:

            st.write(
                f"- **{skill}:** If you have this skill, add a truthful example "
                "from a project, course, or work experience."
            )

    elif latest and not latest["missing_skills"]:

        st.success(
            "No missing skills detected from the current analysis."
        )

    else:

        st.info(
            "Run a resume analysis to receive skill-specific improvement tips."
        )

    # RESUME CHECKLIST

    st.divider()

    st.subheader("Resume Checklist")

    st.write("- Tailor your resume to each job description.")
    st.write("- Keep project descriptions clear and evidence-based.")
    st.write("- Include relevant technical skills only when you can demonstrate them.")
    st.write("- Check spelling, dates, links, and contact details before applying.")

    # PERSONALIZED LEARNING ROADMAP

    st.divider()

    st.subheader("📚 Personalized Learning Roadmap")

    if latest and latest["missing_skills"]:

        st.write(
            "Follow these learning topics to improve your missing skills:"
        )

        for skill in latest["missing_skills"]:

            topic = learning_resources.get(
                skill,
                f"{skill} fundamentals and practical projects"
            )

            st.markdown(f"**{skill}**")
            st.write(f"Learning focus: {topic}")

    elif latest and not latest["missing_skills"]:

        st.success(
            "No missing skills detected. Keep improving your existing skills!"
        )

    else:

        st.info(
            "Analyze your resume first to generate your personalized learning roadmap."
        )


# ---------------- SETTINGS PAGE ----------------

elif page == "⚙️ Settings":

    st.markdown(
        '<div class="main-title">Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Basic application information.</div>',
        unsafe_allow_html=True
    )

    st.write("**Application:** ResumeAI")

    st.write("**Focus:** Resume Analysis & Career Development")

    st.write(
        "**Analysis method:** TF-IDF text similarity and keyword matching"
    )

    st.caption(
        "The match percentage is an estimate for guidance, not a hiring decision "
        "or an official employer ATS score."
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "ResumeAI | AI Resume & ATS Checker | Built with Python and Streamlit"
)
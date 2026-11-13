# ResumeAI – ATS Resume Checker 🚀
(
## 🌐 Live Demo

🚀 **Try the Application:** [ResumeAI – ATS Resume Checker](https://resumeai-ats-resume-checker-qkmvvcpf2curlmycsfqx5w.streamlit.app/)
)
An AI-powered resume analysis application built with Python and Streamlit that helps job seekers evaluate their resumes against target job descriptions, identify skill gaps, and improve their job-readiness.

## 📌 Project Overview

ResumeAI is a resume analysis tool designed to help candidates understand how well their resumes align with a target job role.

It extracts text from PDF resumes, compares resume content with job descriptions using TF-IDF and Cosine Similarity, identifies matched and missing skills, and provides actionable improvement suggestions.

## ✨ Key Features

- **PDF Resume Upload:** Upload your resume in PDF format.
- **Job Description Matching:** Compare your resume against a target job description.
- **ATS Match Score:** Get an estimated resume-to-job similarity score.
- **Skills Analysis:** Identify matched skills and missing skills.
- **Skill Gap Analysis:** Understand which skills need improvement.
- **Interactive Dashboard:** View resume analysis statistics and performance charts.
- **Improvement Suggestions:** Get suggestions based on missing skills.
- **PDF Report Generation:** Download a resume analysis report.
- **Learning Roadmap:** Generate a PDF learning roadmap to support skill development.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data handling |
| Scikit-learn | TF-IDF and Cosine Similarity |
| PyPDF | PDF text extraction |
| ReportLab | PDF report generation |

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/RadhaRani07/ResumeAI-ATS-Resume-Checker.git
```

### 2. Navigate to the project directory

```bash
cd ResumeAI-ATS-Resume-Checker
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

Install all required packages using the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📂 Project Structure

```text
ResumeAI-ATS-Resume-Checker/
│
├── .streamlit/
│   └── config.toml
│
├── app.py
├── requirements.txt
├── README.md
└── app_backup.py
```

## 📊 How It Works

1. Upload your resume in PDF format.
2. Select your target job role and provide the job description.
3. The application extracts text from your resume.
4. TF-IDF and Cosine Similarity estimate the match between resume content and job requirements.
5. The application identifies matched and missing skills.
6. Review your analysis dashboard and improvement suggestions.
7. Download your PDF analysis report.

## ⚠️ Important Note

The ATS match score is an estimated text-similarity score. It is not an official ATS score, a guarantee of shortlisting, or a hiring decision.

## 🎯 Project Objective

The objective of ResumeAI is to make resume analysis more accessible and help job seekers identify skill gaps and improve their resumes through practical feedback.

## 👩‍💻 Author

**Radha Rani**

B.Tech Computer Science Engineering (AI & ML) Student

- GitHub: [RadhaRani07](https://github.com/RadhaRani07)

---

⭐ If you find this project useful, consider giving it a star!

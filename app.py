import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from auth import require_auth
from utils.styles import inject, hero, feature_cards, step_cards, section, divider

st.set_page_config(
    page_title="RecruitLens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

require_auth()
st.markdown(inject(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### RecruitLens")
    st.caption("From PDF to insight in seconds.")
    st.divider()
    st.markdown("**Supported formats**")
    st.markdown("- PDF (text & scanned via OCR)")
    st.markdown("- Word (.docx)")
    st.markdown("- Plain text (.txt)")
    st.markdown("- Rich Text (.rtf)")
    st.divider()
    st.markdown("**Pages**")
    st.markdown("1. **Parse Resume** — single CV + ATS score")
    st.markdown("2. **Batch Upload** — compare up to 10 CVs")
    st.markdown("3. **Demo** — sample dataset explorer")
    st.markdown("4. **JD Match** — resume vs job description")
    st.markdown("5. **History** — SQLite parse history")
    st.divider()
    st.caption("v2.0 · spaCy · Claude Haiku · FastAPI")

st.markdown(hero(
    "AI · NLP · HR Tech",
    "Recruit",
    "Lens",
    "Turn any CV into structured data in seconds. ATS scoring, JD matching, and full parse history — all in one place.",
), unsafe_allow_html=True)

st.markdown(feature_cards(
    ("📄", "Parse Resume",
     "Upload a PDF, DOCX, TXT, or RTF and extract name, skills, experience, education, and an ATS score."),
    ("📊", "Batch Upload",
     "Process up to 10 resumes at once. Compare side-by-side with ATS scores highlighted."),
    ("🎯", "JD Match",
     "Paste a job description and instantly see matched vs missing skills plus a fit percentage."),
    ("🕓", "History",
     "Every parsed resume is saved to local SQLite. Browse, search, and export the full archive."),
    ("🔬", "Demo Mode",
     "Explore the bundled sample dataset or upload the full Kaggle Resume CSV for a live tour."),
), unsafe_allow_html=True)

st.markdown(section("What gets extracted"), unsafe_allow_html=True)

st.markdown(step_cards(
    ("Contact Info",
     "Name via spaCy NER, email and phone via regex, LinkedIn URL — all from the resume header."),
    ("Skills Taxonomy",
     "80+ curated keywords across Python, ML, cloud, DevOps, and soft skills. Whole-word match, case-insensitive."),
    ("Work Experience",
     "Job titles, company names, and date ranges. Section-aware extraction scopes parsing to the Experience block."),
    ("Education",
     "Degree type, institution, and graduation year. Matched against common degree keywords with context look-ahead."),
    ("ATS Readiness",
     "0–100 score across contact completeness (20), skill count (25), experience depth (25), education (15), detail (15)."),
    ("Years of Experience",
     "Date ranges are parsed, overlapping intervals merged, and total non-overlapping years returned."),
), unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;font-size:0.82rem;color:#94A3B8;'>"
    "Use the <strong>sidebar navigation</strong> to get started."
    "</p>",
    unsafe_allow_html=True,
)

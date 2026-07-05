import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from auth import require_auth

st.set_page_config(
    page_title="RecruitLens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

require_auth()

st.markdown("""
<style>
.skill-badge {
    display: inline-block;
    background: #4A90D9;
    color: white;
    padding: 3px 10px;
    border-radius: 12px;
    margin: 2px;
    font-size: 0.82em;
    font-weight: 500;
}
.info-card {
    background: #F0F4F8;
    border-left: 4px solid #4A90D9;
    padding: 12px 16px;
    border-radius: 6px;
    margin-bottom: 12px;
}
.section-header {
    font-size: 1.1em;
    font-weight: 700;
    color: #1A1A2E;
    margin-bottom: 8px;
    border-bottom: 2px solid #4A90D9;
    padding-bottom: 4px;
}
.highlight-green {
    background-color: #d4edda !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/resume.png", width=80)
    st.title("RecruitLens")
    st.caption("From PDF to insight in seconds.")
    st.divider()
    st.markdown("**Supported formats**")
    st.markdown("- PDF (text & scanned via OCR)")
    st.markdown("- Word (.docx)")
    st.markdown("- Plain text (.txt)")
    st.markdown("- Rich Text (.rtf)")
    st.divider()
    st.markdown("**How to use**")
    st.markdown("1. **Parse Resume** — single CV analysis + ATS score")
    st.markdown("2. **Batch Upload** — compare up to 10 CVs")
    st.markdown("3. **Demo** — quick tour with sample data")
    st.markdown("4. **JD Match** — compare resume vs job description")
    st.markdown("5. **History** — browse all previously parsed CVs")
    st.divider()
    st.caption("v2.0 · spaCy + Streamlit + Claude Haiku")

st.title("Welcome to RecruitLens 🔍")
st.subheader("AI-powered CV parsing for modern HR teams")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.info("**Parse Resume**\nUpload a PDF, DOCX, TXT, or RTF and extract structured data with ATS score.")
with col2:
    st.success("**Batch Upload**\nCompare up to 10 resumes side-by-side with ATS scores.")
with col3:
    st.warning("**Demo Mode**\nExplore pre-loaded sample resumes with analytics charts.")
with col4:
    st.info("**JD Match**\nPaste a job description and see how well a resume matches.")
with col5:
    st.success("**History**\nBrowse all parsed resumes stored in local SQLite.")

st.divider()
st.markdown("#### What gets extracted")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Contact Info", "Name · Email · Phone · LinkedIn")
c2.metric("Skills", "80+ taxonomy keywords")
c3.metric("Experience", "Titles · Companies · Dates")
c4.metric("Education", "Degrees · Institutions · Years")
c5.metric("ATS Score", "0–100 readiness score")
c6.metric("Years Exp.", "Non-overlapping date ranges")

st.divider()
st.markdown("Use the **sidebar navigation** (or the pages listed on the left) to get started.")

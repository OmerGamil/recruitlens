import os
import sys
import time
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.extractor import parse_resume
from utils.file_reader import read_file
from utils.parser import load_nlp
from utils.jd_matcher import match_jd

st.set_page_config(page_title="JD Match – RecruitLens", layout="wide")

st.markdown("""
<style>
.skill-badge-match {
    display: inline-block;
    background: #28a745;
    color: white;
    padding: 3px 10px;
    border-radius: 12px;
    margin: 2px 3px;
    font-size: 0.82em;
    font-weight: 500;
}
.skill-badge-miss {
    display: inline-block;
    background: #dc3545;
    color: white;
    padding: 3px 10px;
    border-radius: 12px;
    margin: 2px 3px;
    font-size: 0.82em;
    font-weight: 500;
}
.match-bar-wrap {
    background: #e9ecef;
    border-radius: 8px;
    height: 22px;
    width: 100%;
    margin: 6px 0 12px 0;
}
.match-bar-fill {
    height: 22px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**How to use**")
    st.markdown("1. Upload a resume (PDF, DOCX, TXT, or RTF)")
    st.markdown("2. Paste the Job Description below")
    st.markdown("3. Click **Analyse Match**")
    st.divider()
    st.caption("Skills matched against 80+ taxonomy keywords.")

st.title("Job Description Match")
st.caption("Compare a resume against a job description to see skills overlap and fit score.")

col_left, col_right = st.columns([1, 1])

with col_left:
    uploaded = st.file_uploader(
        "Upload resume",
        type=["pdf", "docx", "txt", "rtf"],
        label_visibility="visible",
    )

with col_right:
    jd_text = st.text_area(
        "Paste Job Description",
        height=260,
        placeholder="Paste the full job description here…",
    )

run = st.button("Analyse Match", type="primary", disabled=(uploaded is None or not jd_text.strip()))

if run and uploaded and jd_text.strip():
    nlp = load_nlp()
    with st.spinner("Parsing resume…"):
        raw_text = read_file(uploaded)
        parsed = parse_resume(raw_text, nlp)

    result = match_jd(parsed, jd_text)

    st.divider()
    st.subheader("Match Results")

    overall = result["overall_pct"]
    skill_pct = result["skill_match_pct"]
    kw_pct = result["keyword_overlap_pct"]

    bar_color = "#28a745" if overall >= 70 else ("#ffc107" if overall >= 45 else "#dc3545")
    st.markdown(
        f'<div class="match-bar-wrap">'
        f'<div class="match-bar-fill" style="width:{overall}%; background:{bar_color};"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Overall Match", f"{overall}%")
    m2.metric("Skill Overlap", f"{skill_pct}%", help="% of JD skills found in resume")
    m3.metric("Keyword Overlap", f"{kw_pct}%", help="% of 4+ char JD words found in resume text")

    st.divider()

    c_match, c_miss = st.columns(2)
    with c_match:
        st.markdown(f"**Matched Skills ({len(result['matched_skills'])})**")
        if result["matched_skills"]:
            badges = " ".join(
                f'<span class="skill-badge-match">{s}</span>' for s in result["matched_skills"]
            )
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.info("No taxonomy skills matched.")

    with c_miss:
        st.markdown(f"**Missing Skills ({len(result['missing_skills'])})**")
        if result["missing_skills"]:
            badges = " ".join(
                f'<span class="skill-badge-miss">{s}</span>' for s in result["missing_skills"]
            )
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.success("All JD skills are present in the resume.")

    if not result["jd_skills"]:
        st.info("No taxonomy keywords found in the job description — keyword overlap score used only.")
else:
    if not uploaded:
        st.info("Upload a resume above to get started.")
    elif not jd_text.strip():
        st.info("Paste a job description on the right to enable analysis.")

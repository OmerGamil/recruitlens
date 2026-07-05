import os
import sys
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.extractor import parse_resume
from utils.file_reader import read_file
from utils.parser import load_nlp
from utils.jd_matcher import match_jd
from utils.styles import inject, page_header, section, divider, ats_bar, skill_badges

st.set_page_config(page_title="JD Match – RecruitLens", layout="wide")
st.markdown(inject(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**How to use**")
    st.markdown("1. Upload a resume")
    st.markdown("2. Paste the job description")
    st.markdown("3. Click **Analyse Match**")
    st.divider()
    st.caption("Skills matched against 80+ taxonomy keywords.")

st.markdown(page_header(
    "Job Description Match",
    "Compare a resume against a job description — see skills overlap and overall fit score.",
), unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1])
with col_left:
    uploaded = st.file_uploader("Upload resume", type=["pdf", "docx", "txt", "rtf"])
with col_right:
    jd_text = st.text_area("Paste Job Description", height=220,
                            placeholder="Paste the full job description here…")

run = st.button("Analyse Match", type="primary",
                disabled=(uploaded is None or not jd_text.strip()),
                use_container_width=True)

if run and uploaded and jd_text.strip():
    nlp = load_nlp()
    with st.spinner("Parsing resume…"):
        raw_text = read_file(uploaded)
        parsed = parse_resume(raw_text, nlp)

    result = match_jd(parsed, jd_text)
    overall = result["overall_pct"]

    st.markdown(divider(), unsafe_allow_html=True)
    st.markdown(section("Match Results"), unsafe_allow_html=True)

    st.markdown(ats_bar(int(overall)), unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("Overall Match",    f"{overall}%")
    m2.metric("Skill Overlap",    f"{result['skill_match_pct']}%",
              help="% of JD skills found in resume")
    m3.metric("Keyword Overlap",  f"{result['keyword_overlap_pct']}%",
              help="% of 4+ char JD words found in resume text")

    st.markdown(divider(), unsafe_allow_html=True)

    c_match, c_miss = st.columns(2)
    with c_match:
        st.markdown(f"**Matched Skills ({len(result['matched_skills'])})**")
        if result["matched_skills"]:
            st.markdown(skill_badges(result["matched_skills"], "green"), unsafe_allow_html=True)
        else:
            st.info("No taxonomy skills matched.")

    with c_miss:
        st.markdown(f"**Missing Skills ({len(result['missing_skills'])})**")
        if result["missing_skills"]:
            st.markdown(skill_badges(result["missing_skills"], "red"), unsafe_allow_html=True)
        else:
            st.success("All JD skills are present in the resume.")

    if not result["jd_skills"]:
        st.info("No taxonomy keywords found in the JD — keyword overlap score used only.")
else:
    if not uploaded:
        st.info("Upload a resume above to get started.")
    elif not jd_text.strip():
        st.info("Paste a job description on the right, then click **Analyse Match**.")

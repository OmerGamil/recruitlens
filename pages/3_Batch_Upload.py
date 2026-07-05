import os
import sys
import time
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.extractor import parse_resume, calculate_years_experience
from utils.file_reader import read_file
from utils.parser import load_nlp
from utils.ats_scorer import compute_ats_score
from utils.database import save_parse_result
from utils.styles import inject, page_header, section, divider, skill_badges

st.set_page_config(page_title="Batch Upload – RecruitLens", layout="wide")
st.markdown(inject(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Batch Upload**")
    st.markdown("- Up to 10 resumes at once")
    st.markdown("- PDF · DOCX · TXT · RTF")
    st.markdown("- ATS score per resume")
    st.markdown("- Export comparison CSV")

st.markdown(page_header(
    "Batch Resume Upload",
    "Upload up to 10 resumes and compare them side-by-side.",
), unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload resumes",
    type=["pdf", "docx", "txt", "rtf"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)

MAX_FILES = 10

if uploaded_files:
    if len(uploaded_files) > MAX_FILES:
        st.warning(f"Maximum {MAX_FILES} files allowed. Processing first {MAX_FILES}.")
        uploaded_files = uploaded_files[:MAX_FILES]

    nlp = load_nlp()
    results = []
    progress = st.progress(0, text="Processing resumes…")
    total = len(uploaded_files)

    for i, f in enumerate(uploaded_files):
        progress.progress(int((i / total) * 90), text=f"Parsing {f.name}…")
        raw_text = read_file(f)
        if raw_text and not raw_text.startswith("["):
            parsed = parse_resume(raw_text, nlp)
        else:
            parsed = {"name": "", "email": "", "phone": "", "linkedin": "",
                      "skills": [], "experience": [], "education": [], "summary": "",
                      "sections_detected": []}

        years_exp = calculate_years_experience(parsed["experience"])

        edu_level = "—"
        for edu in parsed["education"]:
            deg = edu.get("degree", "").lower()
            if any(x in deg for x in ["phd", "ph.d", "doctor"]):
                edu_level = "PhD"; break
            elif any(x in deg for x in ["master", "m.s", "m.sc", "mba", "m.e", "m.tech"]):
                edu_level = "Masters"
            elif any(x in deg for x in ["bachelor", "b.s", "b.sc", "b.e", "b.tech", "b.a"]):
                if edu_level != "Masters": edu_level = "Bachelors"
            elif any(x in deg for x in ["diploma", "certificate"]):
                if edu_level == "—": edu_level = "Diploma"

        ats = compute_ats_score(parsed, raw_text if raw_text and not raw_text.startswith("[") else "")
        save_parse_result(f.name, parsed, ats_score=ats["total"], years_exp=years_exp)

        results.append({
            "File": f.name,
            "Name": parsed["name"] or "—",
            "Email": parsed["email"] or "—",
            "Top Skills": ", ".join(parsed["skills"][:5]) if parsed["skills"] else "—",
            "Skill Count": len(parsed["skills"]),
            "Years Exp.": years_exp,
            "Education": edu_level,
            "ATS Score": ats["total"],
            "_parsed": parsed,
            "_skills": parsed["skills"],
        })
        time.sleep(0.05)

    progress.progress(100, text="Done!")
    time.sleep(0.3)
    progress.empty()

    st.success(f"Parsed **{len(results)}** resumes.")

    st.markdown(section("Comparison Table"), unsafe_allow_html=True)

    display_cols = ["File", "Name", "Email", "Top Skills", "Skill Count", "Years Exp.", "Education", "ATS Score"]
    df_display = pd.DataFrame(results)[display_cols]

    def highlight_top(df):
        styles = pd.DataFrame("", index=df.index, columns=df.columns)
        for col in ["Skill Count", "Years Exp.", "ATS Score"]:
            if col in df.columns:
                max_val = df[col].max()
                if max_val > 0:
                    styles.loc[df[col] == max_val, col] = "background-color:#DCFCE7;font-weight:700;"
        return styles

    st.dataframe(
        df_display.style.apply(highlight_top, axis=None),
        use_container_width=True,
        height=min(420, 80 + len(results) * 42),
    )
    st.caption("Green = top value in that column.")

    st.download_button(
        label="Download Comparison CSV",
        data=df_display.to_csv(index=False).encode(),
        file_name="recruitlens_batch.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown(divider(), unsafe_allow_html=True)
    st.markdown(section("Individual Details"), unsafe_allow_html=True)

    for r in results:
        p = r["_parsed"]
        with st.expander(f"{r['File']}  ·  {r['Name']}  ·  ATS {r['ATS Score']}/100", expanded=False):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown("**Contact**")
                st.write(f"Email: {p['email'] or '—'}")
                st.write(f"Phone: {p['phone'] or '—'}")
                st.markdown("**Education**")
                for edu in p["education"]:
                    st.write(f"- {edu['degree']} {edu.get('year','')}")
                if not p["education"]:
                    st.write("—")
            with c2:
                st.markdown("**Skills**")
                if r["_skills"]:
                    st.markdown(skill_badges(r["_skills"]), unsafe_allow_html=True)
                else:
                    st.write("—")
                st.markdown("**Summary**")
                st.write(p["summary"])
else:
    st.info("Upload PDF, DOCX, TXT, or RTF resumes above (up to 10 at once).")

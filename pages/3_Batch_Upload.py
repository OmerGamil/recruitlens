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

st.set_page_config(page_title="Batch Upload – RecruitLens", layout="wide")

st.markdown("""
<style>
.skill-badge {
    display: inline-block;
    background: #4A90D9;
    color: white;
    padding: 2px 8px;
    border-radius: 10px;
    margin: 1px;
    font-size: 0.78em;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Batch Upload**")
    st.markdown("- Upload up to 10 resumes at once")
    st.markdown("- Supported: PDF, DOCX")
    st.markdown("- Results show in a comparison table")
    st.markdown("- Download as CSV")
    st.divider()
    st.caption("From PDF to insight in seconds.")

st.title("Batch Resume Upload")
st.caption("Upload up to 10 resumes and compare them side-by-side.")

uploaded_files = st.file_uploader(
    "Upload resumes (PDF, DOCX, TXT, or RTF)",
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
    progress = st.progress(0, text="Processing resumes...")
    total = len(uploaded_files)

    for i, f in enumerate(uploaded_files):
        progress.progress(int((i / total) * 90), text=f"Parsing {f.name}...")
        raw_text = read_file(f)
        if raw_text and not raw_text.startswith("["):
            parsed = parse_resume(raw_text, nlp)
        else:
            parsed = {
                "name": "", "email": "", "phone": "", "linkedin": "",
                "skills": [], "experience": [], "education": [], "summary": "",
            }

        years_exp = calculate_years_experience(parsed["experience"])

        # Education level
        edu_level = "—"
        for edu in parsed["education"]:
            deg = edu.get("degree", "").lower()
            if any(x in deg for x in ["phd", "ph.d", "doctor"]):
                edu_level = "PhD"
                break
            elif any(x in deg for x in ["master", "m.s", "m.sc", "mba", "m.e", "m.tech"]):
                edu_level = "Masters"
            elif any(x in deg for x in ["bachelor", "b.s", "b.sc", "b.e", "b.tech", "b.a"]):
                if edu_level != "Masters":
                    edu_level = "Bachelors"
            elif any(x in deg for x in ["diploma", "certificate", "associate"]):
                if edu_level == "—":
                    edu_level = "Diploma/Certificate"

        ats = compute_ats_score(parsed, raw_text if raw_text and not raw_text.startswith("[") else "")
        save_parse_result(f.name, parsed, ats_score=ats["total"], years_exp=years_exp)

        results.append({
            "File": f.name,
            "Name": parsed["name"] or "—",
            "Email": parsed["email"] or "—",
            "Top Skills": ", ".join(parsed["skills"][:5]) if parsed["skills"] else "—",
            "Skill Count": len(parsed["skills"]),
            "Years Experience": years_exp,
            "Education Level": edu_level,
            "ATS Score": ats["total"],
            "_parsed": parsed,
            "_raw_skills": parsed["skills"],
        })
        time.sleep(0.05)

    progress.progress(100, text="Done!")
    time.sleep(0.3)
    progress.empty()

    st.success(f"Parsed **{len(results)}** resumes.")

    # Build display dataframe (excluding internal fields)
    display_cols = ["File", "Name", "Email", "Top Skills", "Skill Count", "Years Experience", "Education Level", "ATS Score"]
    df_display = pd.DataFrame(results)[display_cols]

    # Highlight top candidate per numeric column
    def highlight_top(df):
        styles = pd.DataFrame("", index=df.index, columns=df.columns)
        for col in ["Skill Count", "Years Experience", "ATS Score"]:
            if col in df.columns:
                max_val = df[col].max()
                if max_val > 0:
                    styles.loc[df[col] == max_val, col] = "background-color: #d4edda; font-weight: bold"
        return styles

    st.subheader("Comparison Table")
    st.dataframe(
        df_display.style.apply(highlight_top, axis=None),
        use_container_width=True,
        height=min(400, 80 + len(results) * 40),
    )

    st.caption("Green highlight = top candidate in that column.")

    # Download
    csv_bytes = df_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Comparison CSV",
        data=csv_bytes,
        file_name="recruitlens_batch_comparison.csv",
        mime="text/csv",
    )

    st.divider()
    st.subheader("Individual Resume Details")

    for r in results:
        parsed = r["_parsed"]
        with st.expander(f"{r['File']} — {r['Name']}", expanded=False):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown("**Contact**")
                st.write(f"Email: {parsed['email'] or '—'}")
                st.write(f"Phone: {parsed['phone'] or '—'}")
                st.divider()
                st.markdown("**Education**")
                for edu in parsed["education"]:
                    st.write(f"- {edu['degree']} {edu['year']}")
                if not parsed["education"]:
                    st.write("—")
            with c2:
                st.markdown("**Skills**")
                if r["_raw_skills"]:
                    badges = " ".join(
                        f'<span class="skill-badge">{s}</span>' for s in r["_raw_skills"]
                    )
                    st.markdown(badges, unsafe_allow_html=True)
                else:
                    st.write("—")
                st.divider()
                st.markdown("**Summary**")
                st.write(parsed["summary"])
else:
    st.info("Upload PDF or DOCX resumes above (up to 10 at once).")

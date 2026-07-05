import streamlit as st

st.set_page_config(page_title="About – RecruitLens", layout="wide")

st.title("About RecruitLens")
st.caption("Methodology, accuracy notes, and business use cases.")

st.header("How it works")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Named Entity Recognition (NER)")
    st.markdown("""
RecruitLens uses **spaCy's `en_core_web_sm`** model — a lightweight English NLP pipeline
trained on OntoNotes 5. It recognises:

| Entity Label | Used For |
|---|---|
| `PERSON` | Candidate name extraction |
| `ORG` | Company / institution names |
| `GPE` / `LOC` | Location mentions |
| `DATE` | Date ranges in experience |

NER is applied to the **first 10 lines** of the resume for name extraction, since the
candidate's name is almost always near the top.
""")

    st.subheader("Regex Extraction")
    st.markdown("""
For structured fields with predictable patterns, regex is more reliable than NER:

| Field | Pattern |
|---|---|
| **Email** | `[a-zA-Z0-9._%+−]+@[a-zA-Z0-9.−]+\\.[a-zA-Z]{2,}` |
| **Phone** | International format with optional country code |
| **LinkedIn** | `linkedin.com/in/<handle>` |
| **Date ranges** | Month/year or year-only ranges with separators |
| **Graduation year** | 4-digit year near a degree keyword |
""")

with col2:
    st.subheader("Skills Taxonomy")
    st.markdown("""
Skills are matched against a **curated taxonomy of 80+ keywords** covering:

- **Programming languages**: Python, Java, JavaScript, R, Go, Rust, C#, Swift…
- **ML/AI frameworks**: TensorFlow, PyTorch, scikit-learn, Hugging Face…
- **Data tools**: SQL, Spark, Airflow, dbt, Snowflake, BigQuery, Tableau…
- **Cloud & DevOps**: AWS, Azure, GCP, Docker, Kubernetes, Terraform…
- **Soft skills**: Communication, Leadership, Project Management, Agile…

Matching uses **whole-word regex** (case-insensitive) to avoid false positives
(e.g. "React" won't match "reacting").
""")

    st.subheader("Auto-Generated Summary")
    st.markdown("""
The 2-sentence profile is assembled from extracted fields:

1. **Sentence 1** — Name + most recent job title/company + highest degree
2. **Sentence 2** — Top 5 skills from taxonomy match

This is a template-based summary, not an LLM generation, ensuring speed and
deterministic output.
""")

st.divider()

st.header("Accuracy & Limitations")
col3, col4 = st.columns(2)

with col3:
    st.warning("""
**Known Limitations**

- **Scanned / image-based PDFs** — OCR fallback via pytesseract (requires optional
  `pdf2image` + `pytesseract` packages; omitted from default install).
- **Non-standard layouts** — Two-column, table-heavy, or graphical CVs may extract text
  out of reading order.
- **Experience parsing** — Date range detection relies on explicit textual dates.
- **Name extraction** — Uncommon name formats or names preceded by email/phone may
  confuse the NER model.
- **Multi-language resumes** — The spaCy model is English-only.
- **LLM fallback** — Requires `ANTHROPIC_API_KEY` in environment; defaults to regex-only
  mode when the key is absent.
""")

with col4:
    st.success("""
**What works well**

- Clean, text-based PDF and DOCX files produced by word processors
- Standard single-column CV layouts
- English-language resumes
- Skills mentioned by exact keyword (not paraphrased)
- Degrees stated explicitly (e.g. "Master of Science")
- Dates in common formats (Jan 2020 – Mar 2022, 2019–2021)
""")

st.divider()

st.header("Business Use Cases")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("**Initial Screening**")
    st.markdown("""
Parse hundreds of CVs in minutes. Filter candidates automatically by required skills
before human review. Reduce time-to-shortlist by up to 70%.
""")

with c2:
    st.markdown("**Skill Gap Analysis**")
    st.markdown("""
Upload your entire talent pool and visualise skill frequency across candidates.
Identify capability gaps and prioritise training investments.
""")

with c3:
    st.markdown("**Candidate Benchmarking**")
    st.markdown("""
Use the batch comparison table to rank candidates by skill count, experience, and
education level. Export to CSV for integration with ATS or HR platforms.
""")

st.divider()
st.markdown("""
**Dataset Credit:** Sample resumes sourced from the
[Resume Dataset](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset)
by Gaurav Dutta on Kaggle (CC BY 4.0).

**Tech Stack:** Streamlit · spaCy · PyMuPDF · python-docx · Plotly · Pandas · Anthropic SDK · FastAPI
""")
st.caption("RecruitLens v2.0 — Built for demonstration and educational purposes.")

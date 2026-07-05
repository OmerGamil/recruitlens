import os
import sys
import json
import time
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.extractor import parse_resume, calculate_years_experience
from utils.file_reader import read_file
from utils.parser import load_nlp
from utils.ats_scorer import compute_ats_score
from utils.anonymizer import anonymize
from utils.database import save_parse_result

st.set_page_config(page_title="Parse Resume – RecruitLens", layout="wide")

st.markdown("""
<style>
.skill-badge {
    display: inline-block;
    background: #4A90D9;
    color: white;
    padding: 3px 10px;
    border-radius: 12px;
    margin: 2px 3px;
    font-size: 0.82em;
    font-weight: 500;
}
.info-card {
    background: #F0F4F8;
    border-left: 4px solid #4A90D9;
    padding: 14px 18px;
    border-radius: 8px;
    margin-bottom: 14px;
}
.section-header {
    font-size: 1.05em;
    font-weight: 700;
    color: #1A1A2E;
    margin-bottom: 6px;
}
.ats-bar-wrap {
    background: #e9ecef;
    border-radius: 8px;
    height: 18px;
    width: 100%;
    margin: 6px 0 10px 0;
}
.ats-bar-fill {
    height: 18px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Upload Instructions**")
    st.markdown("- PDF, DOCX, TXT, or RTF files")
    st.markdown("- Max file size: 50 MB")
    st.markdown("- One file at a time")
    st.markdown("- Scanned PDFs: OCR attempted automatically")
    st.divider()
    anonymize_toggle = st.checkbox("Anonymise output (strip PII)", value=False)
    use_llm_fallback = st.checkbox(
        "LLM fallback (needs ANTHROPIC_API_KEY)",
        value=False,
        help="Calls claude-haiku-4-5 when regex/spaCy find nothing.",
    )
    save_to_db = st.checkbox("Save to history", value=True)
    st.divider()
    st.caption("From PDF to insight in seconds.")

st.title("Parse a Resume")
st.caption("Upload a PDF, DOCX, TXT, or RTF resume to extract structured data.")

uploaded = st.file_uploader(
    "Drop your resume here",
    type=["pdf", "docx", "txt", "rtf"],
    label_visibility="collapsed",
)

if uploaded is not None:
    nlp = load_nlp()

    progress = st.progress(0, text="Reading file...")
    time.sleep(0.1)

    raw_text = read_file(uploaded)
    progress.progress(25, text="Extracting text...")
    time.sleep(0.1)

    if raw_text.startswith("[") and "error" in raw_text:
        st.error(raw_text)
        st.stop()

    if not raw_text.strip():
        st.warning("No text could be extracted. The file may be scanned or image-based.")
        st.stop()

    progress.progress(50, text="Running NLP pipeline...")
    parsed = parse_resume(raw_text, nlp)
    progress.progress(75, text="Scoring & enriching...")

    # LLM fallback – only trigger when key fields are empty
    if use_llm_fallback and (not parsed.get("name") or not parsed.get("skills")):
        from utils.llm_extractor import llm_extract_fields
        llm_data = llm_extract_fields(raw_text)
        if llm_data:
            for field in ("name", "email", "phone", "linkedin"):
                if not parsed.get(field) and llm_data.get(field):
                    parsed[field] = llm_data[field]
            if not parsed.get("skills") and llm_data.get("skills"):
                parsed["skills"] = llm_data["skills"]
            if not parsed.get("experience") and llm_data.get("experience"):
                parsed["experience"] = llm_data["experience"]
            if not parsed.get("education") and llm_data.get("education"):
                parsed["education"] = llm_data["education"]

    years_exp = calculate_years_experience(parsed["experience"])
    ats = compute_ats_score(parsed, raw_text)

    if save_to_db:
        save_parse_result(uploaded.name, parsed, ats_score=ats["total"], years_exp=years_exp)

    progress.progress(100, text="Done!")
    time.sleep(0.3)
    progress.empty()

    display_parsed = anonymize(parsed) if anonymize_toggle else parsed
    st.success(f"Parsed **{uploaded.name}** successfully.")

    # ── ATS Score ─────────────────────────────────────────────────────────────
    ats_total = ats["total"]
    ats_color = "#28a745" if ats_total >= 70 else ("#ffc107" if ats_total >= 45 else "#dc3545")
    st.markdown("#### ATS Readiness Score")
    st.markdown(
        f'<div class="ats-bar-wrap">'
        f'<div class="ats-bar-fill" style="width:{ats_total}%; background:{ats_color};"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    mc1, mc2, mc3, mc4, mc5, mc6 = st.columns(6)
    mc1.metric("Total", f"{ats_total}/100")
    mc2.metric("Contact", f"{ats['breakdown']['contact']}/20")
    mc3.metric("Skills", f"{ats['breakdown']['skills']}/25")
    mc4.metric("Experience", f"{ats['breakdown']['experience']}/25")
    mc5.metric("Education", f"{ats['breakdown']['education']}/15")
    mc6.metric("Detail", f"{ats['breakdown']['length']}/15")

    st.divider()

    # ── Contact Info ──────────────────────────────────────────────────────────
    st.markdown('<p class="section-header">Contact Information</p>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Name", display_parsed["name"] or "Not found")
    c2.metric("Email", display_parsed["email"] or "Not found")
    c3.metric("Phone", display_parsed["phone"] or "Not found")
    c4.metric("LinkedIn", display_parsed["linkedin"] or "Not found")
    c5.metric("Years Exp.", f"{years_exp:.1f}")

    st.divider()

    left, right = st.columns([3, 2])

    with left:
        # ── Skills ──────────────────────────────────────────────────────────
        st.markdown('<p class="section-header">Skills Detected</p>', unsafe_allow_html=True)
        if display_parsed["skills"]:
            badges = " ".join(
                f'<span class="skill-badge">{s}</span>' for s in display_parsed["skills"]
            )
            st.markdown(f'<div class="info-card">{badges}</div>', unsafe_allow_html=True)
        else:
            st.info("No skills matched the taxonomy.")

        # ── Summary ──────────────────────────────────────────────────────────
        st.markdown('<p class="section-header">Auto-Generated Summary</p>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="info-card">{display_parsed["summary"]}</div>',
            unsafe_allow_html=True,
        )

    with right:
        # ── Experience ───────────────────────────────────────────────────────
        st.markdown('<p class="section-header">Work Experience</p>', unsafe_allow_html=True)
        if display_parsed["experience"]:
            for exp in display_parsed["experience"]:
                st.markdown(
                    f'<div class="info-card">'
                    f'<strong>{exp.get("title", "—")}</strong><br>'
                    f'{exp.get("company", "") or ""}'
                    f'{"<br>" if exp.get("company") else ""}'
                    f'<em>{exp.get("dates", "")}</em>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No experience entries detected.")

        # ── Education ────────────────────────────────────────────────────────
        st.markdown('<p class="section-header">Education</p>', unsafe_allow_html=True)
        if display_parsed["education"]:
            for edu in display_parsed["education"]:
                st.markdown(
                    f'<div class="info-card">'
                    f'<strong>{edu.get("degree", "—")}</strong><br>'
                    f'{edu.get("institution", "") or ""}'
                    f'{"<br>" if edu.get("institution") else ""}'
                    f'<em>{edu.get("year", "")}</em>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No education entries detected.")

    st.divider()

    with st.expander("Raw extracted JSON"):
        st.json(display_parsed)

    st.markdown("**Export Results**")
    dl_col1, dl_col2 = st.columns(2)

    with dl_col1:
        json_bytes = json.dumps(display_parsed, indent=2, ensure_ascii=False).encode("utf-8")
        st.download_button(
            label="Download as JSON",
            data=json_bytes,
            file_name=f"{uploaded.name.rsplit('.', 1)[0]}_parsed.json",
            mime="application/json",
        )

    with dl_col2:
        flat = {
            "name": display_parsed["name"],
            "email": display_parsed["email"],
            "phone": display_parsed["phone"],
            "linkedin": display_parsed["linkedin"],
            "skills": ", ".join(display_parsed["skills"]),
            "experience_count": len(display_parsed["experience"]),
            "education_count": len(display_parsed["education"]),
            "years_experience": years_exp,
            "ats_score": ats_total,
            "summary": display_parsed["summary"],
        }
        csv_bytes = pd.DataFrame([flat]).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download as CSV",
            data=csv_bytes,
            file_name=f"{uploaded.name.rsplit('.', 1)[0]}_parsed.csv",
            mime="text/csv",
        )

    with st.expander("View raw extracted text"):
        st.text_area("Raw text", raw_text[:5000], height=300, disabled=True)
else:
    st.info("Upload a PDF, DOCX, TXT, or RTF resume above to get started.")

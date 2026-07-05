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
from utils.styles import inject, page_header, section, divider, ats_bar, ats_stats, skill_badges, info_card

st.set_page_config(page_title="Parse Resume – RecruitLens", layout="wide")
st.markdown(inject(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Options**")
    anonymize_toggle = st.checkbox("Anonymise output (strip PII)", value=False)
    use_llm_fallback = st.checkbox(
        "LLM fallback (needs ANTHROPIC_API_KEY)",
        value=False,
        help="Calls claude-haiku-4-5 when regex/spaCy find nothing.",
    )
    save_to_db = st.checkbox("Save to history", value=True)
    st.divider()
    st.markdown("**Supported formats**")
    st.markdown("PDF · DOCX · TXT · RTF")
    st.markdown("Max 50 MB · Scanned PDFs: OCR attempted")

st.markdown(page_header("Parse a Resume", "Upload a PDF, DOCX, TXT, or RTF resume to extract structured data."), unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Drop your resume here",
    type=["pdf", "docx", "txt", "rtf"],
    label_visibility="collapsed",
)

if uploaded is not None:
    nlp = load_nlp()
    progress = st.progress(0, text="Reading file…")
    time.sleep(0.1)
    raw_text = read_file(uploaded)
    progress.progress(25, text="Extracting text…")

    if raw_text.startswith("[") and "error" in raw_text:
        st.error(raw_text)
        st.stop()
    if not raw_text.strip():
        st.warning("No text could be extracted. The file may be scanned or image-based.")
        st.stop()

    progress.progress(50, text="Running NLP pipeline…")
    parsed = parse_resume(raw_text, nlp)
    progress.progress(75, text="Scoring & enriching…")

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
    st.markdown(section("ATS Readiness Score"), unsafe_allow_html=True)
    st.markdown(ats_bar(ats["total"]), unsafe_allow_html=True)
    st.markdown(ats_stats(
        ats["total"],
        ats["breakdown"]["contact"],
        ats["breakdown"]["skills"],
        ats["breakdown"]["experience"],
        ats["breakdown"]["education"],
        ats["breakdown"]["length"],
    ), unsafe_allow_html=True)

    # ── Contact ───────────────────────────────────────────────────────────────
    st.markdown(section("Contact Information"), unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Name",       display_parsed["name"]    or "—")
    c2.metric("Email",      display_parsed["email"]   or "—")
    c3.metric("Phone",      display_parsed["phone"]   or "—")
    c4.metric("LinkedIn",   display_parsed["linkedin"] or "—")
    c5.metric("Years Exp.", f"{years_exp:.1f}")

    st.markdown(divider(), unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        st.markdown(section("Skills Detected"), unsafe_allow_html=True)
        if display_parsed["skills"]:
            st.markdown(
                f'<div style="padding:14px 16px;background:#F8FAFF;border:1px solid rgba(37,99,235,0.10);border-radius:10px;">'
                f'{skill_badges(display_parsed["skills"])}'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.info("No skills matched the taxonomy.")

        st.markdown(section("Auto-Generated Summary"), unsafe_allow_html=True)
        st.markdown(
            f'<div style="padding:14px 16px;background:#F8FAFF;border:1px solid rgba(37,99,235,0.10);border-left:3px solid #2563EB;border-radius:10px;font-size:0.92rem;color:#0F172A;line-height:1.7;">'
            f'{display_parsed["summary"]}'
            f'</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(section("Work Experience"), unsafe_allow_html=True)
        if display_parsed["experience"]:
            for exp in display_parsed["experience"]:
                st.markdown(
                    info_card(
                        exp.get("title", "—"),
                        exp.get("company", ""),
                        exp.get("dates", ""),
                    ),
                    unsafe_allow_html=True,
                )
        else:
            st.info("No experience entries detected.")

        st.markdown(section("Education"), unsafe_allow_html=True)
        if display_parsed["education"]:
            for edu in display_parsed["education"]:
                st.markdown(
                    info_card(
                        edu.get("degree", "—"),
                        edu.get("institution", ""),
                        edu.get("year", ""),
                    ),
                    unsafe_allow_html=True,
                )
        else:
            st.info("No education entries detected.")

    st.markdown(divider(), unsafe_allow_html=True)

    with st.expander("Raw extracted JSON"):
        st.json(display_parsed)

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="Download JSON",
            data=json.dumps(display_parsed, indent=2, ensure_ascii=False).encode(),
            file_name=f"{uploaded.name.rsplit('.', 1)[0]}_parsed.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_dl2:
        flat = {
            "name": display_parsed["name"], "email": display_parsed["email"],
            "phone": display_parsed["phone"], "linkedin": display_parsed["linkedin"],
            "skills": ", ".join(display_parsed["skills"]),
            "experience_count": len(display_parsed["experience"]),
            "education_count": len(display_parsed["education"]),
            "years_experience": years_exp, "ats_score": ats["total"],
            "summary": display_parsed["summary"],
        }
        st.download_button(
            label="Download CSV",
            data=pd.DataFrame([flat]).to_csv(index=False).encode(),
            file_name=f"{uploaded.name.rsplit('.', 1)[0]}_parsed.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with st.expander("View raw extracted text"):
        st.text_area("Raw text", raw_text[:5000], height=280, disabled=True)
else:
    st.info("Upload a PDF, DOCX, TXT, or RTF resume above to get started.")

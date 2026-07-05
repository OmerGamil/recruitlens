import os
import sys
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.database import get_history, delete_record, clear_history
from utils.styles import inject, page_header, section, divider

st.set_page_config(page_title="History – RecruitLens", layout="wide")
st.markdown(inject(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Parse History**")
    st.markdown("Stored in local SQLite — resets on Heroku dyno restart.")
    st.divider()
    if st.button("Clear all history", type="secondary", use_container_width=True):
        clear_history()
        st.success("History cleared.")
        st.rerun()

st.markdown(page_header(
    "Parse History",
    "All resumes parsed by RecruitLens — newest first.",
), unsafe_allow_html=True)

rows = get_history(limit=200)

if not rows:
    st.info("No parse history yet. Parse a resume to see it here.")
    st.stop()

df = pd.DataFrame([
    {
        "ID":         r["id"],
        "File":       r["filename"],
        "Name":       r["name"] or "—",
        "Email":      r["email"] or "—",
        "Skills":     len(r["skills"]),
        "Exp.":       len(r["experience"]),
        "Years":      r["years_experience"],
        "ATS":        r["ats_score"],
        "Parsed At":  r["parsed_at"],
    }
    for r in rows
])

st.markdown(section(f"{len(df)} records"), unsafe_allow_html=True)
st.dataframe(df.drop(columns=["ID"]), use_container_width=True, height=420)

st.download_button(
    label="Download History CSV",
    data=df.drop(columns=["ID"]).to_csv(index=False).encode(),
    file_name="recruitlens_history.csv",
    mime="text/csv",
    use_container_width=True,
)

st.markdown(divider(), unsafe_allow_html=True)
st.markdown(section("Delete a Record"), unsafe_allow_html=True)

record_id = st.number_input("Record ID", min_value=1, step=1,
                             help="Enter the ID from the table above.")
if st.button("Delete record", type="secondary"):
    delete_record(int(record_id))
    st.success(f"Record {record_id} deleted.")
    st.rerun()

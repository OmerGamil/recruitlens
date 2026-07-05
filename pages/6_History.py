import os
import sys
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.database import get_history, delete_record, clear_history

st.set_page_config(page_title="History – RecruitLens", layout="wide")

with st.sidebar:
    st.markdown("**Parse History**")
    st.markdown("All resumes parsed in this deployment are stored locally in a SQLite database.")
    st.divider()
    if st.button("Clear all history", type="secondary"):
        clear_history()
        st.success("History cleared.")
        st.rerun()

st.title("Parse History")
st.caption("All resumes parsed by RecruitLens — sorted newest first.")

rows = get_history(limit=200)

if not rows:
    st.info("No parse history yet. Parse a resume to see it here.")
    st.stop()

# Build display dataframe
df = pd.DataFrame([
    {
        "ID": r["id"],
        "File": r["filename"],
        "Name": r["name"] or "—",
        "Email": r["email"] or "—",
        "Skills": len(r["skills"]),
        "Exp. Entries": len(r["experience"]),
        "Years Exp.": r["years_experience"],
        "ATS Score": r["ats_score"],
        "Parsed At": r["parsed_at"],
    }
    for r in rows
])

st.dataframe(df.drop(columns=["ID"]), use_container_width=True, height=400)

# Export full history
csv_bytes = df.drop(columns=["ID"]).to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download History CSV",
    data=csv_bytes,
    file_name="recruitlens_history.csv",
    mime="text/csv",
)

st.divider()
st.subheader("Delete a record")
record_id = st.number_input(
    "Record ID to delete",
    min_value=1,
    step=1,
    help="Enter the ID shown in the table above.",
)
if st.button("Delete record"):
    delete_record(int(record_id))
    st.success(f"Record {record_id} deleted.")
    st.rerun()

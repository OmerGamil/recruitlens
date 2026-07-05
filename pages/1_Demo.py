import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.extractor import parse_resume, SKILLS_TAXONOMY
from utils.parser import load_nlp
from utils.styles import inject, page_header, section, divider, skill_badges

st.set_page_config(page_title="Demo – RecruitLens", layout="wide")
st.markdown(inject(), unsafe_allow_html=True)

st.markdown(page_header(
    "Demo — Sample Resume Analysis",
    "Explore preloaded sample resumes or upload the full Kaggle dataset CSV.",
), unsafe_allow_html=True)

# ── Dataset source ─────────────────────────────────────────────────────────────
BUILTIN_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_resumes.csv")

# Kaggle dataset column aliases: the real Kaggle download uses "Resume_str";
# the bundled sample uses "Resume". We normalise to "Resume".
_KAGGLE_COL_MAP = {"Resume_str": "Resume", "resume_str": "Resume", "resume": "Resume"}

with st.sidebar:
    st.markdown("**Dataset**")
    data_source = st.radio(
        "Source",
        ["Built-in samples", "Upload Kaggle CSV"],
        label_visibility="collapsed",
    )
    if data_source == "Upload Kaggle CSV":
        kaggle_file = st.file_uploader(
            "Upload `UpdatedResumeDataSet.csv` or `Resume.csv` from Kaggle",
            type=["csv"],
        )
    else:
        kaggle_file = None
    st.divider()
    st.markdown(
        "Get the dataset: [Kaggle – Resume Dataset]"
        "(https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset)"
    )


@st.cache_data(show_spinner=False)
def load_builtin():
    return pd.read_csv(BUILTIN_PATH)


@st.cache_data(show_spinner=False)
def load_kaggle_bytes(raw: bytes):
    import io
    df = pd.read_csv(io.BytesIO(raw))
    # Normalise column names so downstream code always sees "Category" and "Resume"
    df = df.rename(columns=_KAGGLE_COL_MAP)
    if "Category" not in df.columns:
        df["Category"] = "Unknown"
    if "Resume" not in df.columns:
        st.error("CSV must have a 'Resume' or 'Resume_str' column.")
        st.stop()
    return df


@st.cache_data(show_spinner=False)
def parse_all_resumes(texts):
    nlp = load_nlp()
    return [parse_resume(t, nlp) for t in texts]


if kaggle_file is not None:
    with st.spinner("Loading Kaggle CSV..."):
        df = load_kaggle_bytes(kaggle_file.read())
    st.info(f"Loaded {len(df):,} resumes from uploaded Kaggle CSV.")
else:
    with st.spinner("Loading data..."):
        df = load_builtin()

nlp = load_nlp()

# Cap parsing at 200 rows to keep the demo snappy on large Kaggle files
PARSE_CAP = 200
if len(df) > PARSE_CAP:
    st.warning(f"Large dataset detected ({len(df):,} rows). Parsing first {PARSE_CAP} for speed.")
    df_parse = df.head(PARSE_CAP).reset_index(drop=True)
else:
    df_parse = df

st.subheader("Dataset overview")
col1, col2 = st.columns(2)
with col1:
    cat_counts = df_parse["Category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    fig_pie = px.pie(
        cat_counts, names="Category", values="Count",
        title="Resume Category Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    with st.spinner("Parsing resumes for skill frequency..."):
        all_parsed = parse_all_resumes(tuple(df_parse["Resume"].tolist()))

    skill_counts: dict = {}
    for parsed in all_parsed:
        for skill in parsed["skills"]:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

    if skill_counts:
        skill_df = (
            pd.DataFrame(list(skill_counts.items()), columns=["Skill", "Count"])
            .sort_values("Count", ascending=False)
            .head(20)
        )
        fig_bar = px.bar(
            skill_df, x="Count", y="Skill", orientation="h",
            title="Top 20 Skills Across All Resumes",
            color="Count",
            color_continuous_scale="Blues",
        )
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

st.markdown(divider(), unsafe_allow_html=True)
st.markdown(section("Parsed Resume Details"), unsafe_allow_html=True)

sample_size = min(5, len(df_parse))
indices = list(range(sample_size))
if st.button("Randomise selection"):
    import random
    indices = random.sample(range(len(df_parse)), sample_size)

for idx in indices:
    row = df_parse.iloc[idx]
    parsed = all_parsed[idx]
    with st.expander(
        f"**{parsed['name'] or 'Unknown'}** — {row['Category']}", expanded=False
    ):
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("**Contact**")
            st.write(f"Email: {parsed['email'] or '—'}")
            st.write(f"Phone: {parsed['phone'] or '—'}")
            st.write(f"LinkedIn: {parsed['linkedin'] or '—'}")
            st.divider()
            st.markdown("**Education**")
            for edu in parsed["education"]:
                st.write(f"- {edu['degree']} {edu['year']}")
        with c2:
            st.markdown("**Skills**")
            if parsed["skills"]:
                st.markdown(skill_badges(parsed["skills"]), unsafe_allow_html=True)
            else:
                st.write("—")
            st.divider()
            st.markdown("**Summary**")
            st.write(parsed["summary"])

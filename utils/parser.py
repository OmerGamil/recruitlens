import streamlit as st
import spacy


@st.cache_resource(show_spinner=False)
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        st.error(
            "spaCy model not found. Run: `python -m spacy download en_core_web_sm`"
        )
        return None

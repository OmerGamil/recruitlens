"""
Optional lightweight password gate for Streamlit deployments.

Usage in any page:
    from auth import require_auth
    require_auth()

Set RECRUITLENS_PASSWORD in your environment or Streamlit secrets to enable.
If the variable is not set, the gate is bypassed (open access).
"""
import os
import streamlit as st


def require_auth() -> None:
    password = os.environ.get("RECRUITLENS_PASSWORD") or st.secrets.get(
        "RECRUITLENS_PASSWORD", ""
    )
    if not password:
        return  # no password configured → open access

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return

    st.title("RecruitLens — Login")
    entered = st.text_input("Password", type="password")
    if st.button("Login"):
        if entered == password:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

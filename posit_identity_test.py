import os
import streamlit as st

st.set_page_config(
    page_title="TRF Posit Identity Test",
    page_icon="👤"
)

st.title("TRF - Posit Identity Test")

st.write("Checking user information provided by Posit Connect...")

possible_user_vars = [
    "CONNECT_USER",
    "RSTUDIO_CONNECT_USER",
    "REMOTE_USER",
    "USERNAME",
    "USER",
]

found = False

for name in possible_user_vars:
    value = os.getenv(name)

    if value:
        st.write(f"**{name}:** {value}")
        found = True

if not found:
    st.warning("No Posit user environment variable detected.")

st.divider()

st.subheader("Safe environment check")

interesting_vars = []

for name, value in os.environ.items():
    upper = name.upper()

    if any(
        keyword in upper
        for keyword in ["CONNECT", "USER", "EMAIL", "REMOTE"]
    ):
        interesting_vars.append((name, value))

if interesting_vars:
    for name, value in sorted(interesting_vars):
        st.code(f"{name} = {value}")
else:
    st.info("No relevant user variables found.")
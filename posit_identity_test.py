import json
import streamlit as st

st.set_page_config(
    page_title="TRF Posit Identity Test",
    page_icon="👤"
)

st.title("TRF - Posit Identity Test")

credentials = st.context.headers.get(
    "Rstudio-Connect-Credentials"
)

if not credentials:
    st.error("Posit authenticated user not detected")
    st.stop()

user_info = json.loads(credentials)

username = user_info.get("user", "")
groups = user_info.get("groups", [])

st.success("Authenticated Posit user detected")

st.subheader("Current User")
st.write("Username:")
st.code(username)

st.subheader("Groups")

if groups:
    st.write(f"Groups detected: {len(groups)}")

    for group in groups:
        st.write(f"• {group}")
else:
    st.warning("No group information returned")
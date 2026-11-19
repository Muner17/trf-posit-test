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

if credentials:
    try:
        user = json.loads(credentials)

        st.success("Authenticated Posit user detected")

        st.write("Username")
        st.code(user.get("user", "Not available"))

        # Safe diagnostic: show field names only
        st.write("Available user fields")
        st.write(list(user.keys()))

    except Exception as e:
        st.error(f"Unable to read Posit user information: {e}")
else:
    st.warning("Authenticated user information was not detected.")
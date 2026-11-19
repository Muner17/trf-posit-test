import os
import requests
import streamlit as st

from posit import connect

st.set_page_config(
    page_title="TRF SharePoint Test",
    page_icon="🔎"
)

st.title("TRF - Employee Directory Test")

SITE_URL = "https://azcollaboration.sharepoint.com/sites/TSN141"
LIST_NAME = "TRF_EmployeeDirectory"


# -------------------------
# Get SharePoint token
# -------------------------

if os.getenv("POSIT_PRODUCT") == "CONNECT":

    client = connect.Client()

    session_token = st.context.headers.get(
        "Posit-Connect-User-Session-Token"
    )

    if not session_token:
        st.error("Posit user session token not found.")
        st.stop()

    try:
        credentials = client.oauth.get_credentials(
            session_token
        )

        access_token = credentials.get("access_token")

    except Exception as e:
        st.error("SharePoint integration is not available.")
        st.code(str(e))
        st.stop()

else:
    st.warning("This test must run on Posit Connect.")
    st.stop()


if not access_token:
    st.error("No SharePoint access token returned.")
    st.stop()


# -------------------------
# Search Traveller
# -------------------------

search_text = st.text_input(
    "Search Traveller",
    placeholder="Name, PRID or email"
)

if search_text:

    safe_search = search_text.replace("'", "''")

    url = (
        f"{SITE_URL}/_api/web/lists/"
        f"getbytitle('{LIST_NAME}')/items"
    )

    params = {
        "$select":
            "Title,DisplayName,Email,"
            "UserPrincipalName,JobTitle,"
            "Department,Country,OfficeLocation",

        "$filter":
            f"substringof('{safe_search}',Title) "
            f"or substringof('{safe_search}',DisplayName) "
            f"or substringof('{safe_search}',Email)",

        "$top": "10"
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json;odata=nometadata"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    if response.status_code == 200:

        employees = response.json().get("value", [])

        if not employees:
            st.warning("No employee found.")

        else:

            st.success(
                f"Found {len(employees)} employee(s)"
            )

            for emp in employees:

                st.subheader(
                    emp.get("DisplayName", "")
                )

                st.write(
                    f"**PRID:** {emp.get('Title', '')}"
                )

                st.write(
                    f"**Email:** {emp.get('Email', '')}"
                )

                st.write(
                    f"**Job Title:** "
                    f"{emp.get('JobTitle', '')}"
                )

                st.write(
                    f"**Department:** "
                    f"{emp.get('Department', '')}"
                )

                st.divider()

    else:

        st.error(
            f"SharePoint error: "
            f"{response.status_code}"
        )

        st.code(response.text)
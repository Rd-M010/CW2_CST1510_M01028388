import streamlit as st

st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    layout="wide"
)

st.title("🏠 Multi-Domain Intelligence Platform")

# IF 1 — user NOT logged in
if not st.session_state.get("logged_in", False):
    st.markdown(
        """
        Welcome to the Multi-Domain Intelligence Platform.

        Please log in to access:
        - Cybersecurity
        - Data Science
        - IT Operations
        - AI Assistant
        """
    )

    st.info("Go to the Login page to continue.")
    st.stop()

# IF 2 — user IS logged in
st.success(f"Welcome back {st.session_state.current_user}")

st.markdown(
    """
    Use the sidebar to navigate:
    - Cybersecurity
    - Data Science
    - IT Operations
    - AI Assistant
    """
)

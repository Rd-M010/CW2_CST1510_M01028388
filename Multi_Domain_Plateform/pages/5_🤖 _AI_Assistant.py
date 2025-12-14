import streamlit as st

st.set_page_config(
    page_title="AI Assistant",
    layout="wide"
)

import sys
from pathlib import Path

# We ensure the project root is available for imports
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


from services.ai_assistant import ai_assistant_box


# We block access if the user is not logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in.")
    st.stop()


# We detect the current AI domain
ai_domain = st.session_state.get("ai_domain", "General")


st.title("🤖 AI Assistant")


# We adapt the subtitle depending on the domain
if ai_domain == "Cyber Security":
    st.caption("Analyse security incidents and provide response recommendations")

elif ai_domain == "Data Science":
    st.caption("Analyse datasets and provide data-driven insights")

elif ai_domain == "IT Operations":
    st.caption("Support IT operations and incident resolution")

else:
    st.caption("Ask questions and get intelligent insights")


# We show the selected context if available
if "ai_context_title" in st.session_state:
    st.subheader(st.session_state["ai_context_title"])

if "ai_context_description" in st.session_state:
    st.info(st.session_state["ai_context_description"])
else:
    st.info("No context selected. You can ask a general question.")


st.divider()


# We display the chat interface
ai_assistant_box()

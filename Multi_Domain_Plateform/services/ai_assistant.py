import streamlit as st
from openai import OpenAI


def get_openai_client():
    """
    Create OpenAI client using Streamlit secrets
    """
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("OpenAI API key not found in secrets.toml")
        st.stop()

    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def generate_ai_response(user_question, incident_context=None):
    """
    Send user question + optional incident context to OpenAI
    """

    client = get_openai_client()

    system_prompt = (
        "You are a cybersecurity assistant. "
        "You analyse incidents and give clear, professional advice."
    )

    if incident_context:
        system_prompt += f" Incident context: {incident_context}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


def ai_assistant_box():
    """
    Streamlit chat UI for the AI assistant
    """

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask a cybersecurity question")

    if st.button("Send"):
        if user_input.strip() != "":
            incident_context = st.session_state.get(
                "ai_context_description", None
            )

            ai_reply = generate_ai_response(
                user_input,
                incident_context
            )

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", ai_reply))

    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**AI Assistant:** {message}")

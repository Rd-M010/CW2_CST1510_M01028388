import streamlit as st
from openai import OpenAI

# I load the API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# We show the page title
st.title("🤖 AI Assistant")

# I let the user type a message
user_input = st.text_area("Ask something:", "")

# When we press the button, we send the request
if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please type a question first.")
    else:
        try:
            # We send the message to the AI model
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant inside a Streamlit app."},
                    {"role": "user", "content": user_input}
                ]
            )

            # I take the model's response
            answer = response.choices[0].message["content"]

            # We show the answer
            st.success("AI Response:")
            st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")

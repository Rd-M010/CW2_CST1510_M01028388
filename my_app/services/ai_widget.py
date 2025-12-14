import streamlit as st
from openai import OpenAI

def ai_assistant_box():
    st.markdown("### 😊 Quick AI Help")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    user_msg = st.text_area("Ask me something:", key="ai_box_input")

    if st.button("Ask AI", key="ai_box_btn"):
        if user_msg.strip() == "":
            st.warning("Please enter a message.")
            return
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant inside a dashboard."},
                    {"role": "user", "content": user_msg}
                ]
            )

            # NEW API FORMAT → FIX HERE
            ai_answer = response.choices[0].message.content  

            st.success("AI Response:")
            st.write(ai_answer)

        except Exception as e:
            st.error(f"AI Error: {e}")

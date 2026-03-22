import streamlit as st
from openai import OpenAI

st.title("FinLitAI Tutor NG 🇳🇬")
st.write("Your personal money teacher! Ask in Pidgin or English.")

# Use secrets for API key
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("E.g., 'How I go save money?'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are FinLitAI, friendly Nigerian youth financial tutor. Use Pidgin or simple English. Teach saving, budgeting, scams."}
            ] + st.session_state.messages,
            stream=True
        )
        full = ""
        placeholder = st.empty()
        for chunk in response:
            if chunk.choices[0].delta.content:
                full += chunk.choices[0].delta.content
                placeholder.markdown(full + "▌")
        placeholder.markdown(full)
    st.session_state.messages.append({"role": "assistant", "content": full})

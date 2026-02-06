import streamlit as st
from openai import OpenAI
import os

# 1. Page Setup
st.set_page_config(page_title="Hamza AI Assistant", page_icon="🤖")

# 2. DeepSeek Setup
# Streamlit Secrets mein ab API_KEY ka naam 'DEEPSEEK_API_KEY' rakh dein
if "DEEPSEEK_API_KEY" in st.secrets:
    client = OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com" # DeepSeek ka rasta
    )
else:
    st.error("Secrets mein DEEPSEEK_API_KEY nahi mili!")
    st.stop()

# 3. Sidebar
with st.sidebar:
    st.header("👤 Creator Details")
    st.write("Master: **Sultan Muhammad Hamza Hameed**")
    if os.path.exists("hamza.jpg.jpeg"):
        st.image("hamza.jpg.jpeg")

# 4. Chat Logic
st.title("🤖 Hamza AI (Powered by DeepSeek)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Hamza bhai, kuch poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a loyal assistant to Sultan Muhammad Hamza Hameed."},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")

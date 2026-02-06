import streamlit as st
from google import genai
import os

# 1. Page Config
st.set_page_config(page_title="Hamza AI Assistant", page_icon="🤖")

# 2. Setup Client with New Library
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets mein GEMINI_API_KEY nahi mili!")
    st.stop()

# 3. Sidebar Details
with st.sidebar:
    st.header("👤 Creator Details")
    st.write("Master: **Sultan Muhammad Hamza Hameed**")
    photo_path = "hamza.jpg.jpeg" if os.path.exists("hamza.jpg.jpeg") else "hamza.jpg"
    if os.path.exists(photo_path):
        st.image(photo_path)

st.title("🤖 Hamza AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. New Stable Chat Logic
if prompt := st.chat_input("Hamza bhai, kuch poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Google GenAI library ka naya tareeqa
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            
            reply = response.text
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Nayi Library Error: {e}")

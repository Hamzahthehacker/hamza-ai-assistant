import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Hamza AI", page_icon="🤖")

# 2. API Key Check
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key nahi mili! Settings > Secrets check karein.")
    st.stop()

# 3. Sidebar Setup
with st.sidebar:
    st.header("Creator")
    st.write("Master: **Sultan Muhammad Hamza Hameed**")
    # Photo logic
    if os.path.exists("hamza.jpg.jpeg"):
        st.image("hamza.jpg.jpeg", caption="Sultan Muhammad Hamza Hameed")
    elif os.path.exists("hamza.jpg"):
        st.image("hamza.jpg", caption="Sultan Muhammad Hamza Hameed")

# 4. Chat UI
st.title("🤖 Hamza AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Chat Input & Response
if prompt := st.chat_input("Hamza bhai, kuch poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Hum 'gemini-1.5-flash' use kar rahe hain
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

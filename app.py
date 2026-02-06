import streamlit as st
import os
from google import genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Hamza AI Assistant", page_icon="🤖", layout="wide")

# 2. System Prompt
SYSTEM_PROMPT = "You are 'Hamza AI', a loyal assistant to Sultan Muhammad Hamza Hameed. Talk in Urdu/English mix."

# 3. Load API Key
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Secrets mein GEMINI_API_KEY nahi mili!")
    st.stop()

# 4. Initialize Client
client = genai.Client(api_key=API_KEY)

# 5. Sidebar
with st.sidebar:
    st.header("👤 Creator Details")
    st.write("Master: **Sultan Muhammad Hamza Hameed**")
    photo_path = "hamza.jpg.jpeg" if os.path.exists("hamza.jpg.jpeg") else "hamza.jpg"
    if os.path.exists(photo_path):
        st.image(photo_path, caption="Hamza Hameed")

# 6. Main UI
st.title("🤖 Hamza AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. Chat Input (Variable fixed here)
user_prompt = st.chat_input("Hamza bhai, kuch poochein...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            # Stable Model Name for 2026
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=user_prompt
            )
            reply = response.text
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")

import streamlit as st
import os
from google import genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Hamza AI Assistant", page_icon="🤖", layout="wide")

# 2. Key Check
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Secrets mein API Key nahi mili!")
    st.stop()

# 3. Client Setup
client = genai.Client(api_key=API_KEY)

# 4. Sidebar
with st.sidebar:
    st.header("👤 Creator Details")
    st.write("Master: **Sultan Muhammad Hamza Hameed**")
    photo_path = "hamza.jpg.jpeg" if os.path.exists("hamza.jpg.jpeg") else "hamza.jpg"
    if os.path.exists(photo_path):
        st.image(photo_path, caption="Hamza Hameed")

st.title("🤖 Hamza AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Fixed Chat Logic
user_prompt = st.chat_input("Hamza bhai, kuch poochein...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            # Hamza bhai, yahan model name bilkul aise hi likhna hai
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=user_prompt
            )
            reply = response.text
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            # Agar phir bhi 404 aaye to hum model name update karenge
            st.error(f"Error: {e}")

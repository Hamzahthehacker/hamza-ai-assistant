import streamlit as st
import google.generativeai as genai
import os

# 1. Page Config
st.set_page_config(page_title="Hamza AI Assistant", page_icon="🤖")

# 2. Setup API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets mein GEMINI_API_KEY nahi mili!")
    st.stop()

# 3. Sidebar
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

# 4. v1beta Model Implementation
if prompt := st.chat_input("Hamza bhai, v1beta se poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Hum ne model ka pura path 'models/gemini-1.5-flash' diya hai
            # Jo v1beta API ke liye standard hai
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            
            # Yahan hum explicit model call kar rahe hain
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Model ne response generate nahi kiya, dobara koshish karein.")
        except Exception as e:
            st.error(f"v1beta Error: {e}")

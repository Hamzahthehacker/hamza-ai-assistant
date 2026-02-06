import streamlit as st
import google.generativeai as genai
import os

# 1. Page Config
st.set_page_config(page_title="Hamza AI Assistant", page_icon="🤖")

# 2. Setup API Key
if "GEMINI_API_KEY" in st.secrets:
    # Purana stable method
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

# 4. Chat UI
st.title("🤖 Hamza AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Fixed Chat Logic
if prompt := st.chat_input("Hamza bhai, kuch poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Model initialization yahan karein
            model = genai.GenerativeModel('gemini-1.5-flash')
            # generate_content ka sab se simple tareeqa
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("AI ne khali jawab diya hai.")
        except Exception as e:
            st.error(f"Error: {e}")

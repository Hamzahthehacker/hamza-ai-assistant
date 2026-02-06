import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="Hamza AI", page_icon="🤖")

# API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets mein key nahi mili!")
    st.stop()

st.title("🤖 Hamza AI Assistant")
st.write("Created by: Sultan Muhammad Hamza Hameed")

# Initialize Model
model = genai.GenerativeModel('gemini-1.5-flash')

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
if prompt := st.chat_input("Hamza bhai, kuch poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Direct generation
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

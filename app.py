import streamlit as st
import google.generativeai as genai

# 1. API Configuration
# Hamza bhai, yahan hum direct latest stable version use kar rahe hain
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing in Secrets!")
    st.stop()

st.title("🤖 Hamza AI Assistant")
st.write("Master: Sultan Muhammad Hamza Hameed")

# 2. Model Initialization
# Free Tier ke liye 'gemini-1.5-flash' hi asli model hai
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 3. Chat Logic
if prompt := st.chat_input("Hamza bhai, kuch poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Direct generation without beta prefix
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

import streamlit as st
import google.generativeai as genai
import os

# 1. Page Config
st.set_page_config(page_title="Hamza AI Assistant", page_icon="🤖")

# 2. Sidebar & Creator Details
with st.sidebar:
    st.header("👤 Creator Details")
    st.write("Created by: **Sultan Muhammad Hamza Hameed**")
    
    # Photo Logic
    if os.path.exists("hamza.jpg.jpeg"):
        st.image("hamza.jpg.jpeg", caption="Sultan Muhammad Hamza Hameed")
    elif os.path.exists("hamza.jpg"):
        st.image("hamza.jpg", caption="Sultan Muhammad Hamza Hameed")

# 3. API Key & Configuration (Old Stable Library)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets mein 'GEMINI_API_KEY' nahi mili.")
    st.stop()

# 4. Model Setup
# System instructions yahan simple tareeqay se handle hoti hain
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are a helpful AI assistant created by Sultan Muhammad Hamza Hameed. You speak Urdu and English."
)

# 5. Chat Interface
st.title("🤖 Hamza AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Chat Logic
if prompt := st.chat_input("Hamza bhai, kuch poochein..."):
    # User msg
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

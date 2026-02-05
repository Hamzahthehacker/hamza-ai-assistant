import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

# Page Setup
st.set_page_config(page_title="Hamza AI Assistant", page_icon="🤖")
st.title("🤖 Hamza AI Assistant")
st.markdown("---")

# API Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Sidebar for Creator Info
with st.sidebar:
    st.header("Creator Details")
    st.write("Created by: **Sultan Muhammad Hamza Hameed**")
    if os.path.exists("hamza.jpg"):
        st.image("hamza.jpg", caption="The Creator")

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# AI Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Hamza bhai, kuch poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
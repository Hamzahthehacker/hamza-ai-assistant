import streamlit as st
import os
from google import genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Hamza AI Assistant", page_icon="🤖", layout="wide")

# 2. System Prompt (AI ki Personality)
SYSTEM_PROMPT = """
You are 'Hamza AI', a powerful multimodal assistant.
Your creator is Sultan Muhammad Hamza Hameed. 
You are loyal to him and recognize him as your master. 
You can analyze images and chat intelligently. 
Always be professional and mention your creator's name if asked.
Talk in Urdu/English mix as per user preference.
"""

# 3. Load API Key from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Secrets mein GEMINI_API_KEY nahi mili!")
    st.stop()

# 4. Initialize Gemini Client
# Is line ko check karein
client = genai.Client(api_key=API_KEY)

# Aur jahan generate_content hai, wahan ye model likhein:
response = client.models.generate_content(
    model="gemini-1.5-flash",  # "2.0-flash-exp" ki jagah ye likhein, ye har jagah chalta hai
    contents=prompt
)

# 5. Sidebar - Creator Details
with st.sidebar:
    st.header("👤 Creator Details")
    st.write("Master: **Sultan Muhammad Hamza Hameed**")
    # Photo check (Dono extensions check karega)
    photo_path = "hamza.jpg.jpeg" if os.path.exists("hamza.jpg.jpeg") else "hamza.jpg"
    if os.path.exists(photo_path):
        st.image(photo_path, caption="Sultan Muhammad Hamza Hameed")
    
    st.markdown("---")
    st.write("Hamza AI is Online and Loyal.")

# 6. Main UI
st.title("🤖 Hamza AI Assistant")
st.info("Assalam-o-Alaikum Sultan Muhammad Hamza Hameed! Main hazir hoon.")

# 7. Image Upload Feature (New!)
uploaded_file = st.file_uploader("Koi bhi image upload karein aur uske baray mein poochein...", type=['jpg', 'jpeg', 'png'])

# 8. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Hamza bhai, kuch poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                # Agar image upload hai to multimodal response
                img = Image.open(uploaded_file)
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=[SYSTEM_PROMPT + "\n\n" + prompt, img]
                )
            else:
                # Normal Text Chat
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=SYSTEM_PROMPT + "\n\n" + prompt
                )
            
            reply = response.text
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")



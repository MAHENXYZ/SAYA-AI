import streamlit as st
from groq import Groq
import os

# Mengambil API Key dari sistem rahasia (Streamlit Secrets)
# Ini penting agar Key Anda tidak dicuri orang di GitHub
api_key_rahasia = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key_rahasia)

# --- TAMPILAN GAYA GEMINI ---
st.set_page_config(page_title="My Private Gemini", page_icon="🔵", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #131314; color: white; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔵 My Private Gemini")
st.info("AI ini sekarang sudah siap untuk dideploy ke internet!")

# --- MEMORI CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- PROSES CHAT ---
if prompt := st.chat_input("Tanya apa saja..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Menggunakan model terbaru yang sudah terbukti jalan di laptop Anda
        chat_completion = client.chat.completions.create(
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            model="llama-3.3-70b-versatile",
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
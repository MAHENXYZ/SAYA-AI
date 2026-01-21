import streamlit as st
from groq import Groq
import json
import os
import time
import hashlib
from pypdf import PdfReader
import pandas as pd

# [CONFIG] Konfigurasi Dasar
st.set_page_config(page_title="Flow Intelligence", page_icon="✨", layout="wide")

# [STYLING] Sistem Desain Obsidian Gold
def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;600&display=swap');
    :root { --accent-gold: #C5A059; --dark-obsidian: #0A0A0A; }
    .stApp { background-color: var(--dark-obsidian); color: #F5F5F7; font-family: 'Inter', sans-serif; }
    .nav-brand { font-family: 'Instrument Serif', serif; font-size: 32px; color: var(--accent-gold); }
    div.stButton > button { background: transparent; color: var(--accent-gold); border: 1px solid var(--accent-gold); }
    div.stButton > button:hover { background: var(--accent-gold); color: black; }
    </style>
    """, unsafe_allow_html=True)

# [SESSION] Inisialisasi Memori
if "init" not in st.session_state:
    st.session_state.update({
        "init": True, "memory": [], "authenticated": False, 
        "user_prefs": {"bio": "", "verbosity": "Balanced"}, "doc_context": ""
    })

# [AUTH] Gerbang Keamanan
def check_auth():
    if not st.session_state.authenticated:
        st.markdown("<div style='text-align:center'><h1 class='nav-brand'>NEURAL VAULT</h1></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            key = st.text_input("ACCESS KEY", type="password")
            if st.button("INITIALIZE SCAN", use_container_width=True):
                if key == "ADMIN": # Ganti password di sini
                    st.session_state.authenticated = True
                    st.rerun()
                else: st.error("Access Denied")
        return False
    return True

# [MAIN] Eksekusi Aplikasi
def main():
    apply_styles()
    if not check_auth(): return

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="nav-brand">FLOW.AI</div>', unsafe_allow_html=True)
        model = st.selectbox("Intelligence", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        
        with st.expander("👤 PROFILE"):
            bio = st.text_area("User Bio", st.session_state.user_prefs["bio"])
            if st.button("Save"): st.session_state.user_prefs["bio"] = bio
            
        pdf = st.file_uploader("Knowledge (PDF)", type="pdf")
        if pdf:
            reader = PdfReader(pdf)
            st.session_state.doc_context = "\n".join([p.extract_text() for p in reader.pages])
            st.success("Synced")

    # Chat UI
    for msg in st.session_state.memory:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Command the Intelligence..."):
        st.session_state.memory.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        try:
            # Menggunakan API Key dari Streamlit Secrets
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            full_prompt = f"Context: {st.session_state.doc_context[:1000]}\nUser Bio: {st.session_state.user_prefs['bio']}\n\nQuestion: {prompt}"
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": full_prompt}]
            ).choices[0].message.content
            
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.memory.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}. Pastikan 'GROQ_API_KEY' sudah diatur di Secrets Streamlit.")

if __name__ == "__main__":
    main()
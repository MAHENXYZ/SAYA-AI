import streamlit as st
from groq import Groq
import base64
import time
import json
import os
import hashlib
import pandas as pd
from datetime import datetime
from PIL import Image
import io
from pypdf import PdfReader

# =============================================================================
# [CORE-01] INITIAL CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Flow Intelligence | Elite AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# [CORE-02] LUXURY DESIGN SYSTEM
# =============================================================================
def apply_global_design_system():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;600&display=swap');
    :root {
        --accent-gold: #C5A059;
        --dark-obsidian: #0A0A0A;
        --soft-white: #F5F5F7;
        --glass-bg: rgba(255, 255, 255, 0.03);
    }
    .stApp { background-color: var(--dark-obsidian); color: var(--soft-white); font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid rgba(197, 160, 89, 0.1); }
    .nav-brand { font-family: 'Instrument Serif', serif; font-size: 32px; color: var(--accent-gold); letter-spacing: -0.5px; }
    .assistant-header { font-family: 'Instrument Serif', serif; font-size: 1.5rem; color: var(--accent-gold); font-style: italic; }
    .content-body { font-size: 1.1rem; line-height: 1.7; color: rgba(255, 255, 255, 0.85); }
    </style>
    <script>
    const synth = window.speechSynthesis;
    window.speak = (text) => {
        if (synth.speaking) synth.cancel();
        const uttr = new SpeechSynthesisUtterance(text);
        uttr.rate = 1.05;
        synth.speak(uttr);
    };
    window.stopSpeaking = () => synth.cancel();
    </script>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-03] SESSION & DATABASE MANAGEMENT
# =============================================================================
if "init" not in st.session_state:
    st.session_state.update({
        "init": True, "memory": [], "authenticated": False, "start_time": time.time(),
        "user_prefs": {"bio": "", "verbosity": "Balanced"}, "doc_context": ""
    })

def save_to_local_db():
    data = {"memory": st.session_state.memory, "user_prefs": st.session_state.user_prefs}
    with open("neural_storage.json", "w") as f:
        json.dump(data, f)

# =============================================================================
# [CORE-04] SECURITY VAULT
# =============================================================================
def check_neural_vault():
    if not st.session_state.authenticated:
        st.markdown("<br><br><div style='text-align:center'><div class='nav-brand'>NEURAL VAULT</div></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            key = st.text_input("ACCESS KEY", type="password")
            if st.button("INITIALIZE SCAN", use_container_width=True):
                if key == "ADMIN": # Password Default
                    st.session_state.authenticated = True
                    st.rerun()
                else: st.error("Invalid Signature")
        return False
    return True

# =============================================================================
# [CORE-05] MAIN PRODUCTION ENTRY
# =============================================================================
def main():
    apply_global_design_system()
    
    if check_neural_vault():
        # Sidebar Elements
        with st.sidebar:
            st.markdown('<div class="nav-brand">FLOW.AI</div>', unsafe_allow_html=True)
            model_option = st.selectbox("Cognitive Engine", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
            
            with st.expander("👤 NEURAL PROFILE"):
                bio = st.text_area("User Bio", value=st.session_state.user_prefs["bio"])
                if st.button("Update Profile"):
                    st.session_state.user_prefs["bio"] = bio
                    save_to_local_db()
            
            pdf_file = st.file_uploader("Upload Knowledge (PDF)", type="pdf")
            if pdf_file:
                reader = PdfReader(pdf_file)
                st.session_state.doc_context = "\n".join([p.extract_text() for p in reader.pages])
                st.sidebar.success("PDF Context Injected")

            if st.button("Purge Memory", use_container_width=True):
                st.session_state.memory = []
                save_to_local_db()
                st.rerun()

        # Chat Interface
        for i, msg in enumerate(st.session_state.memory):
            if msg["role"] == "user":
                st.markdown(f'<div style="text-align:right; margin-bottom:20px;">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-header">Intelligence Response</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="content-body">{msg["content"]}</div>', unsafe_allow_html=True)
                # Voice Button
                if st.button("🔊", key=f"v_{i}"):
                    st.components.v1.html(f"<script>window.parent.speak(`{msg['content'][:500]}`)</script>")

        # Input Logic
        if prompt := st.chat_input("Command the Intelligence..."):
            st.session_state.memory.append({"role": "user", "content": prompt})
            
            # API Call
            try:
                client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "YOUR_KEY_HERE"))
                context = f"User context: {st.session_state.user_prefs['bio']}. Doc Context: {st.session_state.doc_context[:1000]}"
                
                response = client.chat.completions.create(
                    model=model_option,
                    messages=[{"role": "system", "content": context}, {"role": "user", "content": prompt}]
                ).choices[0].message.content
                
                # Image Detection (Simulation)
                if "gambar" in prompt.lower():
                    st.image(f"https://image.pollinations.ai/prompt/{prompt}?nologo=true")

                st.session_state.memory.append({"role": "assistant", "content": response})
                save_to_local_db()
                st.rerun()
            except Exception as e:
                st.error(f"Neural Engine Error: {str(e)}")

if __name__ == "__main__":
    main()
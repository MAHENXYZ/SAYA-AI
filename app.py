import streamlit as st
from groq import Groq
import base64, time, json, os, hashlib, re
import pandas as pd
from datetime import datetime
from pypdf import PdfReader

# =============================================================================
# [01] GLOBAL CONFIGURATION & DESIGN
# =============================================================================
st.set_page_config(page_title="Flow Intelligence | Elite AI", page_icon="✨", layout="wide")

def apply_all_styles():
    """Menggabungkan semua estetika Obsidian Gold ke dalam satu injeksi CSS."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;600&display=swap');
    :root { --accent-gold: #C5A059; --dark-obsidian: #0A0A0A; --glass-bg: rgba(255, 255, 255, 0.03); }
    
    .stApp { background: radial-gradient(circle at 0% 0%, rgba(197, 160, 89, 0.03) 0%, transparent 50%), #050505; color: #F5F5F7; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #020202 !important; border-right: 1px solid rgba(197, 160, 89, 0.1); }
    .nav-brand { font-family: 'Instrument Serif', serif; font-size: 32px; color: var(--accent-gold); letter-spacing: -0.5px; }
    .assistant-header { font-family: 'Instrument Serif', serif; font-size: 1.5rem; color: var(--accent-gold); font-style: italic; margin-top: 20px; }
    .content-body { font-size: 1.1rem; line-height: 1.7; color: rgba(255, 255, 255, 0.85); animation: fadeIn 0.8s ease-out; }
    
    /* Metrics & Progress */
    [data-testid="stMetricValue"] { font-family: 'Instrument Serif', serif !important; color: var(--accent-gold) !important; }
    div[role="progressbar"] > div { background-color: var(--accent-gold) !important; }
    
    /* Buttons */
    div.stButton > button { background: transparent; color: var(--accent-gold); border: 1px solid rgba(197, 160, 89, 0.3); transition: 0.4s; border-radius: 8px; }
    div.stButton > button:hover { background: var(--accent-gold); color: black; box-shadow: 0 0 15px rgba(197, 160, 89, 0.3); transform: translateX(5px); }
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    
    <script>
    const synth = window.speechSynthesis;
    window.speak = (t) => { if(synth.speaking) synth.cancel(); const u = new SpeechSynthesisUtterance(t); u.rate=1.05; synth.speak(u); };
    window.stopSpeaking = () => synth.cancel();
    </script>
    """, unsafe_allow_html=True)

# =============================================================================
# [02] CORE ENGINES (DATABASE & AUTH)
# =============================================================================
class NeuralCore:
    @staticmethod
    def init_session():
        if "init" not in st.session_state:
            st.session_state.update({
                "init": True, "memory": [], "authenticated": False, "start_time": time.time(),
                "user_prefs": {"bio": "", "verbosity": "Balanced"}, "doc_context": ""
            })
            if os.path.exists("neural_storage.json"):
                with open("neural_storage.json", "r") as f:
                    data = json.load(f)
                    st.session_state.memory = data.get("memory", [])
                    st.session_state.user_prefs = data.get("user_prefs", {})

    @staticmethod
    def save_db():
        with open("neural_storage.json", "w") as f:
            json.dump({"memory": st.session_state.memory, "user_prefs": st.session_state.user_prefs}, f)

    @staticmethod
    def check_auth():
        if not st.session_state.authenticated:
            st.markdown("<br><br><div style='text-align:center'><div class='nav-brand'>NEURAL VAULT</div><p style='letter-spacing:5px; font-size:10px; color:#C5A059'>SECURE ACCESS v4.0</p></div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                key = st.text_input("ACCESS KEY", type="password")
                if st.button("INITIALIZE SCAN", use_container_width=True):
                    if key == "ADMIN": # Password Anda
                        st.session_state.authenticated = True
                        st.rerun()
                    else: st.error("Access Denied")
            st.stop()

# =============================================================================
# [03] SIDEBAR & TOOLS
# =============================================================================
def render_neural_sidebar():
    with st.sidebar:
        st.markdown('<div class="nav-brand">FLOW.AI</div>', unsafe_allow_html=True)
        
        # Model & Persona
        model = st.selectbox("Intelligence", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        with st.expander("👤 IDENTITY"):
            bio = st.text_area("Bio", st.session_state.user_prefs["bio"])
            verb = st.select_slider("Detail", ["Concise", "Balanced", "Extensive"], value=st.session_state.user_prefs["verbosity"])
            if st.button("UPDATE"):
                st.session_state.user_prefs.update({"bio": bio, "verbosity": verb})
                NeuralCore.save_db()

        # Knowledge RAG
        st.write("---")
        pdf = st.file_uploader("Upload PDF Intelligence", type="pdf")
        if pdf:
            reader = PdfReader(pdf)
            st.session_state.doc_context = "\n".join([p.extract_text() for p in reader.pages])
            st.success("Context Loaded")

        # HUD Metrics
        st.write("---")
        st.metric("UPTIME", f"{int(time.time() - st.session_state.start_time)}s")
        st.progress(min(len(st.session_state.memory) * 10, 100))
        
        if st.button("PURGE PATHWAYS", use_container_width=True):
            st.session_state.memory = []
            NeuralCore.save_db()
            st.rerun()
            
    return model

# =============================================================================
# [04] MAIN INTERFACE & LOGIC
# =============================================================================
def main():
    apply_all_styles()
    NeuralCore.init_session()
    NeuralCore.check_auth()
    
    selected_model = render_neural_sidebar()
    
    # Render Chat History
    for i, msg in enumerate(st.session_state.memory):
        if msg["role"] == "user":
            st.markdown(f'<div style="text-align:right; margin-bottom:20px;"><span style="background:var(--glass-bg); padding:10px 20px; border-radius:15px; border:1px solid rgba(255,255,255,0.05)">{msg["content"]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-header">Intelligence Response</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-body">{msg["content"]}</div>', unsafe_allow_html=True)
            
            # Audio Controls
            c1, c2, _ = st.columns([0.05, 0.05, 0.9])
            if c1.button("🔊", key=f"s_{i}"): st.components.v1.html(f"<script>window.parent.speak(`{msg['content'][:500]}`)</script>")
            if c2.button("👍", key=f"f_{i}"): st.toast("Learned")

    # Chat Input
    if prompt := st.chat_input("Command the Intelligence..."):
        st.session_state.memory.append({"role": "user", "content": prompt})
        
        # UI Response
        with st.status("Thinking...", expanded=False):
            try:
                # Build context
                ctx = f"User Bio: {st.session_state.user_prefs['bio']}. Style: {st.session_state.user_prefs['verbosity']}. "
                if st.session_state.doc_context: ctx += f"Context: {st.session_state.doc_context[:2000]}"
                
                client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "MASUKKAN_KEY_DI_SINI"))
                res = client.chat.completions.create(
                    model=selected_model,
                    messages=[{"role": "system", "content": ctx}, {"role": "user", "content": prompt}]
                ).choices[0].message.content
                
                # Check for Image Gen
                if "gambar" in prompt.lower() or "imagine" in prompt.lower():
                    st.image(f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true")

                st.session_state.memory.append({"role": "assistant", "content": res})
                NeuralCore.save_db()
                st.rerun()
            except Exception as e:
                st.error(f"Engine Error: {e}")

if __name__ == "__main__":
    main()
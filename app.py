import streamlit as st
from groq import Groq
import json
import time
from pypdf import PdfReader

# [CONFIG] Ultra-Wide Premium Setup
st.set_page_config(
    page_title="NEURAL FLOW | Premium AI", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# [STYLING] Obsidian & Liquid Gold Design System
def apply_premium_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600&family=Playfair+Display:ital@0;1&display=swap');
    
    :root {
        --accent-gold: #D4AF37;
        --deep-black: #050505;
        --glass-white: rgba(255, 255, 255, 0.05);
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #1a1a1a, #050505);
        color: #E0E0E0;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Elegant Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 10, 0.95) !important;
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    /* Typography */
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        background: linear-gradient(90deg, #D4AF37, #FBE7A1, #D4AF37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-style: italic;
        margin-bottom: 0;
    }
    
    .sub-text {
        letter-spacing: 3px;
        font-size: 0.8rem;
        color: var(--accent-gold);
        text-transform: uppercase;
        margin-bottom: 2rem;
    }

    /* Glassmorphism Cards */
    .stChatMessage {
        background: var(--glass-white) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        backdrop-filter: blur(10px);
    }

    /* Gold Buttons */
    div.stButton > button {
        background: linear-gradient(45deg, #D4AF37, #996515);
        color: black !important;
        border: none;
        font-weight: 600;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea {
        background: #0F0F0F !important;
        border: 1px solid #333 !important;
        color: #D4AF37 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# [CORE] Initialize Intelligence Engine
if "memory" not in st.session_state:
    st.session_state.memory = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_auth():
    if not st.session_state.authenticated:
        st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.markdown("<h1 class='hero-title' style='text-align:center'>Vault</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#666'>SYSTEM ACCESS REQUIRED</p>", unsafe_allow_html=True)
            key = st.text_input("ENCRYPTION KEY", type="password", label_visibility="collapsed")
            if st.button("BYPASS FIREWALL", use_container_width=True):
                if key == "LUXE": # Password baru
                    st.session_state.authenticated = True
                    st.rerun()
                else: st.toast("Access Denied: Invalid Protocol", icon="🚫")
        return False
    return True

def main():
    apply_premium_styles()
    if not check_auth(): return

    # --- SIDEBAR NAV ---
    with st.sidebar:
        st.markdown("<h2 class='hero-title' style='font-size:2rem'>Neural Flow</h2>", unsafe_allow_html=True)
        st.markdown("<p class='sub-text'>Intelligence OS v2.0</p>", unsafe_allow_html=True)
        
        st.divider()
        model = st.selectbox("MODEL CORE", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        
        with st.expander("💠 NEURAL BIOMETRICS"):
            bio = st.text_area("Persona", placeholder="Describe yourself...", height=100)
            tone = st.select_slider("Response Depth", options=["Concise", "Balanced", "Sophisticated"])
            
        with st.expander("📚 KNOWLEDGE VAULT"):
            pdf = st.file_uploader("Inject Data (PDF)", type="pdf")
            if pdf:
                with st.spinner("Processing..."):
                    reader = PdfReader(pdf)
                    text = "\n".join([p.extract_text() for p in reader.pages])
                    st.session_state.doc_context = text
                    st.toast("Intelligence Synced", icon="✅")

    # --- CHAT INTERFACE ---
    st.markdown("<p class='sub-text'>System Online</p>", unsafe_allow_html=True)
    
    # Display Chat History
    for msg in st.session_state.memory:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Enter Command..."):
        st.session_state.memory.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # System Prompting (Kunci AI Terlihat Cerdas)
            system_prompt = f"""
            You are 'Flow Intelligence', a sophisticated and elite AI assistant. 
            Tone: Professional, luxurious, and highly insightful.
            User Profile: {bio}
            Context: {st.session_state.get('doc_context', '')[:2000]}
            Complexity Level: {tone}
            """

            full_messages = [
                {"role": "system", "content": system_prompt},
                *st.session_state.memory[-5:] # Kirim 5 pesan terakhir untuk memori
            ]

            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                # Streaming Effect
                completion = client.chat.completions.create(
                    model=model,
                    messages=full_messages,
                    stream=True
                )
                
                for chunk in completion:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                
            st.session_state.memory.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Neural Bridge Failure: {e}")

if __name__ == "__main__":
    main()
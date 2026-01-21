import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. ARCHITECTURAL CONFIGURATION ---
st.set_page_config(
    page_title="FLOW | Strategic Intelligence",
    page_icon="⚪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. WISPR FLOW AESTHETIC (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@200;300;400;500&display=swap');
    
    /* Wispr Flow Foundation */
    .stApp {
        background-color: #000000; /* Atau #FFFFFF jika ingin versi terang */
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    /* Minimalist Header */
    .nav-bar {
        display: flex;
        justify-content: center;
        padding: 40px 0;
        letter-spacing: 8px;
        font-size: 14px;
        font-weight: 200;
        text-transform: uppercase;
        opacity: 0.6;
    }

    /* Wisdom Typography (The Wispr Style) */
    .hero-text {
        font-family: 'Instrument Serif', serif;
        font-size: 64px;
        text-align: center;
        margin: 40px 0;
        background: linear-gradient(180deg, #FFFFFF 0%, #888888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }

    /* Clean Chat Container */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        padding: 1rem 15% !important;
    }

    .stChatMessage [data-testid="stMarkdownContainer"] p {
        font-size: 18px;
        font-weight: 300;
        line-height: 1.6;
        color: #D1D1D1;
    }

    /* User Message Styling (Right Aligned like Wispr) */
    [data-testid="stChatMessage"]:nth-child(even) {
        text-align: right;
        color: #FFFFFF;
    }

    /* Minimalist Input Bar */
    .stChatInputContainer {
        padding: 40px 20% !important;
        background: transparent !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 40px !important; /* Pill shape */
        padding: 10px 20px !important;
    }

    /* Buttons & Utilities */
    .stButton>button {
        background: transparent;
        border: none;
        color: #666;
        font-size: 12px;
        transition: 0.3s;
    }
    .stButton>button:hover { color: #FFF; }

    /* Hide redundant elements */
    header, footer { visibility: hidden; }
    [data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
api_key = st.secrets.get("GROQ_API_KEY", "YOUR_API_KEY")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. MAIN UI ---
st.markdown('<div class="nav-bar">FLOW INTELLIGENCE</div>', unsafe_allow_html=True)

# Tampilan Selamat Datang (Hanya jika chat kosong)
if not st.session_state.messages:
    st.markdown('<div class="hero-text">Think in flow.<br>Speak in wisdom.</div>', unsafe_allow_html=True)

# Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. INTERACTION ---
if prompt := st.chat_input("What is on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Flow, a minimalist and highly intelligent AI. Your answers are deep, poetic yet practical, and very clean."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                full_res += content
                placeholder.markdown(full_res + " ")
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"Error: {e}")
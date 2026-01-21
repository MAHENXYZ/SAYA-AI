import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. PRESTIGE CONFIGURATION ---
st.set_page_config(
    page_title="NEURAL ELITE | Vision Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LUXURY UI ENGINE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@200;300;400;600&display=swap');
    
    :root {
        --accent-gold: #D4AF37;
        --deep-obsidian: #050505;
        --glass-white: rgba(255, 255, 255, 0.03);
        --border-refined: rgba(255, 255, 255, 0.08);
    }

    /* Background & Global Typography */
    .stApp {
        background-color: var(--deep-obsidian);
        background-image: 
            radial-gradient(circle at 10% 10%, rgba(212, 175, 55, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 90% 90%, rgba(212, 175, 55, 0.02) 0%, transparent 50%);
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }

    /* Top Navigation Simulation */
    .nav-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid var(--border-refined);
        margin-bottom: 3rem;
    }

    .brand-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 24px;
        font-weight: 700;
        letter-spacing: -1px;
        color: white;
    }

    .status-pill {
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid var(--accent-gold);
        color: var(--accent-gold);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(8, 8, 8, 0.98) !important;
        border-right: 1px solid var(--border-refined);
    }

    /* Message Aesthetics */
    .chat-bubble {
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid var(--border-refined);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .user-bubble {
        background: var(--glass-white);
    }

    .ai-bubble {
        background: linear-gradient(145deg, rgba(212, 175, 55, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%);
        border-left: 3px solid var(--accent-gold);
    }

    /* Minimalist Input */
    .stChatInputContainer {
        padding: 2rem 5rem !important;
        background: transparent !important;
    }

    div[data-testid="stChatInput"] {
        border: 1px solid var(--border-refined) !important;
        background: rgba(255,255,255,0.02) !important;
        border-radius: 8px !important;
    }

    /* Refined Buttons */
    .stButton>button {
        background: transparent;
        border: 1px solid var(--border-refined);
        color: #888;
        border-radius: 4px;
        font-size: 11px;
        letter-spacing: 1px;
        transition: 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    }

    .stButton>button:hover {
        border-color: var(--accent-gold);
        color: var(--accent-gold);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.1);
    }

    /* Hidden elements for clean look */
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
api_key = st.secrets.get("GROQ_API_KEY", "YOUR_KEY_HERE")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(file):
    return base64.b64encode(file.getvalue()).decode('utf-8')

# --- 4. SIDEBAR DASHBOARD ---
with st.sidebar:
    st.markdown("<div style='padding: 20px 0;'><h2 style='color:white; font-family:Space Grotesk;'>CORE <span style='color:#D4AF37;'>OS</span></h2></div>", unsafe_allow_html=True)
    
    st.caption("MODEL SELECTION")
    model_choice = st.selectbox("Engine", ["llama-3.3-70b-versatile", "llama-3.2-11b-vision-preview"], label_visibility="collapsed")
    
    st.write("---")
    st.caption("VISUAL DATA")
    uploaded_image = st.file_uploader("Upload assets", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    
    if uploaded_image:
        st.image(uploaded_image, use_container_width=True)
        st.markdown("<p style='text-align:center; font-size:10px; color:#555;'>IMAGE LOADED INTO BUFFER</p>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("CLEAR TERMINAL"):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.markdown("""
    <div class="nav-header">
        <div class="brand-title">NEURAL<span style="color:#D4AF37">ELITE</span></div>
        <div class="status-pill">● System Encrypted</div>
    </div>
    """, unsafe_allow_html=True)

# Chat Display
for msg in st.session_state.messages:
    style_class = "user-bubble" if msg["role"] == "user" else "ai-bubble"
    icon = "●"
    color = "white" if msg["role"] == "user" else "#D4AF37"
    
    st.markdown(f"""
        <div class="chat-bubble {style_class}">
            <div style="color:{color}; font-size:10px; font-weight:700; margin-bottom:10px; letter-spacing:1.5px;">
                {msg["role"].upper()}
            </div>
            <div style="font-weight: 300; line-height: 1.7;">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 6. INTERACTION LOGIC ---
if prompt := st.chat_input("Command the AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Logic for Generating Response (Triggered after rerun if last message is user)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar=None): # Hidden default avatar
        placeholder = st.empty()
        full_response = ""
        
        # Determine Mode
        if uploaded_image:
            current_model = "llama-3.2-11b-vision-preview"
            payload = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": st.session_state.messages[-1]["content"]},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(uploaded_image)}"}}
                ]
            }]
        else:
            current_model = model_choice
            payload = [
                {"role": "system", "content": "You are Neural Elite, a professional and highly intelligent AI. Answer with precision and elegance."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ]

        try:
            completion = client.chat.completions.create(
                model=current_model,
                messages=payload,
                stream=True
            )
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                placeholder.markdown(full_response + "▌")
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()
        except Exception as e:
            st.error(f"System Error: {e}")
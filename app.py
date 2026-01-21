import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. ARCHITECTURAL CONFIGURATION ---
st.set_page_config(
    page_title="NEURAL ELITE | Intelligence System",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE PRESTIGE INTERFACE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@200;300;400;500;600&display=swap');
    
    :root {
        --primary-gold: #C5A059; /* Muted Gold */
        --deep-slate: #0D0E12;
        --surface-glass: rgba(255, 255, 255, 0.02);
        --border-silk: rgba(255, 255, 255, 0.06);
    }

    /* Global Foundation */
    .stApp {
        background-color: var(--deep-slate);
        background-image: 
            radial-gradient(circle at 0% 0%, rgba(197, 160, 89, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 100% 100%, rgba(255, 255, 255, 0.02) 0%, transparent 40%);
        color: #F8F9FA;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Professional Navigation Bar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid var(--border-silk);
        margin-bottom: 3rem;
    }

    .nav-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 20px;
        font-weight: 600;
        letter-spacing: 4px;
        text-transform: uppercase;
        background: linear-gradient(90deg, #FFFFFF, #C5A059);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Premium Sidebar */
    [data-testid="stSidebar"] {
        background-color: #08090B !important;
        border-right: 1px solid var(--border-silk);
    }

    /* Refined Chat Interface */
    .chat-wrapper {
        max-width: 900px;
        margin: 0 auto;
    }

    .msg-box {
        padding: 2rem;
        border-radius: 4px; /* Sharp clean edges */
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-silk);
        backdrop-filter: blur(20px);
    }

    .user-msg {
        background: var(--surface-glass);
    }

    .ai-msg {
        background: linear-gradient(to right, rgba(197, 160, 89, 0.03), transparent);
        border-left: 2px solid var(--primary-gold);
    }

    .role-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        color: var(--primary-gold);
        margin-bottom: 12px;
        text-transform: uppercase;
    }

    /* Executive Input Control */
    .stChatInputContainer {
        border-top: 1px solid var(--border-silk) !important;
        padding: 2rem 15% !important;
        background: #0D0E12 !important;
    }

    div[data-testid="stChatInput"] {
        border: 1px solid var(--border-silk) !important;
        border-radius: 4px !important;
        background: rgba(255, 255, 255, 0.01) !important;
    }

    /* Buttons & Interaction */
    .stButton>button {
        background: transparent;
        border: 1px solid var(--primary-gold);
        color: var(--primary-gold);
        border-radius: 2px;
        text-transform: uppercase;
        font-size: 10px;
        padding: 0.5rem 2rem;
        transition: 0.4s;
    }

    .stButton>button:hover {
        background: var(--primary-gold);
        color: black;
    }

    /* Hide redundant UI */
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE INTELLIGENCE ---
api_key = st.secrets.get("GROQ_API_KEY", "YOUR_API_KEY")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_img(file):
    return base64.b64encode(file.getvalue()).decode('utf-8')

# --- 4. SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("<h3 style='letter-spacing:2px; font-weight:300;'>S Y S T E M</h3>", unsafe_allow_html=True)
    st.write("---")
    
    st.caption("NEURAL ENGINE")
    model_choice = st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.2-11b-vision-preview"], label_visibility="collapsed")
    
    st.write("###")
    st.caption("VISUAL DATA INPUT")
    uploaded_image = st.file_uploader("Upload", type=["jpg", "png"], label_visibility="collapsed")
    
    if uploaded_image:
        st.image(uploaded_image, use_container_width=True)
    
    st.write("---")
    if st.button("RESET SESSION"):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN EXECUTIVE INTERFACE ---
st.markdown("""
    <div class="nav-bar">
        <div class="nav-logo">NEURAL ELITE</div>
        <div style="font-size: 10px; color: #555; letter-spacing: 1px;">ENCRYPTED CHANNEL : 0x82A</div>
    </div>
    """, unsafe_allow_html=True)

# Chat History Container
chat_container = st.container()

with chat_container:
    for m in st.session_state.messages:
        msg_type = "user-msg" if m["role"] == "user" else "ai-msg"
        role_name = "Inquiry" if m["role"] == "user" else "Neural Intelligence"
        
        st.markdown(f"""
            <div class="msg-box {msg_type}">
                <div class="role-label">{role_name}</div>
                <div style="font-size: 15px; font-weight: 300; line-height: 1.8; color: #D1D1D1;">
                    {m["content"]}
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 6. COMMAND EXECUTION ---
if prompt := st.chat_input("Command Neural Elite..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Process Response
    with st.chat_message("assistant", avatar=None):
        placeholder = st.empty()
        full_res = ""
        
        # Smart Logic Switch
        if uploaded_image:
            model = "llama-3.2-11b-vision-preview"
            msgs = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_img(uploaded_image)}"}}
                ]
            }]
        else:
            model = model_choice
            msgs = [
                {"role": "system", "content": "You are Neural Elite, an ultra-professional, high-end AI assistant. Your language is sophisticated, clear, and direct."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ]

        try:
            stream = client.chat.completions.create(model=model, messages=msgs, stream=True)
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                full_res += content
                placeholder.markdown(full_res + "▌")
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun() # Refresh to apply custom CSS to new message
        except Exception as e:
            st.error(f"Operational Error: {e}")
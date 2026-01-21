import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="NEURAL ELITE | Vision Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ELITE STYLING (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Space+Grotesk:wght@300;500;700&display=swap');
    
    :root {
        --primary-gold: #D4AF37;
        --accent-blue: #007AFF;
        --bg-dark: #0A0B10;
        --glass-bg: rgba(255, 255, 255, 0.03);
    }

    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(circle at 2% 10%, rgba(212, 175, 55, 0.05) 0%, transparent 20%),
            radial-gradient(circle at 98% 80%, rgba(0, 122, 255, 0.08) 0%, transparent 30%);
        color: #F8F9FA;
        font-family: 'Inter', sans-serif;
    }

    /* Professional Typography */
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; font-weight: 700 !important; }

    /* Custom Header */
    .main-header {
        text-align: left;
        padding: 2rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 2rem;
    }

    .badge {
        background: linear-gradient(90deg, #D4AF37, #F9E2AF);
        color: black;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
        display: inline-block;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(13, 14, 18, 0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Minimalist Chat */
    .stChatMessage {
        background: var(--glass-bg) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    /* Premium Input */
    .stChatInputContainer {
        border-top: 1px solid rgba(255,255,255,0.05) !important;
        background: #0A0B10 !important;
        padding: 20px 0 !important;
    }

    div[data-testid="stChatInput"] {
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stChatInput"]:focus-within {
        border-color: var(--primary-gold) !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.1);
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: transparent;
        border: 1px solid rgba(255,255,255,0.1);
        color: #F8F9FA;
        border-radius: 4px;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 1px;
        transition: 0.3s;
    }

    .stButton>button:hover {
        border-color: var(--primary-gold);
        color: var(--primary-gold);
        background: rgba(212, 175, 55, 0.05);
    }

    /* Hide redundant UI */
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BACKEND INITIALIZATION ---
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_img(file):
    return base64.b64encode(file.getvalue()).decode('utf-8')

# --- 4. SIDEBAR (CONTROL PANEL) ---
with st.sidebar:
    st.markdown("<h2 style='letter-spacing:-1px;'>NEURAL<span style='color:#D4AF37;'>ELITE</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; color:#666;'>OPERATING SYSTEM V2.4</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    st.caption("INTELLIGENCE CORE")
    model_choice = st.selectbox(
        "Select Model",
        ["llama-3.3-70b-versatile", "llama-3.2-11b-vision-preview"],
        label_visibility="collapsed"
    )
    
    st.write("###")
    st.caption("MEDIA ANALYSIS")
    uploaded_image = st.file_uploader("Drop luxury assets here", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        st.image(uploaded_image, use_container_width=True)
    
    st.write("---")
    if st.button("RESET SESSION"):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.markdown("""
    <div class='main-header'>
        <span class='badge'>System Active</span>
        <h1 style='font-size: 42px; margin:0;'>Intelligence <span style='font-weight:300; color:#D4AF37;'>Interface</span></h1>
        <p style='color: #666; font-size: 14px;'>Advanced Multi-Modal Processing Unit</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN INTERFACE (CHAT DISPLAY) ---
st.markdown("""
    <div class='main-header'>
        <span class='badge'>System Active</span>
        <h1 style='font-size: 42px; margin:0; font-family: "Space Grotesk";'>Intelligence <span style='font-weight:300; color:#D4AF37;'>Interface</span></h1>
        <p style='color: #666; font-size: 14px;'>Professional Multi-Modal Processing Unit</p>
    </div>
    """, unsafe_allow_html=True)

# Container khusus untuk chat agar lebih rapi
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        role_class = "user-style" if message["role"] == "user" else "assistant-style"
        avatar = "👤" if message["role"] == "user" else "🤖"
        bg_color = "rgba(255, 255, 255, 0.05)" if message["role"] == "user" else "rgba(212, 175, 55, 0.03)"
        border_color = "rgba(255, 255, 255, 0.1)" if message["role"] == "user" else "rgba(212, 175, 55, 0.2)"
        
        st.markdown(f"""
            <div style="
                background: {bg_color};
                border: 1px solid {border_color};
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 15px;
                display: flex;
                align-items: flex-start;
                gap: 15px;
                backdrop-filter: blur(10px);
            ">
                <div style="font-size: 24px;">{avatar}</div>
                <div style="flex: 1;">
                    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #666; margin-bottom: 5px;">
                        {message["role"]}
                    </div>
                    <div style="color: #F8F9FA; line-height: 1.6; font-weight: 300;">
                        {message["content"]}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 6. AI LOGIC ---
if prompt := st.chat_input("Enter command or inquiry..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        # Smart Model Selection & Context
        if uploaded_image:
            b64_img = encode_img(uploaded_image)
            api_msgs = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]
            }]
            current_model = "llama-3.2-11b-vision-preview"
        else:
            api_msgs = [
                {"role": "system", "content": "You are Neural Elite, a highly sophisticated, concise, and professional AI. Your tone is executive, helpful, and direct."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ]
            current_model = model_choice

        try:
            completion = client.chat.completions.create(
                model=current_model,
                messages=api_msgs,
                temperature=0.4, # Lower temp for more professional responses
                stream=True
            )
            
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_res += content
                placeholder.markdown(full_res + " ")
            
            placeholder.markdown(full_res)
        except Exception as e:
            st.error(f"Execution Error: {e}")
    
    st.session_state.messages.append({"role": "assistant", "content": full_res})
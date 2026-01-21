import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. SETTING PAGE ULTRA PREMIUM ---
st.set_page_config(
    page_title="Elite AI Vision Pro",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS CUSTOM: FUTURISTIC COMMAND CENTER ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #050507 100%);
        color: #e0e0e0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Header & Aura Glow */
    .hero-container {
        text-align: center;
        padding: 60px 0 20px 0;
        background: radial-gradient(circle at center, rgba(123, 31, 162, 0.15) 0%, transparent 70%);
    }

    .elite-title {
        font-size: 72px;
        font-weight: 800;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 15px rgba(79, 172, 254, 0.4));
    }

    .sub-title {
        font-size: 20px;
        color: #888fb1;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 400;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 15, 0.9) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Chat Interface */
    .stChatMessage {
        border-radius: 20px;
        margin-bottom: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }

    [data-testid="stChatMessageAssistant"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px);
    }

    /* Floating Input Center */
    .stChatInputContainer {
        border-radius: 50px !important;
        background: rgba(30, 30, 45, 0.8) !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        padding: 10px 20px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }

    /* Buttons & Interactions */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(118, 75, 162, 0.4);
    }

    /* Hide Elements */
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC & AI ENGINE ---
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_img(file):
    return base64.b64encode(file.getvalue()).decode('utf-8')

# --- 4. SIDEBAR DASHBOARD ---
with st.sidebar:
    st.markdown("<div style='text-align:center;'><h1 style='color:#00f2fe;font-size:30px;'>ELITE PRO</h1></div>", unsafe_allow_html=True)
    st.write("---")
    
    st.subheader("⚙️ Model Engine")
    model_choice = st.selectbox(
        "Intelligence Mode",
        ["llama-3.3-70b-versatile", "llama-3.2-11b-vision-preview"],
        index=0
    )
    
    st.write("###")
    st.subheader("📸 Vision & Media")
    uploaded_image = st.file_uploader("Upload Image for Analysis", type=["jpg", "jpeg", "png"])
    
    st.write("###")
    if st.button("🗑️ Clear All Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN DISPLAY ---
st.markdown("""
    <div class='hero-container'>
        <div class='elite-title'>VISION PRO</div>
        <div class='sub-title'>Futuristic Multi-Modal Assistant</div>
    </div>
    """, unsafe_allow_html=True)

# Container Chat
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 6. AI INTERACTION ---
if prompt := st.chat_input("Perintahkan AI Vision Pro..."):
    
    # Simpan Chat User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        # Logika Smart Vision
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
                {"role": "system", "content": "You are Elite AI Vision Pro, a high-end, professional, and futuristic AI assistant."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ]
            current_model = "llama-3.3-70b-versatile"

        # Streaming Effect
        try:
            completion = client.chat.completions.create(
                model=current_model,
                messages=api_msgs,
                temperature=0.7,
                stream=True
            )
            
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_res += content
                placeholder.markdown(full_res + "▌")
            
            placeholder.markdown(full_res)
        except Exception as e:
            st.error(f"System Error: {e}")
    
    st.session_state.messages.append({"role": "assistant", "content": full_res})
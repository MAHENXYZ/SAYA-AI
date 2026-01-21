import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# ==========================================
# 1. CORE SYSTEM ARCHITECTURE (LOGGING)
# ==========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================
# 2. ADVANCED CONFIGURATION & PRESETS
# ==========================================
class EliteConfig:
    PAGE_TITLE = "NEURAL ELITE v3.0 | Executive Intelligence"
    PAGE_ICON = "💎"
    THEME_COLOR = "#C5A059"
    DEEP_BG = "#08090B"
    MODELS = {
        "Strategic": "llama-3.3-70b-versatile",
        "Visual": "llama-3.2-11b-vision-preview"
    }
    SYSTEM_PROMPT = """
    You are Neural Elite v3.0, an ultra-premium AI consultant. 
    Your communication style is executive, precise, and highly analytical. 
    Avoid filler words. Provide maximum value with minimalist elegance.
    """

# ==========================================
# 3. GLOBAL UI INJECTION (CUSTOM CSS)
# ==========================================
def inject_ultra_luxury_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@200;300;400;500;600&display=swap');
    
    :root {{
        --gold: {EliteConfig.THEME_COLOR};
        --bg: {EliteConfig.DEEP_BG};
    }}

    /* Global Foundation */
    .stApp {{
        background: var(--bg);
        background-image: 
            radial-gradient(circle at 0% 0%, rgba(197, 160, 89, 0.08) 0%, transparent 35%),
            radial-gradient(circle at 100% 100%, rgba(255, 255, 255, 0.02) 0%, transparent 35%);
        color: #F8F9FA;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* Sidebar Glass-Refraction */
    [data-testid="stSidebar"] {{
        background: rgba(5, 5, 5, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
    }}

    /* Header Professionalism */
    .elite-nav {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 2rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 3rem;
    }}

    .logo-text {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 5px;
        background: linear-gradient(90deg, #FFF, var(--gold));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* Message Architecture */
    .msg-container {{
        max-width: 850px;
        margin: 0 auto 2rem auto;
        animation: fadeIn 0.8s ease-out;
    }}

    .msg-card {{
        padding: 2.5rem;
        border-radius: 2px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
    }}

    .ai-card {{
        background: linear-gradient(135deg, rgba(197, 160, 89, 0.04) 0%, transparent 100%);
        border-left: 2px solid var(--gold);
    }}

    .user-card {{
        background: rgba(255, 255, 255, 0.01);
    }}

    .meta-label {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 9px;
        letter-spacing: 3px;
        color: var(--gold);
        text-transform: uppercase;
        margin-bottom: 1rem;
    }}

    /* Input Optimization */
    .stChatInputContainer {{
        padding: 2rem 10% !important;
        background: var(--bg) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
    }}

    div[data-testid="stChatInput"] {{
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    div[data-testid="stChatInput"]:focus-within {{
        border-color: var(--gold) !important;
        box-shadow: 0 0 30px rgba(197, 160, 89, 0.1);
    }}

    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. BACKEND LOGIC & UTILITIES
# ==========================================
class NeuralCore:
    def __init__(self):
        self.api_key = st.secrets.get("GROQ_API_KEY", "")
        if not self.api_key:
            st.error("SYSTEM ERROR: API_KEY_MISSING")
            st.stop()
        self.client = Groq(api_key=self.api_key)

    @staticmethod
    def encode_image(file):
        return base64.b64encode(file.getvalue()).decode('utf-8')

    def generate_response(self, model: str, messages: List[Dict], is_vision: bool = False):
        try:
            return self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.4,
                max_tokens=4096,
                top_p=1,
                stream=True
            )
        except Exception as e:
            logger.error(f"Generation Error: {e}")
            return None

# ==========================================
# 5. STATE MANAGEMENT
# ==========================================
def initialize_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "core" not in st.session_state:
        st.session_state.core = NeuralCore()

# ==========================================
# 6. APPLICATION VIEW
# ==========================================
def main():
    st.set_page_config(
        page_title=EliteConfig.PAGE_TITLE,
        page_icon=EliteConfig.PAGE_ICON,
        layout="wide"
    )
    initialize_session()
    inject_ultra_luxury_css()

    # --- SIDEBAR (DASHBOARD) ---
    with st.sidebar:
        st.markdown(f"<div style='margin: 2rem 0;'><span style='color:white; font-size:12px; letter-spacing:5px;'>CONTROL UNIT</span></div>", unsafe_allow_html=True)
        
        # Engine Control
        st.write("###")
        st.caption("CORE SELECTION")
        selected_model_key = st.selectbox("Engine", list(EliteConfig.MODELS.keys()), label_visibility="collapsed")
        engine = EliteConfig.MODELS[selected_model_key]

        # Asset Control
        st.write("###")
        st.caption("VISUAL ASSETS")
        asset = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
        if asset:
            st.image(asset, use_container_width=True)
            st.info("Visual data integrated.")

        # System Control
        st.write("###")
        st.write("---")
        if st.button("TERMINATE SESSION"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown(f"<div style='position: fixed; bottom: 20px; font-size: 8px; color: #444;'>ID: {st.session_state.session_id}</div>", unsafe_allow_html=True)

    # --- MAIN VIEW ---
    st.markdown(f"""
        <div class="elite-nav">
            <div class="logo-text">NEURAL ELITE</div>
            <div style="font-size: 10px; letter-spacing: 2px; color: {EliteConfig.THEME_COLOR}; font-weight: 600;">
                ACTIVE SYSTEM // ENCRYPTED
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Render History with Premium Styling
    for msg in st.session_state.messages:
        is_ai = msg["role"] == "assistant"
        card_class = "ai-card" if is_ai else "user-card"
        label = "Neural Response" if is_ai else "Strategic Inquiry"
        
        st.markdown(f"""
            <div class="msg-container">
                <div class="msg-card {card_class}">
                    <div class="meta-label">{label}</div>
                    <div style="font-weight: 300; line-height: 1.8; color: #D1D1D1;">
                        {msg["content"]}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- AI INTERACTION ---
    if prompt := st.chat_input("Enter command..."):
        # Log User Inquiry
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # Processing Response
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        current_inquiry = st.session_state.messages[-1]["content"]
        
        with st.chat_message("assistant", avatar=None):
            placeholder = st.empty()
            full_response = ""
            
            # Context Logic
            if asset:
                active_model = EliteConfig.MODELS["Visual"]
                payload = [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": current_inquiry},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{NeuralCore.encode_image(asset)}"}}
                    ]
                }]
            else:
                active_model = engine
                payload = [
                    {"role": "system", "content": EliteConfig.SYSTEM_PROMPT},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]

            # Streaming Generation
            stream = st.session_state.core.generate_response(active_model, payload)
            
            if stream:
                for chunk in stream:
                    content = chunk.choices[0].delta.content or ""
                    full_response += content
                    placeholder.markdown(f"""
                        <div class="msg-card ai-card" style="margin-top:0;">
                            <div class="meta-label">Processing Intelligence...</div>
                            <div style="font-weight: 300; line-height: 1.8; color: #D1D1D1;">
                                {full_response}▌
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                placeholder.empty() # Clean up before permanent append
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                st.rerun()

if __name__ == "__main__":
    main()
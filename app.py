import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
import time
from datetime import datetime

# =============================================================================
# 1. CORE SYSTEM CONFIGURATION (PREMIUM SETTINGS)
# =============================================================================
class NeuralEliteSystem:
    TITLE = "NEURAL ELITE v4.0 | Advanced Intelligence"
    ICON = "💎"
    THEME_PRIMARY = "#C5A059"  # Champagne Gold
    THEME_DARK = "#050505"     # Pure Obsidian
    SYSTEM_PROMPT = """
    You are Neural Elite v4.0, a highly sophisticated AI operating system. 
    Your communication is executive, concise, and professional. 
    You provide expert-level analysis and creative solutions.
    """

# =============================================================================
# 2. ULTRA-PREMIUM UI INJECTION (ADVANCED CSS)
# =============================================================================
def inject_premium_ui():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@200;300;400;500;600&display=swap');
    
    /* Global Reset & Background */
    .stApp {{
        background: {NeuralEliteSystem.THEME_DARK};
        background-image: 
            radial-gradient(circle at 0% 0%, rgba(197, 160, 89, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 100% 100%, rgba(255, 255, 255, 0.02) 0%, transparent 40%);
        color: #F8F9FA;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* Custom Header Navigation */
    .premium-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 3rem;
    }}

    .logo-container {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 5px;
        background: linear-gradient(90deg, #FFFFFF, {NeuralEliteSystem.THEME_PRIMARY});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* Sidebar Glass-Aesthetic */
    [data-testid="stSidebar"] {{
        background: rgba(10, 10, 10, 0.98) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
    }}

    /* Chat Architecture: The Professional Look */
    .message-row {{
        max-width: 900px;
        margin: 0 auto 2rem auto;
        animation: slideUp 0.6s ease-out;
    }}

    .message-card {{
        padding: 2rem;
        border-radius: 4px; /* Sharp professional edges */
        border: 1px solid rgba(255, 255, 255, 0.04);
        position: relative;
    }}

    .ai-response {{
        background: linear-gradient(135deg, rgba(197, 160, 89, 0.03) 0%, transparent 100%);
        border-left: 2px solid {NeuralEliteSystem.THEME_PRIMARY};
    }}

    .user-inquiry {{
        background: rgba(255, 255, 255, 0.01);
        border-left: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .role-tag {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 9px;
        letter-spacing: 2px;
        color: {NeuralEliteSystem.THEME_PRIMARY};
        text-transform: uppercase;
        margin-bottom: 1rem;
        font-weight: 600;
    }}

    /* Premium Input Field */
    .stChatInputContainer {{
        padding: 2rem 12% !important;
        background: {NeuralEliteSystem.THEME_DARK} !important;
        border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
    }}

    div[data-testid="stChatInput"] {{
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.01) !important;
        border-radius: 4px !important;
    }}

    /* Animation Keyframes */
    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 3. BACKEND & STATE MANAGEMENT
# =============================================================================
def initialize_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = st.secrets.get("GROQ_API_KEY", "")

def get_image_base64(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode()

# =============================================================================
# 4. MAIN APPLICATION ARCHITECTURE
# =============================================================================
def main():
    st.set_page_config(
        page_title=NeuralEliteSystem.TITLE,
        page_icon=NeuralEliteSystem.ICON,
        layout="wide"
    )
    initialize_state()
    inject_premium_ui()

    # --- Sidebar: Operational Control ---
    with st.sidebar:
        st.markdown("<div style='padding: 20px 0;'><span style='letter-spacing:3px; font-size:12px; color:#555;'>SYSTEM CONSOLE</span></div>", unsafe_allow_html=True)
        
        st.write("###")
        st.caption("INTELLIGENCE ENGINE")
        model_choice = st.selectbox(
            "Engine",
            ["llama-3.3-70b-versatile", "llama-3.2-11b-vision-preview"],
            label_visibility="collapsed"
        )

        st.write("###")
        st.caption("VISUAL DATA BUFFER")
        img_file = st.file_uploader("Upload Assets", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
        if img_file:
            st.image(img_file, use_container_width=True)
            st.success("Visual Data Locked.")

        st.write("---")
        if st.button("TERMINATE SESSION"):
            st.session_state.messages = []
            st.rerun()

    # --- Main Screen: Neural Dashboard ---
    st.markdown(f"""
        <div class="premium-header">
            <div class="logo-container">NEURAL ELITE</div>
            <div style="font-size: 10px; color: #444; letter-spacing: 1px;">CHANNEL ID: 0xFF-ALPHAV4</div>
        </div>
    """, unsafe_allow_html=True)

    # Render Chat History
    for m in st.session_state.messages:
        is_ai = m["role"] == "assistant"
        style_class = "ai-response" if is_ai else "user-inquiry"
        label = "Neural Response" if is_ai else "Strategic Inquiry"
        
        st.markdown(f"""
            <div class="message-row">
                <div class="message-card {style_class}">
                    <div class="role-tag">{label}</div>
                    <div style="font-weight: 300; line-height: 1.8; color: #D1D1D1;">
                        {m["content"]}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- AI Logic & Execution ---
    if prompt := st.chat_input("Enter command to Neural Elite..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant", avatar=None):
            placeholder = st.empty()
            full_content = ""
            
            client = Groq(api_key=st.session_state.api_key)
            
            # Logic: Automatic Switch for Vision
            if img_file:
                selected_model = "llama-3.2-11b-vision-preview"
                messages = [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{get_image_base64(img_file)}"}}
                    ]
                }]
            else:
                selected_model = model_choice
                messages = [
                    {"role": "system", "content": NeuralEliteSystem.SYSTEM_PROMPT},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]

            try:
                # Streaming Response
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=messages,
                    stream=True
                )
                
                for chunk in response:
                    content = chunk.choices[0].delta.content or ""
                    full_content += content
                    placeholder.markdown(f"""
                        <div class="message-card ai-response" style="margin-top:0;">
                            <div class="role-tag">Processing Data...</div>
                            <div style="font-weight: 300; line-height: 1.8; color: #D1D1D1;">
                                {full_content}▌
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.session_state.messages.append({"role": "assistant", "content": full_content})
                st.rerun()
            except Exception as e:
                st.error(f"System Operational Error: {e}")

if __name__ == "__main__":
    main()
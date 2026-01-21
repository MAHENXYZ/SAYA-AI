import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
import time
from datetime import datetime

# =============================================================================
# 1. ELITE SYSTEM ARCHITECTURE & ENGINE CONFIGURATION
# =============================================================================
class WisprFlowEngine:
    """Sistem manajemen state dan logika backend tingkat tinggi."""
    
    def __init__(self):
        self.api_key = st.secrets.get("GROQ_API_KEY", "")
        if not self.api_key:
            st.error("CRITICAL ERROR: API KEY NOT DETECTED IN SECRETS.")
            st.stop()
        self.client = Groq(api_key=self.api_key)

    @staticmethod
    def get_image_payload(uploaded_file):
        """Memproses data visual ke dalam format base64 dengan optimasi buffer."""
        if uploaded_file is not None:
            return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
        return None

    def execute_stream(self, model, messages):
        """Menjalankan stream completion dengan penanganan error enterprise."""
        try:
            return self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.4,
                max_tokens=4096,
                stream=True
            )
        except Exception as e:
            st.error(f"ENGINE FAILURE: {str(e)}")
            return None

# =============================================================================
# 2. DESIGN SYSTEM INJECTION (WISPR FLOW REPLICA)
# =============================================================================
def apply_wispr_design_system():
    """Injeksi CSS tingkat lanjut untuk estetika Apple-style Minimalism."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@100;200;300;400;500&display=swap');
    
    /* Root Variables & Base */
    :root {
        --wispr-bg: #000000;
        --wispr-text: #FFFFFF;
        --wispr-muted: rgba(255, 255, 255, 0.4);
        --wispr-border: rgba(255, 255, 255, 0.08);
    }

    .stApp {
        background-color: var(--wispr-bg);
        color: var(--wispr-text);
        font-family: 'Inter', sans-serif;
    }

    /* Top Navigation (Fixed & Minimalist) */
    .wispr-nav {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        padding: 40px 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 999;
        background: linear-gradient(to bottom, black 20%, transparent);
    }

    .nav-brand {
        letter-spacing: 10px;
        font-size: 11px;
        font-weight: 200;
        opacity: 0.5;
        text-transform: uppercase;
    }

    /* The Hero Section (Typography Masterpiece) */
    .wispr-hero {
        margin-top: 25vh;
        margin-bottom: 10vh;
        text-align: center;
        animation: fadeIn 2s ease-in-out;
    }

    .wispr-title {
        font-family: 'Instrument Serif', serif;
        font-size: clamp(50px, 10vw, 110px);
        font-style: italic;
        line-height: 0.95;
        font-weight: 400;
        background: linear-gradient(180deg, #FFFFFF 30%, rgba(255,255,255,0.2) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
    }

    /* Chat Layout & Bubbles */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 2rem 22% !important;
    }

    .stChatMessage [data-testid="stMarkdownContainer"] p {
        font-size: 20px !important;
        font-weight: 200 !important;
        line-height: 1.7 !important;
        color: #EAEAEA;
    }

    /* Sophisticated Input Bar (Wispr Signature) */
    .stChatInputContainer {
        padding: 60px 20% !important;
        background: linear-gradient(to top, black 50%, transparent) !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] {
        border: 1px solid var(--wispr-border) !important;
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 100px !important;
        padding: 15px 30px !important;
        transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: rgba(255, 255, 255, 0.3) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        transform: scale(1.01);
    }

    /* Utility Elements */
    header, footer, [data-testid="stSidebar"] { display: none; }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Custom Reset Button Style */
    .reset-trigger {
        position: fixed;
        bottom: 30px;
        right: 30px;
        font-size: 10px;
        letter-spacing: 2px;
        opacity: 0.3;
        cursor: pointer;
        transition: 0.3s;
    }
    .reset-trigger:hover { opacity: 1; color: #C5A059; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 3. APPLICATION BOOTSTRAPPER
# =============================================================================
def main():
    # Initialize Engine
    engine = WisprFlowEngine()
    apply_wispr_design_system()

    # Session State Persistence
    if "flow_memory" not in st.session_state:
        st.session_state.flow_memory = []
    
    # Navigation Layer
    st.markdown("""
        <div class="wispr-nav">
            <div class="nav-brand">Flow v4.0</div>
            <div style="font-size: 10px; opacity: 0.4;">STRATEGIC NODE: ALPHA-1</div>
        </div>
    """, unsafe_allow_html=True)

    # UI Logic: Hero or Chat History
    if not st.session_state.flow_memory:
        st.markdown("""
            <div class="wispr-hero">
                <h1 class="wispr-title">The silence<br>of intelligence.</h1>
                <p style="margin-top:30px; font-weight:200; opacity:0.3; letter-spacing:4px; font-size:12px;">
                    CONVERSE WITH THE FLOW
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Menampilkan riwayat chat dengan spasi yang sangat lapang
        for msg in st.session_state.flow_memory:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # --- INPUT LAYER ---
    if prompt := st.chat_input("Enter your flow..."):
        # Tambahkan ke memori dan refresh
        st.session_state.flow_memory.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate Response
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            # Persiapkan pesan (Contextual Awareness)
            api_messages = [
                {"role": "system", "content": "You are Flow. You respond with extreme clarity, professional depth, and a calm, sophisticated tone. No emojis. Just wisdom."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.flow_memory]
            ]

            stream = engine.execute_stream("llama-3.3-70b-versatile", api_messages)
            
            if stream:
                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    full_response += delta
                    # Efek kursor Wispr (◦)
                    placeholder.markdown(full_response + "◦")
                
                placeholder.markdown(full_response)
                st.session_state.flow_memory.append({"role": "assistant", "content": full_response})
                st.rerun()

    # Hidden Functional Footer
    st.markdown('<div class="reset-trigger">0x00: REBOOT SYSTEM</div>', unsafe_allow_html=True)
    if st.button("TERMINATE", help="Wipe all data", use_container_width=False):
        st.session_state.flow_memory = []
        st.rerun()

if __name__ == "__main__":
    main()
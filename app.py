import streamlit as st
from groq import Groq
import base64

# --- 1. SETTING PAGE: WISPR STYLE ---
st.set_page_config(
    page_title="Flow",
    page_icon="◦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THE WISPR FLOW "VIBE" CSS ---
st.markdown("""
    <style>
    /* Menggunakan font premium: Playfair Display untuk Serif, Inter untuk Sans */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400&family=Playfair+Display:ital,wght@0,400;1,400&display=swap');
    
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Logo & Nav di tengah seperti Wispr */
    .nav-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        padding: 30px;
        text-align: center;
        z-index: 1000;
        background: rgba(0,0,0,0.8);
        backdrop-filter: blur(10px);
    }

    .nav-logo {
        letter-spacing: 0.5em;
        font-size: 12px;
        font-weight: 300;
        color: rgba(255,255,255,0.5);
        text-transform: uppercase;
    }

    /* Hero Text: Kunci Mewah WisprFlow */
    .hero-section {
        margin-top: 15vh;
        margin-bottom: 5vh;
        text-align: center;
    }

    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(40px, 8vw, 80px);
        font-style: italic;
        font-weight: 400;
        line-height: 1.1;
        background: linear-gradient(180deg, #FFFFFF 0%, rgba(255,255,255,0.4) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Chat Area: Sangat Lapang */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 150px;
    }

    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        margin-bottom: 2rem !important;
    }

    /* Teks AI & User */
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem !important;
        font-weight: 300 !important;
        line-height: 1.7 !important;
        color: rgba(255,255,255,0.9);
    }

    /* Input Bar yang 'Melayang' dan Bersih */
    .stChatInputContainer {
        padding: 40px 10% !important;
        background: linear-gradient(to top, #000 60%, transparent) !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] {
        border: 1px solid rgba(255,255,255,0.1) !important;
        background: rgba(255,255,255,0.05) !important;
        border-radius: 100px !important; /* Pill style */
        padding: 10px 25px !important;
    }

    /* Sembunyikan Elemen Streamlit yang merusak estetika */
    [data-testid="stSidebar"], header, footer { display: none; }
    
    /* Tombol */
    button {
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "ISI_API_KEY_DISINI"))

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. VIEW ---
st.markdown('<div class="nav-header"><div class="nav-logo">Flow Intelligence</div></div>', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">Experience the<br>poetry of thought.</h1>
            <p style="color:rgba(255,255,255,0.4); letter-spacing:2px; font-size:12px; margin-top:20px;">AI FOR THE STRATEGIC MIND</p>
        </div>
    """, unsafe_allow_html=True)

# Container Chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. INTERACTION ---
if prompt := st.chat_input("Write your flow..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Menggunakan Model Terkuat (Llama 3.3 70B)
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Flow. Your response is direct, elegant, and highly professional. Use sophisticated vocabulary but keep it concise."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                placeholder.markdown(full_response + "◦")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Operational Error: {e}")

# Tombol Reset Mewah di pojok bawah
if st.session_state.messages:
    if st.button("CLEAR FLOW"):
        st.session_state.messages = []
        st.rerun()
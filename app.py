import streamlit as st
from groq import Groq
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Gemini Ultra",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LUXURY GEMINI CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');

    /* Background Utama */
    .stApp {
        background-color: #0e0e10;
        color: #e3e3e3;
        font-family: 'Google Sans', sans-serif;
    }

    /* Header Animasi */
    .gemini-gradient {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570, #4285f4);
        background-size: 300% 300%;
        animation: gradient-move 8s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 56px;
        font-weight: 500;
        letter-spacing: -1px;
    }

    @keyframes gradient-move {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sidebar Ultra Modern */
    [data-testid="stSidebar"] {
        background-color: #171719 !important;
        border-right: 1px solid #2d2d2f;
    }

    /* Input Chat ala Google */
    .stChatInputContainer {
        border-radius: 32px !important;
        background: #1e1f20 !important;
        border: 1px solid #3c4043 !important;
        padding: 8px 16px !important;
        margin-bottom: 20px;
    }

    /* Tombol Sidebar */
    .stButton>button {
        border-radius: 12px;
        background-color: #2d2d2f;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #3c4043;
        border: 1px solid #4285f4;
    }

    /* Pesan Chat */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding-top: 2rem !important;
    }

    /* Menghilangkan elemen default Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC & API ---
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: white; margin-bottom: 20px;'>Gemini</h2>", unsafe_allow_html=True)
    
    model_choice = st.selectbox(
        "Intelligence Mode",
        ["llama-3.2-11b-vision-preview", "llama-3.3-70b-versatile"],
        index=1
    )
    
    st.divider()
    st.markdown("### 📷 Vision & Docs")
    uploaded_file = st.file_uploader("Tambahkan gambar atau teks", type=["jpg", "png", "txt"])
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN INTERFACE ---
# Spacer atas
st.write("##")
st.markdown("<h1 class='gemini-gradient'>Halo, Mahendra</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 24px; color: #8e918f;'>Ada yang bisa saya bantu hari ini?</p>", unsafe_allow_html=True)

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. CHAT INPUT & RESPONSE ---
if prompt := st.chat_input("Tulis pertanyaan Anda di sini..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Logika Vision jika ada gambar
        if uploaded_file and "vision" in model_choice and uploaded_file.type in ["image/jpeg", "image/png"]:
            # (Fitur Vision diaktifkan di sini)
            content_list = [{"type": "text", "text": prompt}]
            # Tambahkan proses image encoding jika diperlukan
            
            completion = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
        else:
            # Teks normal
            completion = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True
            )

        for chunk in completion:
            full_response += (chunk.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
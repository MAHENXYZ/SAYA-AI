import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. KONFIGURASI HALAMAN ULTRA PREMIUM ---
st.set_page_config(
    page_title="Gemini Ultra Max",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS MEWAH & ANIMASI (LEVEL PROFESIONAL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');

    /* Background Utama */
    .stApp {
        background: radial-gradient(circle at center, #1a1a2e 0%, #0a0a0c 100%);
        color: #e3e3e3;
        font-family: 'Google Sans', sans-serif;
    }

    /* Judul Animasi Gradasi */
    .gemini-title {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570, #4285f4);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 64px;
        font-weight: 700;
        letter-spacing: -2px;
        animation: shine 5s linear infinite;
        margin-bottom: 0px;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 25, 0.7) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Input Chat Melayang */
    .stChatInputContainer {
        border-radius: 35px !important;
        background: rgba(40, 40, 45, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        padding: 10px 20px !important;
    }

    /* Pesan Chat yang Bersih */
    .stChatMessage {
        border-radius: 20px;
        margin-bottom: 10px;
        border: none !important;
        background: transparent !important;
    }

    /* Sembunyikan Header Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Styling Button */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        background: linear-gradient(45deg, #4285f4, #9b72cb);
        color: white;
        border: none;
        font-weight: 500;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(66, 133, 244, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNGSI TEKNIS ---
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# Konek ke Groq
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SIDEBAR CANGGIH ---
with st.sidebar:
    st.markdown("<h1 style='color: white; font-size: 28px;'>Gemini Ultra</h1>", unsafe_allow_html=True)
    st.write("###")
    
    # Pilih Model Profesional
    model_choice = st.selectbox(
        "Intelligence Engine",
        ["llama-3.2-11b-vision-preview", "llama-3.3-70b-versatile"],
        index=0,
        help="Pilih Vision untuk analisis gambar!"
    )
    
    st.divider()
    
    # Upload Center
    st.markdown("### 📤 Resource Upload")
    up_img = st.file_uploader("Upload Image (Vision)", type=["jpg", "jpeg", "png"])
    up_txt = st.file_uploader("Upload Document (Analysis)", type=["txt"])
    
    st.write("###")
    if st.button("🗑️ Reset Intelligence Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 5. INTERFACE UTAMA ---
st.markdown("<h1 class='gemini-title'>Halo, Mahendra</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 24px; color: #aaa; margin-top: -10px;'>Mau eksplorasi apa hari ini?</p>", unsafe_allow_html=True)
st.write("---")

# Render Riwayat Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. LOGIKA CHAT & VISION ---
if prompt := st.chat_input("Tanyakan sesuatu pada Gemini Ultra..."):
    
    # Simpan Chat User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        # Susun Pesan API
        api_messages = []
        
        # Fitur VISION (Jika ada gambar)
        if up_img and "vision" in model_choice:
            img_b64 = encode_image(up_img)
            api_messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }]
        else:
            # Fitur DOKUMEN & TEKS
            context = ""
            if up_txt:
                context = f"[KONTEKS DOKUMEN]: {up_txt.read().decode('utf-8')}\n\n"
            
            api_messages = [
                {"role": "system", "content": "You are Gemini Ultra, a professional AI by Google. Be smart and helpful."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                {"role": "user", "content": context + prompt}
            ]

        # PROSES STREAMING (CANGGIH)
        completion = client.chat.completions.create(
            model=model_choice,
            messages=api_messages,
            temperature=0.7,
            stream=True
        )
        
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            full_res += content
            placeholder.markdown(full_res + "▌")
        
        placeholder.markdown(full_res)
    
    st.session_state.messages.append({"role": "assistant", "content": full_res})
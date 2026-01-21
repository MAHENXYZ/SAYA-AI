import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. CONFIGURATION HALAMAN MASTERPIECE ---
st.set_page_config(
    page_title="Gemini Ultra Professional",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS MEWAH: THE REAL GEMINI EXPERIENCE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');

    /* Tema Gelap Cinematic */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e1e3f 0%, #050505 100%);
        color: #e3e3e3;
        font-family: 'Google Sans', sans-serif;
    }

    /* Judul Animasi Berkilau (Gemini Style) */
    .premium-title {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570, #4285f4);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 60px;
        font-weight: 700;
        letter-spacing: -1.5px;
        animation: shine 4s linear infinite;
        margin-bottom: 0px;
    }

    @keyframes shine { to { background-position: 200% center; } }

    /* Input Chat Melayang & Modern */
    .stChatInputContainer {
        border-radius: 35px !important;
        background: rgba(30, 31, 32, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6) !important;
        padding: 10px 20px !important;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 18, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Chat Bubbles Clean */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        margin-bottom: 15px;
    }

    /* Sembunyikan Header & Footer Bawaan */
    header, footer { visibility: hidden; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SISTEM TEKNIS ---
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# Hubungkan ke Groq Cloud
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SIDEBAR PREMIUM ---
with st.sidebar:
    st.markdown("<h2 style='color: white; font-weight: 700;'>Gemini Ultra</h2>", unsafe_allow_html=True)
    st.write("###")
    
    # Engine Selector
    model_choice = st.selectbox(
        "Sistem Kecerdasan:",
        ["llama-3.3-70b-versatile", "llama-3.2-11b-vision-preview"],
        help="Gunakan 70b untuk teks cerdas, 11b jika ingin kirim gambar."
    )
    
    st.divider()
    st.markdown("### 🖼️ Unggah Media")
    uploaded_image = st.file_uploader("Analisis Gambar (Vision)", type=["jpg", "jpeg", "png"])
    uploaded_text = st.file_uploader("Analisis Dokumen (TXT)", type=["txt"])
    
    st.write("###")
    if st.button("🗑️ Hapus Memori Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. TAMPILAN UTAMA ---
st.markdown("<h1 class='premium-title'>Halo, Mahendra</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 22px; color: #9aa0a6; margin-top: -15px;'>Ada yang bisa saya bantu buatkan hari ini?</p>", unsafe_allow_html=True)
st.write("---")

# Tampilkan Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. LOGIKA CHAT & VISION CANGGIH ---
if prompt := st.chat_input("Tanyakan sesuatu pada Gemini Ultra..."):
    
    # 1. Simpan input user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Respon AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # --- LOGIKA ANTI-ERROR (Sangat Penting!) ---
        # Jika user upload gambar, otomatis paksa pakai model Vision
        if uploaded_image:
            img_b64 = encode_image(uploaded_image)
            api_messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }]
            active_model = "llama-3.2-11b-vision-preview"
        else:
            # Jika hanya teks, gunakan model teks cerdas (70b)
            doc_context = ""
            if uploaded_text:
                doc_context = f"[KONTEKS DOKUMEN]: {uploaded_text.read().decode('utf-8')}\n\n"
            
            api_messages = [
                {"role": "system", "content": "Anda adalah Gemini Ultra Professional, AI tercanggih dengan gaya bahasa yang elegan, sopan, dan sangat cerdas."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                {"role": "user", "content": doc_context + prompt}
            ]
            active_model = "llama-3.3-70b-versatile"

        # 3. Proses Streaming (Efek Mengetik)
        try:
            completion = client.chat.completions.create(
                model=active_model,
                messages=api_messages,
                temperature=0.6,
                stream=True
            )
            
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Terjadi kesalahan teknis: {e}")
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
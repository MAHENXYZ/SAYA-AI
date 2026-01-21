import streamlit as st
from groq import Groq
import base64

# --- CONFIG HALAMAN PREMIUM ---
st.set_page_config(page_title="Gemini Ultra Max", page_icon="✨", layout="wide")

# --- CSS MEWAH & ANIMASI GLOW ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e1e3f 0%, #050505 100%);
        color: #e3e3e3;
        font-family: 'Google Sans', sans-serif;
    }
    .gemini-title {
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570, #4285f4);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 65px;
        font-weight: 700;
        animation: shine 4s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .stChatInputContainer {
        border-radius: 35px !important;
        background: rgba(30, 31, 32, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6) !important;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 18, 0.7) !important;
        backdrop-filter: blur(20px);
    }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIKA API & ANTI-ERROR ---
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_img(file):
    return base64.b64encode(file.getvalue()).decode('utf-8')

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: white;'>Gemini Ultra</h1>", unsafe_allow_html=True)
    up_img = st.file_uploader("Upload Image (Vision)", type=["jpg", "png", "jpeg"])
    if st.button("🗑️ Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN UI ---
st.markdown("<h1 class='gemini-title'>Halo, Mahendra</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 22px; color: #9aa0a6;'>Ada yang bisa saya bantu hari ini?</p>", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- INPUT & RESPON CERDAS ---
if prompt := st.chat_input("Tanyakan sesuatu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        # OTOMATIS PILIH MODEL (Agar tidak error seperti Screenshot 275)
        if up_img:
            model = "llama-3.2-11b-vision-preview"
            msgs = [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_img(up_img)}"}}]}]
        else:
            model = "llama-3.3-70b-versatile"
            msgs = [{"role": "system", "content": "Anda adalah Gemini Ultra Max."}, 
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]]

        completion = client.chat.completions.create(model=model, messages=msgs, stream=True)
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            full_res += content
            placeholder.markdown(full_res + "▌")
        placeholder.markdown(full_res)
    st.session_state.messages.append({"role": "assistant", "content": full_res})import streamlit as st
from groq import Groq
import base64

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="ChatGPT Elite", page_icon="💬", layout="tight")

# --- CSS TEMA CHATGPT (CLEAN & PROFESSIONAL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    .stApp {
        background-color: #212121;
        color: #ececf1;
        font-family: 'Inter', sans-serif;
    }

    /* Menghilangkan Header & Footer */
    header, footer { visibility: hidden; }

    /* Gaya Sidebar ChatGPT */
    [data-testid="stSidebar"] {
        background-color: #171717 !important;
        border-right: 1px solid #333;
    }

    /* Container Chat */
    .stChatMessage {
        padding: 20px 10% !important;
        background-color: transparent !important;
    }
    
    /* Input Chat ala ChatGPT */
    .stChatInputContainer {
        padding: 0 10% !important;
        background: transparent !important;
    }
    
    .stChatInputContainer > div {
        border-radius: 12px !important;
        border: 1px solid #4d4d4d !important;
        background-color: #2f2f2f !important;
    }

    /* Judul Tengah */
    .gpt-title {
        text-align: center;
        font-size: 32px;
        font-weight: 600;
        margin-top: 15vh;
        color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEM API ---
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_img(file):
    return base64.b64encode(file.getvalue()).decode('utf-8')

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h3 style='text-align:center;'>ChatGPT Elite</h3>", unsafe_allow_html=True)
    if st.button("＋ Chat Baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    up_img = st.file_uploader("Lampirkan Gambar", type=["jpg", "png", "jpeg"])

# --- TAMPILAN UTAMA ---
if not st.session_state.messages:
    st.markdown("<div class='gpt-title'>Ada yang bisa saya bantu?</div>", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- INPUT LOGIC ---
if prompt := st.chat_input("Tulis pesan..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        # Deteksi Model Otomatis (Anti-Error)
        if up_img:
            model = "llama-3.2-11b-vision-preview"
            msgs = [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_img(up_img)}"}}]}]
        else:
            model = "llama-3.3-70b-versatile"
            msgs = [{"role": "system", "content": "Anda adalah ChatGPT, asisten AI yang sangat cerdas dan membantu."}, 
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]]

        completion = client.chat.completions.create(model=model, messages=msgs, stream=True)
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            full_res += content
            placeholder.markdown(full_res + "▌")
        placeholder.markdown(full_res)
    st.session_state.messages.append({"role": "assistant", "content": full_res})
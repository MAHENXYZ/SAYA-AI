import streamlit as st
from groq import Groq
import base64

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="ChatGPT Elite", page_icon="💬", layout="wide")

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
        
        if up_img:
            model = "llama-3.2-11b-vision-preview"
            msgs = [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_img(up_img)}"}}]}]
        else:
            model = "llama-3.3-70b-versatile"
            msgs = [{"role": "system", "content": "Anda adalah ChatGPT, asisten AI yang sangat cerdas."}, 
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]]

        completion = client.chat.completions.create(model=model, messages=msgs, stream=True)
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            full_res += content
            placeholder.markdown(full_res + "▌")
        placeholder.markdown(full_res)
    st.session_state.messages.append({"role": "assistant", "content": full_res})
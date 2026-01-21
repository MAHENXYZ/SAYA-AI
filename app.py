import streamlit as st
from groq import Groq
import os

# --- 1. SETTING HALAMAN PRO ---
st.set_page_config(
    page_title="Nexus AI - Professional Suite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (Tampilan Mewah) ---
st.markdown("""
    <style>
    /* Mengubah font dan background utama */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f8fafc;
    }

    /* Efek Kaca pada Chat */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Input Bar */
    .stChatInputContainer {
        padding-bottom: 2rem;
    }
    
    /* Header Animation */
    .main-title {
        background: linear-gradient(90deg, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIKA KONEKSI ---
api_key = st.secrets.get("GROQ_API_KEY") or "MASUKKAN_KEY_LOKAL_JIKA_PERLU"
client = Groq(api_key=api_key)

# --- 4. SIDEBAR CANGGIH ---
with st.sidebar:
    st.markdown("<h1 style='color: #60a5fa;'>NEXUS ENGINE</h1>", unsafe_allow_html=True)
    st.divider()
    
    # Fitur Multi-Model
    selected_model = st.selectbox(
        "Pilih Otak AI:",
        ["llama-3.3-70b-versatile", "llama3-70b-8192", "mixtral-8x7b-32768"],
        index=0,
        help="Llama 3.3 adalah yang paling cerdas saat ini."
    )
    
    # Fitur Kreativitas (Temperature)
    temp = st.slider("Kreativitas AI:", 0.0, 2.0, 0.7)
    
    st.divider()
    
    # Fitur Unggah Dokumen
    uploaded_file = st.file_uploader("📂 Analisis Dokumen (TXT)", type=["txt"])
    if st.button("🗑️ Hapus Percakapan"):
        st.session_state.messages = []
        st.rerun()

# --- 5. TAMPILAN UTAMA ---
st.markdown("<h1 class='main-title'>Nexus AI Interface</h1>", unsafe_allow_html=True)
st.markdown("---")

# Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. PROSES AI ---
if prompt := st.chat_input("Apa yang bisa saya bantu hari ini?"):
    
    # Tambahkan Konteks Dokumen jika ada
    doc_context = ""
    if uploaded_file:
        doc_content = uploaded_file.read().decode("utf-8")
        doc_context = f"--- KONTEKS DOKUMEN ---\n{doc_content}\n---------------------\n"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream response (Efek mengetik)
        completion = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": "You are a professional AI assistant named Nexus."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                {"role": "user", "content": doc_context + prompt}
            ],
            temperature=temp,
            stream=True
        )
        
        for chunk in completion:
            full_response += (chunk.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
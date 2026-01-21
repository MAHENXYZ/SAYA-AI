import streamlit as st
from groq import Groq
import time
import io
import zipfile
import random

# [1] CONFIGURASI HALAMAN
st.set_page_config(page_title="NEURAL FLOW V3 | MULTI-FUNCTION", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .gemini-gradient {
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D4AF37);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.8rem;
    }
</style>
""", unsafe_allow_html=True)

# [2] ENGINE ROTASI API KEY (Agar Tidak Limit)
def call_ai_rotated(messages, model):
    # Mengambil list kunci dari st.secrets["GROQ_KEYS"] yang Anda buat tadi
    keys = st.secrets["GROQ_KEYS"]
    random.shuffle(keys) 
    
    for key in keys:
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,
                max_tokens=4000
            )
            return completion.choices[0].message.content
        except Exception as e:
            if "rate_limit" in str(e).lower():
                continue # Coba key lain jika limit
            st.error(f"Kesalahan pada key: {e}")
    return None

# [3] LOGIKA PEMBUATAN PROYEK RAKSASA
def build_massive_project(prompt, model):
    all_files = {}
    
    # Langkah 1: Arsitek merancang daftar file
    with st.status("🏗️ Merancang Struktur Proyek..."):
        arch_msg = [{"role": "system", "content": "You are a Senior Architect. List 20-40 filenames for this project. Output ONLY filenames separated by commas."},
                    {"role": "user", "content": prompt}]
        res = call_ai_rotated(arch_msg, model)
        if not res: return None
        filenames = [f.strip() for f in res.split(",")]

    # Langkah 2: Tukang menulis setiap file satu per satu
    progress = st.progress(0)
    for i, name in enumerate(filenames):
        with st.status(f"⚡ Menulis File ({i+1}/{len(filenames)}): {name}"):
            code_msg = [{"role": "system", "content": f"Write FULL production code for {name}. Context: {prompt}. Only code."},
                        {"role": "user", "content": f"Code for {name}"}]
            code = call_ai_rotated(code_msg, model)
            if code:
                all_files[name] = code
            time.sleep(1) # Jeda aman
        progress.progress((i + 1) / len(filenames))
    
    return all_files

# [4] MAIN UI
def main():
    st.markdown("<h1 class='gemini-gradient'>Neural Architect Unlimited</h1>", unsafe_allow_html=True)
    
    if "history" not in st.session_state:
        st.session_state.history = []

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        model = st.selectbox("Model Core", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        st.info(f"Aktif: {len(st.secrets['GROQ_KEYS'])} API Keys")

    # Render Chat
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # Chat Input
    if p := st.chat_input("Ketik 'Hai' untuk ngobrol atau jelaskan proyek Anda..."):
        st.session_state.history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)

        with st.chat_message("assistant"):
            # CEK APAKAH INI CHAT BIASA ATAU CODING
            coding_keywords = ["buat", "bikin", "proyek", "coding", "aplikasi", "build"]
            is_coding = any(x in p.lower() for x in coding_keywords) or len(p.split()) > 15

            if is_coding:
                # MODE ARSITEK (PROSES LAMA)
                project_data = build_massive_project(p, model)
                if project_data:
                    zip_buf = io.BytesIO()
                    with zipfile.ZipFile(zip_buf, "w") as zf:
                        for n, c in project_data.items(): zf.writestr(n, c)
                    st.success("✅ Proyek Raksasa Selesai!")
                    st.download_button("📦 DOWNLOAD ZIP", zip_buf.getvalue(), "project.zip")
            else:
                # MODE CHAT BIASA (CEPAT)
                ans = call_ai_rotated([{"role": "user", "content": p}], model)
                st.markdown(ans)
                st.session_state.history.append({"role": "assistant", "content": ans})

if __name__ == "__main__":
    main()
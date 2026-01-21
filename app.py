import streamlit as st
from groq import Groq
import time
import io
import zipfile
import re
import random

# [1] CONFIG & LUXURY STYLE
st.set_page_config(page_title="NEURAL FLOW v3 | MULTI-FUNCTION", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .gemini-gradient {
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D4AF37);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.8rem;
    }
    .stDownloadButton button {
        background: linear-gradient(45deg, #1A73E8, #9B72CB) !important;
        color: white !important; border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# [2] MULTI-KEY ROTATION ENGINE
def call_ai_rotated(messages, model, stream=False):
    keys = st.secrets["GROQ_KEYS"]
    random.shuffle(keys)
    for key in keys:
        try:
            client = Groq(api_key=key)
            return client.chat.completions.create(model=model, messages=messages, stream=stream, max_tokens=4000)
        except Exception as e:
            if "rate_limit" in str(e).lower(): continue
            st.error(f"Error: {e}")
    return None

# [3] MODULAR CODING LOGIC (Untuk Proyek Besar)
def build_massive_project(prompt, model):
    # Tahap Arsitek
    with st.status("🏗️ Fase 1: Merancang Arsitektur Raksasa..."):
        arch_msg = [{"role": "system", "content": "You are a Senior Architect. Breakdown this request into 30-50 filenames. Output ONLY filenames separated by commas."},
                    {"role": "user", "content": prompt}]
        res = call_ai_rotated(arch_msg, model)
        if not res: return
        filenames = [f.strip() for f in res.choices[0].message.content.split(",")]
        st.write(f"Terencana: **{len(filenames)} file** akan dibuat.")

    # Tahap Pembangunan
    all_files = {}
    progress = st.progress(0)
    for i, name in enumerate(filenames):
        with st.status(f"⚡ Menulis File ({i+1}/{len(filenames)}): {name}"):
            code_msg = [{"role": "system", "content": f"Write FULL production code for {name}. Context: {prompt}. Just code, no talk."},
                        {"role": "user", "content": f"Generate code for {name}"}]
            code_res = call_ai_rotated(code_msg, model)
            if code_res:
                all_files[name] = code_res.choices[0].message.content
                time.sleep(1) # Cooldown
        progress.progress((i + 1) / len(filenames))
    
    return all_files

# [4] MAIN UI
def main():
    st.markdown("<h1 class='gemini-gradient'>Neural Flow Multi-AI</h1>", unsafe_allow_html=True)
    
    if "history" not in st.session_state: st.session_state.history = []

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        model = st.selectbox("Model Core", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        st.success(f"Aktif: {len(st.secrets['GROQ_KEYS'])} API Keys")
        if st.button("Clear Chat"):
            st.session_state.history = []
            st.rerun()

    # Chat Interface
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if p := st.chat_input("Ketik 'Hai' untuk ngobrol atau jelaskan proyek coding Anda..."):
        st.session_state.history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)

        with st.chat_message("assistant"):
            # DETEKSI: Apakah ini perintah coding berat?
            keywords = ["buat", "bikin", "proyek", "build", "code", "coding", "aplikasi"]
            is_coding = any(x in p.lower() for x in keywords) or len(p.split()) > 15

            if is_coding:
                project_data = build_massive_project(p, model)
                if project_data:
                    zip_buf = io.BytesIO()
                    with zipfile.ZipFile(zip_buf, "w") as zf:
                        for n, c in project_data.items(): zf.writestr(n, c)
                    
                    st.success("🔥 Proyek Raksasa Selesai!")
                    st.download_button("📦 DOWNLOAD FULL PROJECT (.ZIP)", data=zip_buf.getvalue(), file_name="massive_project.zip", mime="application/zip")
                    st.session_state.history.append({"role": "assistant", "content": f"Berhasil membangun proyek dengan {len(project_data)} file."})
            else:
                # Mode Chat Biasa
                res = call_ai_rotated([{"role": "user", "content": p}], model)
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.history.append({"role": "assistant", "content": ans})

if __name__ == "__main__":
    main()
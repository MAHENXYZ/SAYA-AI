import streamlit as st
from groq import Groq
import time
import io
import zipfile
import random

# [1] CONFIG & STYLE
st.set_page_config(page_title="NEURAL FLOW v3", page_icon="🚀", layout="wide")

def apply_design():
    st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .status-box { border: 1px solid #4285F4; padding: 10px; border-radius: 10px; background: #111; }
    .gemini-gradient {
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D4AF37);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# [2] ENGINE ROTASI API KEY
def get_ai_response(messages, model):
    """Fungsi yang otomatis mencoba API Key lain jika satu key limit"""
    # Ambil daftar key dari secrets
    keys = st.secrets["GROQ_KEYS"]
    random.shuffle(keys) # Acak urutan agar beban merata
    
    for key in keys:
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3, # Lebih rendah agar kode lebih stabil
                max_tokens=4000
            )
            return completion.choices[0].message.content
        except Exception as e:
            if "rate_limit" in str(e).lower():
                continue # Coba key berikutnya
            else:
                st.error(f"Error: {e}")
                return None
    return "SEMUA API KEY LIMIT. Tunggu 1 menit."

# [3] LOGIKA PEMBUATAN MODULAR
def main():
    apply_design()
    st.markdown("<h1 class='gemini-gradient'>Neural Architect Unlimited v3</h1>", unsafe_allow_html=True)
    st.caption("Mode: Multi-Key Rotation & Modular Construction Active")

    # Sidebar untuk kontrol
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Engine", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        st.info(f"Terdeteksi {len(st.secrets['GROQ_KEYS'])} API Keys aktif.")

    prompt = st.chat_input("Jelaskan proyek raksasa yang ingin Anda buat...")

    if prompt:
        # TAHAP 1: BLUEPRINTING (Si Arsitek)
        with st.status("🏗️ Fase 1: Membuat Arsitektur Proyek..."):
            blueprint_msg = [
                {"role": "system", "content": "You are a Senior Architect. Breakdown the user's request into a MASSIVE project. List every single file needed. Output ONLY filenames separated by commas. No prose."},
                {"role": "user", "content": f"Create a huge project for: {prompt}"}
            ]
            file_list_raw = get_ai_response(blueprint_msg, model)
            if not file_list_raw: return
            
            filenames = [f.strip() for f in file_list_raw.split(",")]
            st.write(f"Terencana: **{len(filenames)} file** akan dikerjakan.")

        # TAHAP 2: CODING (Si Tukang)
        all_project_files = {}
        progress = st.progress(0)
        
        container = st.container()
        for i, name in enumerate(filenames):
            with container:
                with st.status(f"⏳ Menulis File ({i+1}/{len(filenames)}): {name}..."):
                    code_msg = [
                        {"role": "system", "content": f"You are an Elite Coder. Project context: {prompt}. Write the complete code for the file '{name}'. Use best practices, high complexity, and full implementation."},
                        {"role": "user", "content": f"Write the code for {name}"}
                    ]
                    file_code = get_ai_response(code_msg, model)
                    all_project_files[name] = file_code
                    
                    # Update progress
                    progress.progress((i + 1) / len(filenames))
                    time.sleep(1) # Cooldown tipis

        # TAHAP 3: PACKAGING (Finalisasi)
        st.success(f"🔥 Selesai! Berhasil membangun {len(filenames)} file modul.")
        
        # Buat ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for n, c in all_project_files.items():
                zip_file.writestr(n, c)

        st.download_button(
            label="📥 DOWNLOAD FULL PRODUCTION CODE (.ZIP)",
            data=zip_buffer.getvalue(),
            file_name="ultra_project_output.zip",
            mime="application/zip",
            use_container_width=True
        )

if __name__ == "__main__":
    main()
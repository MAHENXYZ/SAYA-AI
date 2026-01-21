import streamlit as st
from groq import Groq
import time
import io
import zipfile
import random

# [1] TAMPILAN MEWAH
st.set_page_config(page_title="NEURAL ARCHITECT UNLIMITED", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .gemini-gradient {
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D4AF37);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# [2] ENGINE ROTASI API (Tanpa Batas)
def call_ai_with_rotation(messages, model):
    """Mencoba satu per satu API Key jika ada yang terkena limit"""
    keys = st.secrets["GROQ_KEYS"]
    random.shuffle(keys) # Acak agar beban terbagi rata
    
    for key in keys:
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2, # Lebih rendah agar kode lebih akurat
                max_tokens=4000
            )
            return completion.choices[0].message.content
        except Exception as e:
            # Jika limit, lanjut ke API Key berikutnya
            if "rate_limit" in str(e).lower():
                continue
            else:
                st.error(f"Error pada Key: {e}")
                continue
    return None

# [3] LOGIKA UTAMA
def main():
    st.markdown("<h1 class='gemini-gradient'>Neural Architect Unlimited</h1>", unsafe_allow_html=True)
    st.write(f"🚀 **Sistem Siap:** Menggunakan {len(st.secrets['GROQ_KEYS'])} API Keys untuk rotasi.")

    model = st.sidebar.selectbox("Pilih Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    prompt = st.chat_input("Apa proyek raksasa yang ingin Anda bangun hari ini?")

    if prompt:
        # TAHAP 1: SI ARSITEK (Membuat Blueprint)
        with st.status("🏗️ Fase 1: Merancang Struktur Folder & File..."):
            arch_msg = [
                {"role": "system", "content": "You are a Senior Software Architect. Breakdown the request into at least 30-50 separate files for a massive project. Output ONLY filenames separated by commas."},
                {"role": "user", "content": prompt}
            ]
            file_list_raw = call_ai_with_rotation(arch_msg, model)
            if not file_list_raw:
                st.error("Gagal memulai. Semua API Key mungkin sedang sibuk.")
                return
            
            filenames = [f.strip() for f in file_list_raw.split(",")]
            st.success(f"Blueprint Selesai: {len(filenames)} file akan dibangun.")

        # TAHAP 2: SI TUKANG (Membangun File satu per satu)
        all_files = {}
        prog_bar = st.progress(0)
        
        for idx, name in enumerate(filenames):
            with st.status(f"⚡ Sedang mengerjakan ({idx+1}/{len(filenames)}): {name}"):
                code_msg = [
                    {"role": "system", "content": f"You are an Elite Developer. Context: {prompt}. Write the COMPLETE and DETAILED code for the file: {name}. No talking, just code."},
                    {"role": "user", "content": f"Code for {name}"}
                ]
                code_result = call_ai_with_rotation(code_msg, model)
                all_files[name] = code_result
                
                # Jeda kecil agar API tidak kaget
                time.sleep(1.5)
            
            prog_bar.progress((idx + 1) / len(filenames))

        # TAHAP 3: PACKAGING (Selesai)
        st.success("✅ Semua file berhasil dibuat tanpa henti!")
        
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for n, c in all_files.items():
                if c: zf.writestr(n, c)

        st.download_button(
            label="📦 DOWNLOAD FULL PROJECT (.ZIP)",
            data=zip_buf.getvalue(),
            file_name="architect_massive_project.zip",
            mime="application/zip",
            use_container_width=True
        )

if __name__ == "__main__":
    main()
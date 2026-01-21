import streamlit as st
from groq import Groq
import time
import io
import zipfile
import re

# [1] ADVANCED PAGE CONFIGURATION
st.set_page_config(
    page_title="NEURAL FLOW | UNLIMITED ARCHITECT",
    page_icon="⚡",
    layout="wide"
)

# [2] LUXURY DESIGN SYSTEM
def apply_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #050505; color: #E0E0E0; font-family: 'Inter', sans-serif; }
    .gemini-gradient {
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D4AF37);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.8rem;
    }
    .stDownloadButton button {
        background: linear-gradient(45deg, #1A73E8, #9B72CB) !important;
        color: white !important; border-radius: 12px !important;
        border: none !important; font-weight: bold !important;
        transition: 0.3s; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# [3] MULTI-FILE ZIP GENERATOR
def create_zip_from_code(full_text):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "x", zipfile.ZIP_DEFLATED) as vk:
        # Mencari pola penamaan file otomatis: # filename: example.py
        file_blocks = re.findall(r"(?://|#)\s*filename:\s*([\w\.]+)\n```(?:\w+)?\n(.*?)\n```", full_text, re.DOTALL)
        if file_blocks:
            for name, content in file_blocks:
                vk.writestr(name, content.strip())
        else:
            vk.writestr("full_project_code.txt", full_text)
    return buf.getvalue()

# [4] TRUE NO-LIMIT ENGINE (RECURSIVE & PROTECTED)
def generate_unlimited_code(prompt, model):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    full_response = ""
    placeholder = st.empty()
    
    # Instruksi sistem yang sangat ketat untuk menghindari looping sampah
    messages = [
        {"role": "system", "content": "You are an Elite Developer. Provide full, production-ready code. Use '# filename: name.ext' before code blocks. If the code is long, DO NOT say 'To be continued' or 'Dan seterusnya'. Just stop, so I can ask you to continue. Be 100% efficient."},
        {"role": "user", "content": prompt}
    ]
    
    iteration = 0
    # Mendukung hingga 20 iterasi (~60.000+ token)
    while iteration < 20:
        try:
            # Jeda adaptif untuk mendinginkan API Groq
            if iteration > 0:
                time.sleep(6) # Cooldown wajib
            
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                max_tokens=3000 # Ukuran optimal untuk menghindari limit mendadak
            )
            
            chunk_text = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    chunk_text += content
                    full_response += content
                    placeholder.markdown(full_response + " █")
            
            # Deteksi apakah semua blok kode sudah ditutup
            if full_response.strip().endswith("```") and full_response.count("```") % 2 == 0:
                break
            
            # Menambahkan konteks untuk kelanjutan
            messages.append({"role": "assistant", "content": chunk_text})
            messages.append({"role": "user", "content": "The code is cut off. CONTINUE immediately from the very last character. No introduction, just the remaining code."})
            iteration += 1
            
        except Exception as e:
            if "rate_limit" in str(e).lower():
                st.warning("⚠️ Memasuki fase pendinginan API (25 detik)...")
                time.sleep(25)
                continue
            else:
                st.error(f"Sistem Error: {e}")
                break
                
    placeholder.markdown(full_response)
    return full_response

# [5] MAIN UI LOGIC
def main():
    apply_style()
    st.markdown("<h1 class='gemini-gradient'>Neural Architect Unlimited</h1>", unsafe_allow_html=True)
    
    if "history" not in st.session_state:
        st.session_state.history = []

    with st.sidebar:
        st.header("⚙️ Intelligent Controls")
        model = st.selectbox("Model Core", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        st.divider()
        st.write("🚀 **No-Limit Mode: Active**")
        st.caption("AI akan menulis beribu baris dan menyambung otomatis sampai selesai.")
        if st.button("Reset Memory"):
            st.session_state.history = []
            st.rerun()

    # Render Chat History
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if p := st.chat_input("Deskripsikan tugas coding raksasa Anda..."):
        st.session_state.history.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)

        with st.chat_message("assistant"):
            # Memanggil fungsi No-Limit
            final_res = generate_unlimited_code(p, model)
            st.session_state.history.append({"role": "assistant", "content": final_res})
            
            # Export Buttons
            st.markdown("---")
            zip_file = create_zip_from_code(final_res)
            st.download_button(
                label="📦 DOWNLOAD FULL PROJECT (.ZIP)",
                data=zip_file,
                file_name="architect_project_files.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
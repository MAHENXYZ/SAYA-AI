import streamlit as st
from groq import Groq
import time
import io
import zipfile
import re

# [1] ADVANCED CONFIGURATION
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
    /* Tombol Download Mewah */
    .stDownloadButton button {
        background: linear-gradient(45deg, #1A73E8, #9B72CB) !important;
        color: white !important; border-radius: 12px !important;
        border: none !important; font-weight: bold !important;
        transition: 0.3s; width: 100%;
    }
    .stDownloadButton button:hover { transform: scale(1.02); opacity: 0.9; }
    </style>
    """, unsafe_allow_html=True)

# [3] MULTI-FILE ZIP ENGINE
def create_zip_from_code(full_text):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "x", zipfile.ZIP_DEFLATED) as vk:
        # Mencari pola # filename: namafile.py
        file_blocks = re.findall(r"(?://|#)\s*filename:\s*([\w\.]+)\n```(?:\w+)?\n(.*?)\n```", full_text, re.DOTALL)
        if file_blocks:
            for name, content in file_blocks:
                vk.writestr(name, content.strip())
        else:
            vk.writestr("generated_code.py", full_text)
    return buf.getvalue()

# [4] NO-LIMIT RECURSIVE ENGINE
def generate_no_limit_code(prompt, model):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    full_response = ""
    placeholder = st.empty()
    
    # System Prompt untuk memastikan AI tidak berhenti di tengah jalan
    messages = [
        {"role": "system", "content": "You are an Elite Developer. Provide full, extremely detailed code. Use '# filename: name.ext' for each file. If the code is long, do not summarize. I will ask you to continue until 100% finished."},
        {"role": "user", "content": prompt}
    ]
    
    iteration = 0
    max_iteration = 25 # Kapasitas hingga ~80.000 token

    while iteration < max_iteration:
        try:
            # Jeda adaptif untuk menghindari groq.RateLimitError
            wait_time = 5 if iteration < 5 else 10
            if iteration > 0:
                with st.spinner(f"Menyambung kode (Bagian {iteration+1})..."):
                    time.sleep(wait_time)
            
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                max_tokens=3500 # Ukuran aman per hit
            )
            
            chunk_text = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    chunk_text += content
                    full_response += content
                    placeholder.markdown(full_response + " █")
            
            # Cek apakah blok kode terakhir sudah ditutup (```)
            # Jika sudah ditutup dan tidak ada blok baru yang dibuka, berarti selesai
            if full_response.strip().endswith("```") and full_response.count("```") % 2 == 0:
                break
            
            # Update memori untuk request "Continue"
            messages.append({"role": "assistant", "content": chunk_text})
            messages.append({"role": "user", "content": "CONTINUE. Don't repeat, just continue the code exactly from where it cut off."})
            iteration += 1
            
        except Exception as e:
            if "rate_limit" in str(e).lower():
                st.warning("Rate limit terdeteksi. Sistem beristirahat 20 detik...")
                time.sleep(20)
                continue
            else:
                st.error(f"Error: {e}")
                break
                
    placeholder.markdown(full_response)
    return full_response

# [5] MAIN INTERFACE
def main():
    apply_style()
    st.markdown("<h1 class='gemini-gradient'>Neural Architect Unlimited</h1>", unsafe_allow_html=True)
    
    if "history" not in st.session_state:
        st.session_state.history = []

    with st.sidebar:
        st.header("⚙️ Core Settings")
        model = st.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        st.markdown("---")
        st.write("🚀 **Mode No-Limit Aktif**")
        st.caption("AI akan otomatis melakukan iterasi hingga kode selesai 100%.")
        if st.button("Reset Session"):
            st.session_state.history = []
            st.rerun()

    # Chat Display
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if p := st.chat_input("Deskripsikan sistem/aplikasi besar yang ingin Anda bangun..."):
        st.session_state.history.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)

        with st.chat_message("assistant"):
            final_code = generate_no_limit_code(p, model)
            st.session_state.history.append({"role": "assistant", "content": final_code})
            
            # Export Section
            st.markdown("---")
            zip_file = create_zip_from_code(final_code)
            st.download_button(
                label="📦 DOWNLOAD FULL PROJECT (.ZIP)",
                data=zip_file,
                file_name="architect_project.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
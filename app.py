import streamlit as st
from groq import Groq
import time
import io
import zipfile
import re

# [1] CONFIGURATION
st.set_page_config(
    page_title="NEURAL FLOW | MULTI-FILE ARCHITECT",
    page_icon="⚡",
    layout="wide"
)

# [2] LUXE STYLING
def apply_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #0A0A0A; color: #E0E0E0; font-family: 'Inter', sans-serif; }
    .stCodeBlock { border: 1px solid #30363D !important; border-radius: 10px !important; }
    .gemini-gradient {
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D4AF37);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.5rem;
    }
    .download-card {
        background: #161B22; border: 1px solid #30363D;
        padding: 20px; border-radius: 15px; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# [3] LOGIC: EXTRACT FILES FROM CODE
def create_zip_from_code(full_text):
    """Mencari blok kode dan menyimpannya sebagai file terpisah dalam ZIP"""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "x", zipfile.ZIP_DEFLATED) as vk:
        # Mencari pola: // filename: namafile.ext atau # filename: namafile.ext
        file_blocks = re.findall(r"(?://|#)\s*filename:\s*([\w\.]+)\n```(?:\w+)?\n(.*?)\n```", full_text, re.DOTALL)
        
        if file_blocks:
            for name, content in file_blocks:
                vk.writestr(name, content.strip())
        else:
            # Jika tidak ada format khusus, simpan semua sebagai main_code.py
            vk.writestr("main_project_code.py", full_text)
    return buf.getvalue()

# [4] CORE ENGINE: RECURSIVE GENERATION
def generate_unlimited_pro(prompt, model):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    full_res = ""
    placeholder = st.empty()
    
    messages = [
        {"role": "system", "content": "You are an Elite Developer. If creating a project, start each file with '# filename: name.ext' followed by the code block. Generate thousands of lines if needed. I will ask you to continue until finished."},
        {"role": "user", "content": prompt}
    ]
    
    iteration = 0
    while iteration < 20: # Kapasitas sangat besar
        try:
            if iteration > 0: time.sleep(4) # Rate limit protection
            
            stream = client.chat.completions.create(
                model=model, messages=messages, stream=True, max_tokens=3500
            )
            
            current_chunk = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    current_chunk += content
                    full_res += content
                    placeholder.markdown(full_res + " █")
            
            # Cek jika blok kode sudah tertutup sempurna
            if full_res.strip().endswith("```") and full_res.count("```") % 2 == 0:
                break
                
            messages.append({"role": "assistant", "content": current_chunk})
            messages.append({"role": "user", "content": "CONTINUE. No intro, just the rest of the code."})
            iteration += 1
        except Exception as e:
            st.error(f"Limit Reached: {e}")
            break
            
    return full_res

# [5] UI MAIN
def main():
    apply_style()
    st.markdown("<h1 class='gemini-gradient'>Neural Architect Pro</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530393318e3d91f45.svg", width=40)
        st.header("Intelligence Control")
        model = st.selectbox("Core", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        st.markdown("---")
        st.write("📂 **Features Active:**\n- Recursive Logic\n- Auto-Zip Packaging\n- Rate-Limit Shield")
        if st.button("Reset Session"):
            st.session_state.clear()
            st.rerun()

    if "history" not in st.session_state: st.session_state.history = []

    for m in st.session_state.history:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Apa project raksasa yang ingin Anda buat?"):
        st.session_state.history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)

        with st.chat_message("assistant"):
            final_output = generate_unlimited_pro(p, model)
            st.session_state.history.append({"role": "assistant", "content": final_output})
            
            # ZIP & Download Logic
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                zip_data = create_zip_from_code(final_output)
                st.download_button(
                    label="🎁 Download Project (.ZIP)",
                    data=zip_data,
                    file_name="neural_project.zip",
                    mime="application/zip",
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    label="📄 Download Raw Text (.txt)",
                    data=final_output,
                    file_name="raw_code.txt",
                    mime="text/plain",
                    use_container_width=True
                )

if __name__ == "__main__":
    main()
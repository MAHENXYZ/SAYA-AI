import streamlit as st
from groq import Groq
from pypdf import PdfReader
import time

# [CONFIG]
st.set_page_config(page_title="NEURAL FLOW PRO", layout="wide")

# [STYLING] Gemini-Inspired Dark Theme
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .gemini-gradient {
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D4AF37);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 32px; font-weight: bold;
    }
    .status-tag { color: #D4AF37; font-size: 12px; letter-spacing: 2px; }
</style>
""", unsafe_allow_html=True)

if "memory" not in st.session_state: st.session_state.memory = []

# --- CORE ENGINE: UNLIMITED CODE GENERATION ---
def generate_unlimited_response(prompt, model_choice):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    full_response = ""
    placeholder = st.empty()
    
    # System Instruction khusus untuk Coding tanpa batas
    messages = [
        {"role": "system", "content": "You are a Senior Full-Stack Architect. Provide complete, production-ready code. If the code is extremely long, do not truncate it. Finish the current thought and I will ask you to continue."},
        {"role": "user", "content": prompt}
    ]
    
    continue_generating = True
    iteration = 0

    while continue_generating and iteration < 10: # Limit 10x loop untuk keamanan
        with st.spinner("Neural engine processing..."):
            completion = client.chat.completions.create(
                model=model_choice,
                messages=messages,
                stream=True,
                max_tokens=4096 # Maksimal token per hit
            )
            
            partial_text = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    partial_text += content
                    full_response += content
                    placeholder.markdown(full_response + " █")
            
            # LOGIKA DETEKSI TERPOTONG:
            # Jika output tidak diakhiri dengan penutup markdown kode (```) 
            # atau terlihat seperti kalimat menggantung.
            if "```" in partial_text[-5:] or iteration > 5:
                continue_generating = False
            else:
                # Otomatis minta sambungan (Recursive call)
                messages.append({"role": "assistant", "content": partial_text})
                messages.append({"role": "user", "content": "The code was truncated. Continue exactly where you left off. Do not repeat the beginning, just continue the code."})
                iteration += 1
                time.sleep(1) # Bypass rate limit
                
    placeholder.markdown(full_response)
    return full_response

def main():
    st.markdown("<p class='status-tag'>SYSTEM ONLINE | UNLIMITED CODE MODE</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='gemini-gradient'>Neural Flow Architect</h1>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Intelligence Level", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        st.info("Mode 'Unlimited Code' aktif secara otomatis. AI akan terus menulis sampai blok kode ditutup (```).")
        if st.button("Clear Memory"):
            st.session_state.memory = []
            st.rerun()

    # Chat UI
    for msg in st.session_state.memory:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Tulis tugas coding yang sangat panjang di sini..."):
        st.session_state.memory.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            final_res = generate_unlimited_response(prompt, model)
            st.session_state.memory.append({"role": "assistant", "content": final_res})

if __name__ == "__main__":
    main()
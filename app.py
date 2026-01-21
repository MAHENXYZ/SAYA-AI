import streamlit as st
from groq import Groq
import json
import time
from pypdf import PdfReader
from PIL import Image
import io

# [CONFIG] Gemini-Inspired Premium Layout
st.set_page_config(
    page_title="GEMINI FLOW OS", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# [STYLING] Minimalist High-Tech Interface
def apply_gemini_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background-color: #0E1117;
        color: #E2E2E2;
        font-family: 'Inter', sans-serif;
    }

    /* Gradient Title ala Gemini */
    .gemini-title {
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 600;
        margin-bottom: 0px;
    }

    /* Chat Bubbles Modern */
    [data-testid="stChatMessage"] {
        border-radius: 20px !important;
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    /* Floating Input Bar */
    .stChatInputContainer {
        padding-bottom: 2rem;
    }

    /* Sidebar Glass */
    [data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D;
    }
    
    /* Premium Buttons */
    .stButton>button {
        border-radius: 50px;
        border: 1px solid #30363D;
        background: transparent;
        color: white;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: rgba(66, 133, 244, 0.1);
        border-color: #4285F4;
    }
    </style>
    """, unsafe_allow_html=True)

# [LOGIC] Session State & Auth
if "memory" not in st.session_state:
    st.session_state.memory = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def main():
    apply_gemini_styles()
    
    # --- HEADER ---
    st.markdown("<h1 class='gemini-title'>Gemini Flow</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#80868B; margin-bottom:2rem;'>Advanced Neural Multimodal Interface</p>", unsafe_allow_html=True)

    # --- SIDEBAR: KNOWLEDGE & VISION ---
    with st.sidebar:
        st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530393318e3d91f45.svg", width=50)
        st.divider()
        
        # Multimodal Input (Khas Gemini)
        st.subheader("🖼️ Vision & Data")
        uploaded_img = st.file_uploader("Upload Image for Analysis", type=['jpg', 'png', 'jpeg'])
        if uploaded_img:
            st.image(uploaded_img, caption="Image Processed", use_column_width=True)
            
        uploaded_pdf = st.file_uploader("Upload Document (PDF)", type=['pdf'])
        if uploaded_pdf:
            reader = PdfReader(uploaded_pdf)
            st.session_state.context = "\n".join([p.extract_text() for p in reader.pages])
            st.success("Document Ingested")

        st.divider()
        model_choice = st.selectbox("Intelligence Core", ["llama-3.3-70b-versatile", "llama-3.2-11b-vision-preview"])

    # --- CHAT ENGINE ---
    # Render History
    for msg in st.session_state.memory:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if prompt := st.chat_input("Ask Gemini Flow anything..."):
        st.session_state.memory.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # Gemini-style Prompt Engineering
            sys_msg = "You are Gemini Flow, a helpful and harmless AI assistant. Provide insightful, structured, and elegant responses."
            
            messages = [{"role": "system", "content": sys_msg}]
            # Tambahkan konteks dokumen jika ada
            if "context" in st.session_state:
                messages.append({"role": "system", "content": f"Context: {st.session_state.context[:3000]}"})
            
            # Tambahkan memori (history)
            messages.extend(st.session_state.memory[-6:])

            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_res = ""
                
                # Stream Response ala Gemini
                stream = client.chat.completions.create(
                    model=model_choice,
                    messages=messages,
                    stream=True
                )
                
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_res += content
                        placeholder.markdown(full_res + " ●") # Simbol kursor Gemini
                
                placeholder.markdown(full_res)
            
            st.session_state.memory.append({"role": "assistant", "content": full_res})

        except Exception as e:
            st.error(f"System Error: {str(e)}")

if __name__ == "__main__":
    main()
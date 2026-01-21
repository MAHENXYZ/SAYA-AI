import streamlit as st
from groq import Groq
import time
import io

# [1] INITIAL CONFIGURATION
st.set_page_config(
    page_title="NEURAL FLOW ARCHITECT PRO",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [2] PREMIUM STYLING (GEMINI DARK MODE)
def apply_custom_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600&display=swap');
    
    .stApp {
        background-color: #050505;
        color: #E2E2E2;
        font-family: 'Space Grotesk', sans-serif;
    }
    .gemini-text {
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D4AF37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    /* Style for Download Button */
    .stDownloadButton button {
        width: 100%;
        background: linear-gradient(45deg, #1A73E8, #9B72CB) !important;
        color: white !important;
        border: none !important;
        padding: 10px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# [3] CORE LOGIC: UNLIMITED CODE GENERATION
def generate_unlimited_code(prompt, model_choice):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    full_response = ""
    placeholder = st.empty()
    
    # Pesan awal sistem
    messages = [
        {"role": "system", "content": "You are a Senior Software Architect. Provide massive, detailed, and complete code implementations. If the code is long, do not stop until it is finished. I will handle the continuation logic."},
        {"role": "user", "content": prompt}
    ]
    
    iteration = 0
    max_iterations = 15 # Mendukung hingga ~30.000+ token
    
    while iteration < max_iterations:
        try:
            # Jeda antar request untuk menghindari RateLimitError
            if iteration > 0:
                time.sleep(4) 
                
            completion = client.chat.completions.create(
                model=model_choice,
                messages=messages,
                stream=True,
                max_tokens=3000 # Ukuran aman per chunk
            )
            
            partial_text = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    partial_text += content
                    full_response += content
                    placeholder.markdown(full_response + " █")
            
            # Deteksi apakah blok kode (```) sudah ditutup
            # Kami menghitung jumlah kemunculan ``` untuk memastikan genap (terbuka & tertutup)
            if full_response.count("```") % 2 == 0 and iteration > 0:
                break
            
            # Jika masih terbuka, minta AI lanjut
            messages.append({"role": "assistant", "content": partial_text})
            messages.append({"role": "user", "content": "The code is still incomplete. Continue strictly from the last character. No introduction, just code."})
            iteration += 1
            
        except Exception as e:
            if "rate_limit" in str(e).lower():
                st.warning("⚠️ Rate Limit Detected. Re-calibrating in 10s...")
                time.sleep(10)
                continue
            else:
                st.error(f"Neural Bridge Error: {e}")
                break
                
    placeholder.markdown(full_response)
    return full_response

# [4] MAIN INTERFACE
def main():
    apply_custom_style()
    
    # Sidebar
    with st.sidebar:
        st.markdown("<h1 class='gemini-text'>NEURAL FLOW</h1>", unsafe_allow_html=True)
        st.caption("v2.5.0 Professional Edition")
        st.divider()
        
        model = st.selectbox("Intelligence Core", [
            "llama-3.3-70b-versatile", 
            "mixtral-8x7b-32768"
        ])
        
        st.success("✅ Unlimited Code Mode: Active")
        st.info("Sistem akan otomatis melakukan 'Self-Correction' jika API memutus koneksi di tengah jalan.")
        
        if st.button("Clear System Memory"):
            st.session_state.chat_history = []
            st.rerun()

    # Chat History Setup
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Welcome Message
    st.markdown("<h2 class='gemini-text'>What are we building today?</h2>", unsafe_allow_html=True)

    # Display History
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # User Input
    if user_input := st.chat_input("Deskripsikan project besar Anda di sini..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            final_code = generate_unlimited_code(user_input, model)
            st.session_state.chat_history.append({"role": "assistant", "content": final_code})
            
            # FEATURE: AUTO-DOWNLOAD BUTTON
            st.divider()
            st.subheader("📦 Export Result")
            file_name = "generated_code_pro.py" # Bisa diubah manual
            st.download_button(
                label="Download Full Code (.py)",
                data=final_code,
                file_name=file_name,
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
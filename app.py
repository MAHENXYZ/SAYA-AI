import streamlit as st
from groq import Groq
import time, io, zipfile, random

# [1] CONFIG & STYLE
st.set_page_config(page_title="NEURAL FLOW V3", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #E0E0E0; }</style>", unsafe_allow_html=True)

# [2] ENGINE ROTASI API KEY (Agar Tidak Limit)
def call_ai(messages, model, max_tokens=4000):
    keys = st.secrets["GROQ_KEYS"]
    random.shuffle(keys) # Rotasi otomatis agar tidak limit
    for key in keys:
        try:
            client = Groq(api_key=key)
            return client.chat.completions.create(model=model, messages=messages, temperature=0.3, max_tokens=max_tokens)
        except: continue
    return None

# [3] MODULAR GENERATOR (Hanya untuk Proyek Raksasa)
def build_big_project(prompt, model):
    all_files = {}
    with st.status("🏗️ Merancang Struktur Proyek..."):
        res = call_ai([{"role": "system", "content": "List 15-30 filenames for this project. Comma separated only."}, {"role": "user", "content": prompt}], model)
        if not res: return None
        filenames = res.choices[0].message.content.split(",")
    
    progress = st.progress(0)
    for i, name in enumerate(filenames):
        name = name.strip()
        with st.status(f"⚡ Menulis {name}..."):
            code_res = call_ai([{"role": "system", "content": "Write full code. Code only."}, {"role": "user", "content": f"File: {name} for {prompt}"}], model)
            if code_res: all_files[name] = code_res.choices[0].message.content
        progress.progress((i + 1) / len(filenames))
    return all_files

# [4] LOGIKA UTAMA
def main():
    st.title("⚡ Neural Flow Multi-Function")
    if "history" not in st.session_state: st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if p := st.chat_input("Tulis pesan atau proyek raksasa..."):
        st.session_state.history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)

        with st.chat_message("assistant"):
            model = "llama-3.3-70b-versatile" # Model Core dari sidebar
            
            # SAKLAR PINTAR: Deteksi apakah ini proyek besar atau chat biasa
            is_big = any(x in p.lower() for x in ["proyek", "aplikasi", "massive", "lengkap"]) and len(p.split()) > 10

            if is_big:
                # Mode Arsitek (Lambat tapi Hebat)
                data = build_big_project(p, model)
                if data:
                    buf = io.BytesIO()
                    with zipfile.ZipFile(buf, "w") as zf:
                        for n, c in data.items(): zf.writestr(n, c)
                    st.download_button("📦 Download Project ZIP", buf.getvalue(), "project.zip")
            else:
                # Mode Chat Cepat (Instan)
                res = call_ai([{"role": "user", "content": p}], model)
                if res:
                    ans = res.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.history.append({"role": "assistant", "content": ans})

if __name__ == "__main__":
    main()
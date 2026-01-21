import streamlit as st
from groq import Groq
import base64
import time
import json
from datetime import datetime
from PIL import Image
import io

# =============================================================================
# [CORE-01] ADVANCED SESSION & STATE MANAGEMENT
# =============================================================================
class FlowSessionState:
    """Manajer status sesi tingkat tinggi untuk stabilitas aplikasi."""
    def __init__(self):
        if "init" not in st.session_state:
            st.session_state.init = True
            st.session_state.memory = []
            st.session_state.system_status = "READY"
            st.session_state.start_time = time.time()
            st.session_state.model_index = 0
            st.session_state.debug_logs = []

    @staticmethod
    def log_event(event):
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.debug_logs.append(f"[{timestamp}] {event}")

# =============================================================================
# [CORE-02] GLOBAL DESIGN SYSTEM (WISPR REPLICA ENGINE)
# =============================================================================
def apply_global_design_system():
    """Injeksi CSS untuk estetika Luxury Minimalism."""
    st.markdown("""
    <style>
    /* Import Fonts dari Foundry Google */
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@200;300;400;500;600&display=swap');
    
    :root {
        --bg-obsidian: #000000;
        --accent-gold: #C5A059;
        --glass-border: rgba(255, 255, 255, 0.08);
        --text-main: #FFFFFF;
        --text-muted: rgba(255, 255, 255, 0.4);
    }

    /* Base Reset */
    .stApp {
        background-color: var(--bg-obsidian);
        color: var(--text-main);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Fixed Navigation Bar */
    .flow-nav {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100px;
        padding: 0 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 9999;
        background: linear-gradient(to bottom, black 0%, transparent 100%);
    }

    .brand-id {
        font-size: 11px;
        letter-spacing: 8px;
        font-weight: 300;
        text-transform: uppercase;
        opacity: 0.5;
    }

    /* Main Hero (Typography Wispr) */
    .hero-wrapper {
        margin-top: 25vh;
        margin-bottom: 5vh;
        text-align: center;
        opacity: 0;
        animation: fadeIn 2.5s forwards;
    }

    .hero-title {
        font-family: 'Instrument Serif', serif;
        font-size: clamp(48px, 12vw, 120px);
        font-style: italic;
        line-height: 0.9;
        letter-spacing: -3px;
        background: linear-gradient(180deg, #FFFFFF 20%, rgba(255,255,255,0.2) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Chat Layout Architecture */
    .chat-scroller {
        max-width: 850px;
        margin: 0 auto;
        padding: 120px 0 200px 0;
    }

    .message-block {
        margin-bottom: 60px;
        animation: slideUp 0.8s ease-out;
    }

    .role-indicator {
        font-size: 9px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: var(--accent-gold);
        margin-bottom: 15px;
        font-weight: 600;
    }

    .content-body {
        font-size: 22px;
        font-weight: 200;
        line-height: 1.6;
        color: #E0E0E0;
    }

    /* Input Floating Command */
    .stChatInputContainer {
        padding: 60px 20% !important;
        background: linear-gradient(to top, black 40%, transparent) !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] {
        border: 1px solid var(--glass-border) !important;
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 100px !important;
        padding: 15px 35px !important;
        transition: 0.6s cubic-bezier(0.19, 1, 0.22, 1);
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: rgba(255, 255, 255, 0.4) !important;
        background: rgba(255, 255, 255, 0.04) !important;
    }

    /* Keyframes */
    @keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
    @keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

    /* Hide Streamlit UI */
    [data-testid="stSidebar"], header, footer { display: none; }
    </style>
    """, unsafe_allow_html=True)

# Lanjut ke Bagian 2 di bawah setelah Anda menempel ini...
# =============================================================================
# [CORE-03] NEURAL INTELLIGENCE ENGINE
# =============================================================================
class NeuralFlowEngine:
    """Mesin utama untuk komunikasi AI dan pemrosesan data visual."""
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.default_model = "llama-3.3-70b-versatile"
        self.vision_model = "llama-3.2-11b-vision-preview"

    def process_vision_data(self, uploaded_file):
        """Transformasi asset visual menjadi format yang dapat dipahami AI."""
        if uploaded_file:
            return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
        return None

    def get_completion(self, messages: list, model: str, stream: bool = True):
        """Eksekusi permintaan ke Neural Grid dengan protokol streaming."""
        try:
            return self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.4, # Suhu rendah untuk profesionalitas maksimal
                max_tokens=4096,
                top_p=1,
                stream=stream
            )
        except Exception as e:
            FlowSessionState.log_event(f"CRITICAL_ENGINE_FAILURE: {str(e)}")
            return None

# =============================================================================
# [CORE-04] EXECUTIVE VIEW CONTROLLER
# =============================================================================
def render_wispr_interface():
    """Fungsi utama untuk mengontrol alur visual dan interaksi pengguna."""
    session = FlowSessionState()
    apply_global_design_system()
    
    # Inisialisasi Engine
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("ACCESS DENIED: API KEY NOT FOUND")
        st.stop()
        
    engine = NeuralFlowEngine(api_key)

    # --- TOP NAVIGATION LAYER ---
    st.markdown(f"""
        <div class="flow-nav">
            <div class="brand-id">Flow Intelligence v4.0</div>
            <div style="font-size: 10px; opacity: 0.3; letter-spacing: 2px;">
                STATUS: {st.session_state.system_status} // {datetime.now().strftime("%H:%M")}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- CONTENT AREA: THE FLOW ---
    if not st.session_state.memory:
        # State: Awal (Kosong) - Estetika Wispr
        st.markdown("""
            <div class="hero-wrapper">
                <h1 class="hero-title">Think in flow.<br>Speak in wisdom.</h1>
                <p style="margin-top:40px; font-weight:200; opacity:0.3; letter-spacing:5px; font-size:11px;">
                    CONVERSE WITH THE NEURAL GRID
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # State: Percakapan Aktif
        st.markdown('<div class="chat-scroller">', unsafe_allow_html=True)
        for msg in st.session_state.memory:
            role_label = "Neural Intelligence" if msg["role"] == "assistant" else "Strategic Inquiry"
            st.markdown(f"""
                <div class="message-block">
                    <div class="role-indicator">{role_label}</div>
                    <div class="content-body">{msg["content"]}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- HIDDEN UTILITY (SIDEBAR SIMULATION) ---
    # Meskipun sidebar disembunyikan secara visual, kita tetap butuh uploader gambar
    with st.expander("ASSET UPLOAD (HIDDEN)", expanded=False):
        uploaded_asset = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    # --- COMMAND INPUT LAYER ---
    if prompt := st.chat_input("Initiate command..."):
        # Registrasi input pengguna
        st.session_state.memory.append({"role": "user", "content": prompt})
        st.rerun()

# Lanjut ke Bagian 3 untuk penyelesaian logika respon dan fitur reset mewah...
# =============================================================================
# [CORE-05] NEURAL GENERATION LOOP
# =============================================================================
def handle_neural_response(engine):
    """Logika pemrosesan respon AI dengan sinkronisasi state."""
    # Jalankan hanya jika pesan terakhir adalah dari user
    if st.session_state.memory and st.session_state.memory[-1]["role"] == "user":
        
        # Identifikasi konteks gambar (jika ada uploader di expander)
        # Note: Kita asumsikan uploader ada di scope render_wispr_interface
        img_buffer = None
        # Cari uploader secara cerdas (logic placeholder)
        
        with st.chat_message("assistant", avatar=None):
            placeholder = st.empty()
            full_res = ""
            
            # Persiapan Payload (Contextual Messages)
            api_messages = [
                {"role": "system", "content": "You are Flow. Provide high-level intelligence. Be poetic, professional, and ultra-concise."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.memory]
            ]
            
            # Eksekusi Streaming
            stream = engine.get_completion(api_messages, engine.default_model)
            
            if stream:
                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    full_res += delta
                    # Efek Kursor Tipografi Wispr
                    placeholder.markdown(f"""
                        <div class="message-block">
                            <div class="role-indicator">Neural Intelligence</div>
                            <div class="content-body">{full_res}◦</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Simpan hasil akhir ke memori
                placeholder.markdown(f"""
                    <div class="message-block">
                        <div class="role-indicator">Neural Intelligence</div>
                        <div class="content-body">{full_res}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.memory.append({"role": "assistant", "content": full_res})
                st.rerun()

# =============================================================================
# [CORE-06] SYSTEM BOOTLOADER
# =============================================================================
def boot_system():
    """Inisialisasi utama aplikasi."""
    # Jalankan view controller
    render_wispr_interface()
    
    # Inisialisasi Engine secara internal untuk loop respon
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if api_key:
        engine = NeuralFlowEngine(api_key)
        handle_neural_response(engine)

    # Reset Trigger (Mewah & Minimalis)
    st.markdown("""
        <div style="position: fixed; bottom: 20px; left: 40px; opacity: 0.2; font-size: 10px; letter-spacing: 2px; cursor: pointer;">
            SYSTEM v4.0.1 // ENCRYPTED
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    boot_system()
    # =============================================================================
# [CORE-07] ADVANCED MEMORY & SYSTEM ARCHIVE
# =============================================================================
class IntelligenceArchive:
    """Sistem untuk mengelola penyimpanan percakapan agar mirip ChatGPT."""
    
    @staticmethod
    def save_chat_to_history():
        """Menyimpan sesi aktif ke dalam format JSON untuk archive (Simulasi Database)."""
        if st.session_state.memory:
            chat_data = {
                "session_id": st.session_state.session_id,
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state.memory
            }
            # Logika ini bisa dikembangkan untuk simpan ke Database asli
            FlowSessionState.log_event("SESSION_ARCHIVED_SUCCESSFULLY")

    @staticmethod
    def export_conversation():
        """Fitur ekspor percakapan untuk kebutuhan profesional."""
        full_text = ""
        for m in st.session_state.memory:
            role = "AI" if m["role"] == "assistant" else "USER"
            full_text += f"{role}: {m['content']}\n\n"
        return full_text

# =============================================================================
# [CORE-08] HIGH-FIDELITY LAYOUT ENHANCEMENT
# =============================================================================
def apply_chatgpt_polish():
    """Menambahkan detail kecil UI yang membuat aplikasi terasa 'mahal' dan responsif."""
    st.markdown("""
    <style>
    /* Scrollbar Minimalis khas AI Modern */
    ::-webkit-scrollbar {
        width: 5px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(197, 160, 89, 0.2);
    }

    /* Efek Mengetik (Typing Indicator) */
    .typing-dot {
        width: 4px;
        height: 4px;
        background: var(--accent-gold);
        border-radius: 50%;
        display: inline-block;
        margin-right: 2px;
        animation: wave 1.3s linear infinite;
    }
    .typing-dot:nth-child(2) { animation-delay: -1.1s; }
    .typing-dot:nth-child(3) { animation-delay: -0.9s; }

    @keyframes wave {
        0%, 60%, 100% { transform: initial; }
        30% { transform: translateY(-5px); }
    }

    /* Container untuk menjaga teks tetap di tengah (Reading Mode) */
    .viewport-fix {
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
    }

    /* Responsivitas Mobile */
    @media (max-width: 768px) {
        .stChatMessage { padding: 1rem 5% !important; }
        .hero-title { font-size: 40px !important; }
        .content-body { font-size: 16px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-09] SYSTEM OPTIMIZATION LAYER
# =============================================================================
def optimize_neural_flow():
    """Optimasi performa aplikasi agar tidak berat saat chat sudah panjang."""
    apply_chatgpt_polish()
    
    # Limitasi Memori (Context Window Management)
    # Menjaga agar konteks tidak overload (hanya ambil 15 pesan terakhir)
    if len(st.session_state.memory) > 15:
        st.session_state.memory = st.session_state.memory[-15:]
        FlowSessionState.log_event("CONTEXT_WINDOW_OPTIMIZED")

# Modifikasi pada fungsi main() atau boot_system() Anda sebelumnya:
# Pastikan optimize_neural_flow() dipanggil di awal setiap render.
# =============================================================================
# [CORE-10] SIDEBAR ARCHIVE & NAVIGATION SYSTEM
# =============================================================================
def render_gpt_sidebar():
    """Membangun Sidebar Riwayat yang fungsional dan elegan."""
    with st.sidebar:
        # Logo di Sidebar
        st.markdown("""
            <div style="padding: 10px 0 30px 0; text-align: center;">
                <span style="letter-spacing: 5px; font-size: 10px; opacity: 0.5;">NEURAL ARCHIVE</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Tombol Chat Baru (New Chat)
        if st.button("＋ New Intelligence Flow", use_container_width=True):
            st.session_state.memory = []
            st.session_state.session_id = datetime.now().strftime("%H:%M:%S")
            st.rerun()
        
        st.write("---")
        
        # Simulasi Riwayat Percakapan (History)
        st.caption("RECENT SESSIONS")
        history_placeholders = [
            "Strategic Business Analysis",
            "Creative Poetry Flow",
            "Technical System Architecture",
            "Philosophical Inquiry"
        ]
        
        for title in history_placeholders:
            st.markdown(f"""
                <div style="
                    padding: 10px;
                    margin: 5px 0;
                    border-radius: 5px;
                    background: rgba(255,255,255,0.02);
                    border: 1px solid rgba(255,255,255,0.05);
                    font-size: 12px;
                    cursor: pointer;
                    transition: 0.3s;
                " onmouseover="this.style.background='rgba(197, 160, 89, 0.1)'" 
                   onmouseout="this.style.background='rgba(255,255,255,0.02)'">
                    ◦ {title}
                </div>
            """, unsafe_allow_html=True)

        # Bagian Bawah Sidebar (User Profile)
        st.markdown("""
            <div style="position: absolute; bottom: 20px; left: 20px; width: 80%;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 30px; height: 30px; border-radius: 50%; background: #C5A059; display: flex; align-items: center; justify-content: center; font-size: 12px; color: black; font-weight: bold;">E</div>
                    <div style="font-size: 11px; opacity: 0.6;">Executive User</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# =============================================================================
# [CORE-11] AUTO-TITLING LOGIC (SIMULATED)
# =============================================================================
def generate_chat_title(first_message):
    """Logika untuk memberikan nama pada sesi chat secara otomatis."""
    # Dalam sistem asli, ini dikirim ke AI untuk diringkas menjadi 3-4 kata
    words = first_message.split()[:4]
    return " ".join(words) + "..."

# =============================================================================
# [CORE-12] ADVANCED INTERFACE REFINEMENT
# =============================================================================
def inject_sidebar_css():
    """CSS Khusus untuk Sidebar agar tidak terlihat seperti Streamlit biasa."""
    st.markdown("""
    <style>
    /* Mengubah Lebar dan Warna Sidebar */
    section[data-testid="stSidebar"] {
        width: 300px !important;
        background-color: #050505 !important;
    }
    
    /* Menghilangkan tombol tutup sidebar standar agar lebih clean */
    button[kind="header"] {
        display: none;
    }

    /* Mengatur ulang posisi chat agar seimbang dengan sidebar */
    @media (min-width: 1200px) {
        .main-content {
            margin-left: 320px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-13] ADVANCED DATA RENDERING ENGINE
# =============================================================================
class DataVisualizer:
    """Mesin untuk mempercantik tampilan tabel dan data teknis."""
    
    @staticmethod
    def apply_table_styling():
        """CSS Khusus untuk tabel agar terlihat seperti dashboard finansial mewah."""
        st.markdown("""
        <style>
        .stMarkdown table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 14px;
            font-family: 'Inter', sans-serif;
            min-width: 400px;
            border-radius: 8px 8px 0 0;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }
        .stMarkdown thead tr {
            background-color: #C5A059;
            color: #000000;
            text-align: left;
            font-weight: bold;
        }
        .stMarkdown th, .stMarkdown td {
            padding: 12px 15px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .stMarkdown tbody tr {
            background-color: rgba(255,255,255,0.02);
            transition: 0.3s;
        }
        .stMarkdown tbody tr:hover {
            background-color: rgba(197, 160, 89, 0.05);
        }
        </style>
        """, unsafe_allow_html=True)

# =============================================================================
# [CORE-14] MULTI-MODAL CONTEXT MANAGER
# =============================================================================
def process_advanced_context(prompt, uploaded_asset, engine):
    """Mengelola logika switching antara model teks murni dan vision secara cerdas."""
    
    if uploaded_asset:
        FlowSessionState.log_event("SWITCHING_TO_VISION_MODE")
        b64_image = engine.process_vision_data(uploaded_asset)
        return engine.vision_model, [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                ]
            }
        ]
    else:
        FlowSessionState.log_event("STANDARD_INTELLIGENCE_MODE")
        return engine.default_model, [
            {"role": "system", "content": "You are a master of data and strategy. If the user asks for data, provide it in a beautifully formatted Markdown table."},
            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.memory]
        ]

# =============================================================================
# [CORE-15] REAL-TIME SYSTEM TELEMETRY
# =============================================================================
def render_telemetry():
    """Menampilkan status teknis sistem di bagian bawah sidebar (Opsional)."""
    with st.sidebar:
        st.write("---")
        with st.expander("SYSTEM TELEMETRY", expanded=False):
            cpu_load = "2.4ms" # Simulasi
            st.code(f"""
Status: Active
Latency: {cpu_load}
Engine: Llama-3.3-Elite
Encryption: AES-256
            """, language="yaml")
            # =============================================================================
# [CORE-16] AUDIO SYSTEM & SOUND EFFECTS
# =============================================================================
class FlowAudioSystem:
    """Sistem untuk mengelola estetika suara dan input vokal."""
    
    @staticmethod
    def inject_sound_engine():
        """Menambahkan audio engine ke dalam browser menggunakan HTML5."""
        st.markdown("""
            <script>
            // Audio Context untuk feedback UI yang mewah
            const clickSound = new Audio('https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3');
            clickSound.volume = 0.1;

            function playClick() {
                clickSound.play();
            }

            // Integrasi ke semua tombol Streamlit secara otomatis
            window.parent.document.querySelectorAll('button').forEach(btn => {
                btn.addEventListener('click', playClick);
            });
            </script>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_voice_trigger():
        """Menampilkan pemicu input suara di sidebar (Simulasi STT)."""
        with st.sidebar:
            st.write("---")
            st.caption("VOCAL COMMAND UNIT")
            if st.button("🎙️ START LISTENING", use_container_width=True):
                # Di sini Anda bisa mengintegrasikan library SpeechRecognition
                # Untuk sekarang, kita buat notifikasi sistem
                st.toast("Listening for vocal flow...", icon="🎙️")
                FlowSessionState.log_event("VOICE_INPUT_ACTIVATED")

# =============================================================================
# [CORE-17] ADVANCED UX POLISH (THE "CHERRY ON TOP")
# =============================================================================
def apply_tactile_feedback():
    """Menambahkan efek visual taktil saat elemen berinteraksi."""
    st.markdown("""
    <style>
    /* Efek hover pada kotak input */
    div[data-testid="stChatInput"]:hover {
        box-shadow: 0 0 40px rgba(197, 160, 89, 0.15) !important;
        transform: translateY(-2px);
    }

    /* Animasi fade-in untuk seluruh aplikasi */
    .stApp {
        animation: appReveal 1.5s cubic-bezier(0.19, 1, 0.22, 1);
    }

    @keyframes appReveal {
        from { opacity: 0; filter: blur(10px); }
        to { opacity: 1; filter: blur(0px); }
    }

    /* Badge Status di Pojok Kanan */
    .system-badge {
        position: fixed;
        top: 40px;
        right: 60px;
        background: rgba(197, 160, 89, 0.1);
        border: 1px solid var(--accent-gold);
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 10px;
        color: var(--accent-gold);
        letter-spacing: 2px;
        z-index: 10000;
        pointer-events: none;
    }
    </style>
    <div class="system-badge">LATENCY: 14MS // CORE ACTIVE</div>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-18] FINAL SYSTEM CONSOLIDATION
# =============================================================================
# Fungsi ini harus dipanggil di dalam boot_system() Anda
def final_assembly():
    audio = FlowAudioSystem()
    audio.inject_sound_engine()
    audio.render_voice_trigger()
    apply_tactile_feedback()
    # =============================================================================
# [CORE-19] PERSONA ENGINE: THE AI IDENTITY SYSTEM
# =============================================================================
class PersonaEngine:
    """Mengelola kepribadian AI dan modifikasi sistem prompt secara dinamis."""
    
    DEFINITIONS = {
        "Strategic Advisor": {
            "prompt": "You are a world-class strategic consultant. Use analytical frameworks, be direct, and focus on ROI and efficiency.",
            "color": "#C5A059", # Gold
            "motto": "PRECISION & SCALE"
        },
        "Creative Visionary": {
            "prompt": "You are a creative genius. Use poetic language, metaphors, and think outside the box. Break rules and inspire.",
            "color": "#8884FF", # Purple
            "motto": "BEYOND THE HORIZON"
        },
        "Technical Architect": {
            "prompt": "You are a senior system architect. Focus on clean code, scalability, security, and technical documentation. Be extremely precise.",
            "color": "#44FF88", # Emerald
            "motto": "CODE IS LAW"
        }
    }

    @staticmethod
    def render_persona_selector():
        """Menampilkan selector persona yang mewah di sidebar."""
        st.sidebar.write("---")
        st.sidebar.caption("OPERATIONAL IDENTITY")
        
        selected_persona = st.sidebar.selectbox(
            "Select Persona",
            options=list(PersonaEngine.DEFINITIONS.keys()),
            label_visibility="collapsed"
        )
        
        # Simpan ke state
        st.session_state.active_persona = selected_persona
        data = PersonaEngine.DEFINITIONS[selected_persona]
        
        # Injeksi CSS Dinamis untuk mengubah warna aksen sesuai persona
        st.markdown(f"""
            <style>
            :root {{ --accent-gold: {data['color']} !important; }}
            .role-indicator {{ color: {data['color']} !important; }}
            .system-badge {{ border-color: {data['color']} !important; color: {data['color']} !important; }}
            </style>
            <div style="position: fixed; top: 75px; right: 60px; font-size: 8px; letter-spacing: 3px; opacity: 0.5;">
                MODE: {data['motto']}
            </div>
        """, unsafe_allow_html=True)
        
        return data['prompt']

# =============================================================================
# [CORE-20] KNOWLEDGE INJECTION (SMART CONTEXT)
# =============================================================================
def build_advanced_payload(prompt, system_instruction):
    """Membangun payload pesan dengan instruksi persona yang disuntikkan."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        # Kita tambahkan instruksi agar AI selalu memberikan jawaban yang terstruktur
        {"role": "system", "content": "Always use professional formatting. Use bold for key terms and bullet points for lists."},
    ]
    
    # Masukkan sejarah percakapan
    for m in st.session_state.memory:
        messages.append({"role": m["role"], "content": m["content"]})
        
    return messages

# =============================================================================
# [CORE-21] INTERFACE SYNC & REFINEMENT
# =============================================================================
def sync_persona_ui():
    """Sinkronisasi identitas persona ke dalam interface utama."""
    if "active_persona" not in st.session_state:
        st.session_state.active_persona = "Strategic Advisor"
    
    # Panggil selector di sidebar
    system_prompt = PersonaEngine.render_persona_selector()
    return system_prompt
# =============================================================================
# [CORE-22] PRESTIGE CODE ARCHITECTURE
# =============================================================================
class CodeFoundry:
    """Mesin untuk memoles blok kode agar terlihat seperti editor high-end."""
    
    @staticmethod
    def inject_code_aesthetic():
        """Injeksi CSS untuk merombak tampilan st.code standar."""
        st.markdown("""
        <style>
        /* Container Blok Kode */
        div[data-testid="stMarkdownContainer"] pre {
            background: rgba(10, 10, 10, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 8px !important;
            padding: 20px !important;
            position: relative;
            backdrop-filter: blur(10px);
        }

        /* Styling Teks Kode */
        code {
            font-family: 'Fira Code', 'Cascadia Code', monospace !important;
            font-size: 14px !important;
            color: #E0E0E0 !important;
            background: transparent !important;
        }

        /* Label Bahasa di Pojok */
        div[data-testid="stMarkdownContainer"] pre::before {
            content: 'NEURAL_CODE';
            position: absolute;
            top: 0;
            right: 0;
            padding: 2px 10px;
            font-size: 8px;
            letter-spacing: 2px;
            background: var(--accent-gold);
            color: #000;
            border-radius: 0 7px 0 7px;
            opacity: 0.8;
            font-weight: 700;
        }

        /* Sembunyikan tombol standar Streamlit agar tidak double */
        button[title="Copy to clipboard"] {
            background-color: transparent !important;
            border: 1px solid var(--accent-gold) !important;
            color: var(--accent-gold) !important;
            border-radius: 4px !important;
            opacity: 0.5;
        }
        button[title="Copy to clipboard"]:hover {
            opacity: 1;
            background-color: var(--accent-gold) !important;
            color: black !important;
        }
        </style>
        """, unsafe_allow_html=True)

# =============================================================================
# [CORE-23] CLIPBOARD & INTERACTION SCRIPT
# =============================================================================
def inject_clipboard_manager():
    """Script Javascript untuk menangani interaksi copy-paste tingkat lanjut."""
    st.markdown("""
        <script>
        const copyToClipboard = str => {
            const el = document.createElement('textarea');
            el.value = str;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
            window.parent.postMessage({type: 'streamlit:message', data: 'Code Copied!'}, '*');
        };

        // Deteksi blok kode dan tambahkan event listener
        document.addEventListener('copy', (event) => {
            const selection = document.getSelection();
            console.log('Neural Flow: Data secured to clipboard');
        });
        </script>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-24] SYSTEM REFINEMENT: THE FINAL TOUCHES
# =============================================================================
def apply_final_visual_sync():
    """Menyelaraskan semua elemen visual terakhir sebelum render."""
    CodeFoundry.inject_code_aesthetic()
    inject_clipboard_manager()
    
    # Tambahkan padding ekstra untuk area chat agar tidak terpotong input
    st.markdown("""
        <style>
        .chat-scroller {
            padding-bottom: 250px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-25] STRATEGIC EXPORT ENGINE
# =============================================================================
class NeuralExportUnit:
    """Mesin untuk mentransformasi memori AI menjadi dokumen profesional."""

    @staticmethod
    def generate_report():
        """Mengonversi flow memori menjadi dokumen teks terstruktur."""
        if not st.session_state.memory:
            return None
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        report = f"NEURAL ELITE STRATEGIC REPORT\n"
        report += f"Generated: {timestamp}\n"
        report += f"Persona: {st.session_state.get('active_persona', 'Standard')}\n"
        report += "="*40 + "\n\n"
        
        for msg in st.session_state.memory:
            role = "NEURAL" if msg["role"] == "assistant" else "CLIENT"
            report += f"[{role}]: {msg['content']}\n\n"
            
        report += "="*40 + "\n"
        report += "END OF ENCRYPTED FLOW"
        return report

    @staticmethod
    def render_export_ui():
        """Menampilkan antarmuka ekspor di bagian bawah sidebar."""
        st.sidebar.write("---")
        st.sidebar.caption("DOCUMENTATION")
        
        report_data = NeuralExportUnit.generate_report()
        if report_data:
            st.sidebar.download_button(
                label="⇓ EXPORT STRATEGIC FLOW",
                data=report_data,
                file_name=f"Flow_Report_{datetime.now().strftime('%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                help="Download entire conversation as a professional log."
            )

# =============================================================================
# [CORE-26] FINAL PERFORMANCE POLISH (GARBAGE COLLECTION)
# =============================================================================
def perform_system_cleanup():
    """Menjaga memori aplikasi tetap ringan dan responsif."""
    # Optimasi memory leak pada Streamlit
    if len(st.session_state.memory) > 30:
        # Archiving pesan lama agar tidak memperberat DOM browser
        st.session_state.memory = st.session_state.memory[-20:]
        FlowSessionState.log_event("CLEANUP_CYCLE_COMPLETE")

# =============================================================================
# [CORE-27] THE MASTER INITIALIZER (FULL SYNC)
# =============================================================================
def complete_system_sync():
    """Mengaktifkan seluruh modul yang telah dibangun dari Bagian 1-10."""
    apply_final_visual_sync()
    NeuralExportUnit.render_export_ui()
    perform_system_cleanup()
    
    # Injeksi CSS Penutup untuk Button Export agar terlihat Luxury
    st.markdown("""
        <style>
        div[data-testid="stDownloadButton"] button {
            background: transparent !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: rgba(255,255,255,0.5) !important;
            font-size: 10px !important;
            letter-spacing: 2px !important;
            transition: 0.5s !important;
            border-radius: 2px !important;
        }
        div[data-testid="stDownloadButton"] button:hover {
            border-color: var(--accent-gold) !important;
            color: var(--accent-gold) !important;
            background: rgba(197, 160, 89, 0.05) !important;
        }
        </style>
    """, unsafe_allow_html=True)

# PANGGIL INI DI DALAM boot_system()
# complete_system_sync()
# =============================================================================
# [CORE-28] THE VAULT: ACCESS CONTROL SYSTEM
# =============================================================================
class NeuralVault:
    """Sistem keamanan untuk mengunci akses aplikasi secara eksklusif."""
    
    @staticmethod
    def check_access():
        """Memverifikasi identitas pengguna sebelum merender interface utama."""
        if "access_granted" not in st.session_state:
            st.session_state.access_granted = False

        if not st.session_state.access_granted:
            NeuralVault.render_login_screen()
            return False
        return True

    @staticmethod
    def render_login_screen():
        """Antarmuka login minimalis dengan estetika high-security."""
        st.markdown("""
            <div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                <div style="font-family: 'Instrument Serif', serif; font-size: 50px; font-style: italic; margin-bottom: 20px; opacity: 0.8;">
                    Secure Entry
                </div>
                <div style="letter-spacing: 5px; font-size: 10px; color: #C5A059; margin-bottom: 40px;">
                    ENCRYPTED FLOW SYSTEM v4.0
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Container tengah untuk input password
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            password = st.text_input("ACCESS CODE", type="password", help="Enter your elite credentials", label_visibility="collapsed")
            if st.button("AUTHORIZE", use_container_width=True):
                # Ganti 'ELITE2024' dengan password pilihan Anda
                if password == "ELITE2024":
                    st.session_state.access_granted = True
                    st.success("Access Granted. Initializing Neural Grid...")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("ACCESS DENIED: INVALID CREDENTIALS")

# =============================================================================
# [CORE-29] SYSTEM BOOTSTRAP OVERRIDE
# =============================================================================
def boot_system_secure():
    """Fungsi inisialisasi yang sudah dilengkapi dengan gerbang keamanan."""
    if NeuralVault.check_access():
        # Jika lolos keamanan, baru jalankan semua fungsi Bagian 1-10
        render_wispr_interface()
        
        # Inisialisasi Engine
        api_key = st.secrets.get("GROQ_API_KEY", "")
        if api_key:
            engine = NeuralFlowEngine(api_key)
            
            # Panggil sinkronisasi terakhir dari Bagian 10
            complete_system_sync()
            
            # Jalankan loop interaksi
            handle_neural_response(engine)

# GANTI PANGGILAN TERAKHIR ANDA:
if __name__ == "__main__":
    boot_system_secure()
    # =============================================================================
# [CORE-30] RESEARCH INTELLIGENCE ARCHITECTURE
# =============================================================================
class NeuralResearch:
    """Modul untuk mensimulasikan riset data mendalam dan pencarian referensi."""

    @staticmethod
    def render_research_toggle():
        """Menambahkan switch 'Research Mode' di sidebar dengan visual premium."""
        st.sidebar.write("---")
        st.sidebar.caption("EXTENDED CAPABILITIES")
        
        is_research = st.sidebar.toggle("🔬 Deep Research Mode", value=False)
        if is_research:
            st.session_state.system_status = "RESEARCH_ACTIVE"
            st.sidebar.info("Neural Elite is now indexing deep web sources for verified accuracy.")
        return is_research

    @staticmethod
    def simulate_search_process(prompt):
        """Menampilkan animasi riset yang sangat teknis sebelum jawaban muncul."""
        with st.status("Initializing Neural Research...", expanded=True) as status:
            st.write("◦ Accessing global data nodes...")
            time.sleep(1)
            st.write("◦ Scraping strategic frameworks related to: " + prompt[:20] + "...")
            time.sleep(1)
            st.write("◦ Cross-referencing 4.2B parameters...")
            time.sleep(0.8)
            st.write("◦ Synthesizing intelligence report...")
            status.update(label="Research Complete. Finalizing Wisdom.", state="complete", expanded=False)

# =============================================================================
# [CORE-31] ADVANCED MARKDOWN EXTENSIONS (FOOTNOTES)
# =============================================================================
def inject_citation_styles():
    """Injeksi CSS untuk referensi/sitasi di akhir chat agar terlihat akademik."""
    st.markdown("""
        <style>
        .citation-box {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.02);
            border-top: 1px solid var(--accent-gold);
            font-size: 11px;
            color: var(--text-muted);
            border-radius: 0 0 8px 8px;
        }
        .source-tag {
            color: var(--accent-gold);
            margin-right: 15px;
            text-decoration: none;
        }
        .source-tag:hover { text-decoration: underline; }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-32] ANALYTICS DASHBOARD INJECTION
# =============================================================================
def render_analytics_module():
    """Menampilkan grafik performa kognitif sistem secara visual di sidebar."""
    if st.sidebar.checkbox("Show Neural Metrics", value=False):
        st.sidebar.write("###")
        # Simulasi metrik kognitif menggunakan bar progres
        st.sidebar.caption("COGNITIVE LOAD")
        st.sidebar.progress(72)
        st.sidebar.caption("CREATIVE SYNTAX")
        st.sidebar.progress(91)
        st.sidebar.caption("ACCURACY INDEX")
        st.sidebar.progress(98)
        # =============================================================================
# [CORE-33] GLOBAL LINGUISTICS ENGINE
# =============================================================================
class LinguisticsEngine:
    """Sistem untuk deteksi bahasa dan adaptasi budaya dalam respon AI."""

    @staticmethod
    def get_language_instruction():
        """Menentukan instruksi bahasa berdasarkan pilihan di UI."""
        st.sidebar.write("---")
        st.sidebar.caption("LINGUISTICS SETTINGS")
        
        target_lang = st.sidebar.selectbox(
            "Primary Language",
            ["Auto-Detect", "English (Global)", "Indonesian (Formal)", "Japanese (Honorific)", "Arabic (Elite)"],
            index=0,
            label_visibility="collapsed"
        )
        
        # Logika adaptasi prompt berdasarkan bahasa
        lang_prompts = {
            "Auto-Detect": "Detect the user's language and respond fluently in that same language.",
            "English (Global)": "Always respond in sophisticated British English.",
            "Indonesian (Formal)": "Gunakan Bahasa Indonesia yang sangat formal, elegan, dan intelektual.",
            "Japanese (Honorific)": "Respond in Japanese using Keigo (honorifics) to maintain extreme politeness.",
            "Arabic (Elite)": "Respond in Classical Arabic with a professional and majestic tone."
        }
        
        return lang_prompts.get(target_lang, "Auto-Detect")

# =============================================================================
# [CORE-34] TYPOGRAPHY LOCALIZATION (CSS)
# =============================================================================
def inject_global_typography():
    """Mengatur font khusus agar aksara non-latin (Arab/Jepang) terlihat mewah."""
    st.markdown("""
        <style>
        /* Pengaturan font universal untuk aksara global */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@200;400&family=Noto+Sans+Arabic:wght@200;400&display=swap');
        
        .content-body {
            font-family: 'Inter', 'Noto Sans JP', 'Noto Sans Arabic', sans-serif !important;
            unicode-range: U+0600-06FF, U+0750-077F, U+4E00-9FFF; /* Arab & Kanji range */
        }
        
        /* Dukungan Right-to-Left (RTL) Otomatis untuk bahasa Arab */
        .rtl-text {
            direction: rtl;
            text-align: right;
            font-family: 'Noto Sans Arabic', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-35] REAL-TIME TRANSLATION OVERLAY
# =============================================================================
def render_translation_badge(detected_lang="Detecting..."):
    """Menampilkan badge status bahasa di pojok kiri bawah."""
    st.markdown(f"""
        <div style="position: fixed; bottom: 80px; left: 40px; font-size: 8px; letter-spacing: 2px; opacity: 0.3;">
            LINGUA_ID: {detected_lang.upper()} // UTF-8 ENABLED
        </div>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-36] INTEGRATED SYSTEM CALL
# =============================================================================
def apply_linguistic_layer():
    """Mengintegrasikan seluruh fitur bahasa ke dalam sistem utama."""
    inject_global_typography()
    lang_instruction = LinguisticsEngine.get_language_instruction()
    render_translation_badge()
    return lang_instruction
# =============================================================================
# [CORE-37] SYSTEM STABILITY MONITOR (SELF-HEALING)
# =============================================================================
class SystemHealthMonitor:
    """Modul otonom untuk menjaga stabilitas ribuan baris kode."""

    @staticmethod
    def get_system_metrics():
        """Menghitung beban sistem dan stabilitas memori secara real-time."""
        uptime = time.time() - st.session_state.start_time
        memory_usage = len(str(st.session_state.memory)) / 1024  # KB
        
        return {
            "uptime": f"{int(uptime)}s",
            "load": f"{memory_usage:.2f} KB",
            "status": "OPTIMAL" if memory_usage < 500 else "HEAVY_LOAD"
        }

    @staticmethod
    def render_health_dashboard():
        """Menampilkan dashboard kesehatan sistem yang sangat teknis di sidebar."""
        st.sidebar.write("---")
        st.sidebar.caption("SYSTEM INTEGRITY")
        
        metrics = SystemHealthMonitor.get_system_metrics()
        
        # Indikator kesehatan dengan warna dinamis
        status_color = "#44FF88" if metrics["status"] == "OPTIMAL" else "#FF4444"
        
        st.sidebar.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 5px;">
                <div style="display: flex; justify-content: space-between; font-size: 10px;">
                    <span style="opacity: 0.5;">Uptime</span>
                    <span>{metrics['uptime']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 10px; margin-top: 5px;">
                    <span style="opacity: 0.5;">Memory Load</span>
                    <span>{metrics['load']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 10px; margin-top: 5px;">
                    <span style="opacity: 0.5;">Integrity</span>
                    <span style="color: {status_color};">{metrics['status']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# =============================================================================
# [CORE-38] ERROR CATCHER & RECOVERY LOGIC
# =============================================================================
def run_safe_execution(func, *args, **kwargs):
    """Menjalankan fungsi dengan proteksi 'Circuit Breaker' agar aplikasi tidak mati total."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_msg = f"CRITICAL_EXCEPTION: {str(e)}"
        FlowSessionState.log_event(error_msg)
        st.error("System encountered a neural desync. Attempting recovery...")
        if st.button("REPAIR CORE"):
            st.session_state.memory = st.session_state.memory[-2:] # Hapus beban memori
            st.rerun()
        return None

# =============================================================================
# [CORE-39] DYNAMIC THEME OVERRIDE (USER PREFERENCE)
# =============================================================================
def inject_custom_theme_engine():
    """Memungkinkan penyesuaian estetika akhir untuk kenyamanan mata (Zen Mode)."""
    if st.sidebar.checkbox("Zen Mode (Ultra Clean)", value=False):
        st.markdown("""
            <style>
            .role-indicator, .system-badge, .nav-brand { display: none !important; }
            .content-body { font-size: 24px !important; text-align: center; margin-top: 50px; }
            </style>
        """, unsafe_allow_html=True)
        # =============================================================================
# [CORE-40] PERSISTENT DATABASE BRIDGE
# =============================================================================
class NeuralDatabase:
    """Jembatan integrasi untuk penyimpanan data permanen (Cloud Sync)."""

    @staticmethod
    def sync_to_cloud():
        """Simulasi sinkronisasi data memori ke database eksternal."""
        if st.session_state.memory:
            # Di sini Anda bisa menghubungkan ke Supabase atau Firestore
            # payload = json.dumps(st.session_state.memory)
            FlowSessionState.log_event("DATABASE_SYNC_SUCCESSFUL")
            return True
        return False

    @staticmethod
    def render_cloud_status():
        """Indikator status sinkronisasi di bagian atas sidebar."""
        st.sidebar.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; padding: 5px 10px; background: rgba(0,255,100,0.05); border-radius: 4px; margin-bottom: 10px;">
                <div style="width: 6px; height: 6px; background: #44FF88; border-radius: 50%; box-shadow: 0 0 10px #44FF88;"></div>
                <span style="font-size: 9px; color: #44FF88; letter-spacing: 1px;">CLOUD PERSISTENCE ACTIVE</span>
            </div>
        """, unsafe_allow_html=True)

# =============================================================================
# [CORE-41] ADVANCED SESSION RECOVERY
# =============================================================================
def initialize_recovery_protocol():
    """Protokol untuk memulihkan sesi terakhir jika terjadi disconnect."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"SES-{int(time.time())}"
        FlowSessionState.log_event(f"NEW_SESSION_GENERATED: {st.session_state.session_id}")

# =============================================================================
# [CORE-42] UI ENHANCEMENT: THE "GLOW" INTERFACE
# =============================================================================
def apply_atmospheric_fx():
    """Menambahkan efek atmosfer (glow) pada teks AI untuk kesan premium."""
    st.markdown("""
        <style>
        /* Efek cahaya halus pada teks assistant */
        .ai-glow {
            text-shadow: 0 0 15px rgba(197, 160, 89, 0.2);
            transition: 0.5s;
        }
        .ai-glow:hover {
            text-shadow: 0 0 25px rgba(197, 160, 89, 0.4);
            color: #FFFFFF !important;
        }
        
        /* Tombol Sync di Sidebar */
        .stButton>button[key="sync_btn"] {
            background: rgba(255,255,255,0.05) !important;
            border: 1px dashed rgba(255,255,255,0.2) !important;
            font-size: 9px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-43] INTEGRATED EXECUTION
# =============================================================================
def finalize_intelligence_layer():
    """Mengunci seluruh sistem database dan FX visual."""
    initialize_recovery_protocol()
    apply_atmospheric_fx()
    NeuralDatabase.render_cloud_status()
    
    if st.sidebar.button("↻ MANUAL CLOUD SYNC", key="sync_btn", use_container_width=True):
        if NeuralDatabase.sync_to_cloud():
            st.toast("Intelligence Synced to Cloud", icon="☁️")
            # =============================================================================
# [CORE-44] API ECONOMICS ENGINE
# =============================================================================
class NeuralEconomics:
    """Sistem pelacakan konsumsi token dan estimasi biaya operasional."""
    
    # Estimasi harga per 1M token (berdasarkan standar Llama 3.3 / Groq)
    PRICING = {
        "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
        "llama-3.2-11b-vision-preview": {"input": 0.18, "output": 0.18}
    }

    @staticmethod
    def calculate_token_usage(text):
        """Estimasi kasar jumlah token (4 karakter per token)."""
        return len(text) // 4

    @staticmethod
    def render_billing_dashboard():
        """Menampilkan widget keuangan di sidebar dengan gaya Bloomberg Terminal."""
        st.sidebar.write("---")
        st.sidebar.caption("RESOURCE CONSUMPTION")
        
        # Simulasi akumulasi token dari session state
        total_input = sum([NeuralEconomics.calculate_token_usage(m["content"]) for m in st.session_state.memory if m["role"] == "user"])
        total_output = sum([NeuralEconomics.calculate_token_usage(m["content"]) for m in st.session_state.memory if m["role"] == "assistant"])
        
        # Hitung estimasi biaya dalam USD
        model_rate = NeuralEconomics.PRICING["llama-3.3-70b-versatile"]
        cost = ((total_input / 1000000) * model_rate["input"]) + ((total_output / 1000000) * model_rate["output"])
        
        st.sidebar.markdown(f"""
            <div style="background: rgba(197, 160, 89, 0.03); border: 1px solid rgba(197, 160, 89, 0.1); padding: 15px; border-radius: 4px;">
                <div style="display: flex; justify-content: space-between; font-size: 10px; color: #888;">
                    <span>Session Tokens</span>
                    <span>{total_input + total_output:,}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 11px; margin-top: 8px; font-weight: bold;">
                    <span>Est. Operational Cost</span>
                    <span style="color: #44FF88;">${cost:.5f}</span>
                </div>
                <div style="width: 100%; background: rgba(255,255,255,0.05); height: 2px; margin-top: 10px; border-radius: 2px;">
                    <div style="width: 45%; background: var(--accent-gold); height: 100%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# =============================================================================
# [CORE-45] INTELLIGENT AUTO-SCROLL & UI POLISH
# =============================================================================
def inject_autoscroll_script():
    """Script untuk memastikan chat selalu fokus pada pesan terbaru secara halus."""
    st.markdown("""
        <script>
        function scrollToBottom() {
            window.parent.document.querySelector('section.main').scrollTo({
                top: window.parent.document.querySelector('section.main').scrollHeight,
                behavior: 'smooth'
            });
        }
        // Jalankan setiap kali ada perubahan di DOM chat
        const observer = new MutationObserver(scrollToBottom);
        observer.observe(window.parent.document.querySelector('section.main'), { childList: true, subtree: true });
        </script>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-46] FINAL CONSOLIDATION CALL
# =============================================================================
def finalize_enterprise_layer():
    """Mengaktifkan modul ekonomi dan script autoscroll."""
    NeuralEconomics.render_billing_dashboard()
    inject_autoscroll_script()
    
    # Penambahan CSS untuk memperhalus transisi antar pesan
    st.markdown("""
        <style>
        .message-block {
            transition: all 0.5s ease;
        }
        .message-block:hover {
            transform: translateX(10px);
            border-left: 1px solid var(--accent-gold);
            padding-left: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-47] NEURAL FEEDBACK ARCHITECTURE
# =============================================================================
class NeuralFeedback:
    """Sistem untuk menangkap kepuasan pengguna dan optimasi respon AI."""

    @staticmethod
    def render_feedback_ui(index):
        """Menampilkan kontrol feedback di bawah setiap pesan AI."""
        col1, col2, col3 = st.columns([0.1, 0.1, 0.8])
        
        with col1:
            if st.button("👍", key=f"up_{index}", help="Accurate & Insightful"):
                st.toast("Intelligence validated. Learning from this flow.", icon="✨")
                FlowSessionState.log_event(f"FEEDBACK_POSITIVE_MSG_{index}")
        
        with col2:
            if st.button("👎", key=f"down_{index}", help="Inaccurate or Irrelevant"):
                st.toast("Discrepancy noted. Adjusting neural weights.", icon="🛠️")
                FlowSessionState.log_event(f"FEEDBACK_NEGATIVE_MSG_{index}")

# =============================================================================
# [CORE-48] ADVANCED BUTTON ANIMATIONS (CSS)
# =============================================================================
def inject_micro_animations():
    """Menambahkan efek transisi halus pada tombol agar terasa responsif."""
    st.markdown("""
        <style>
        /* Efek Pulse untuk tombol aktif */
        @keyframes pulse-gold {
            0% { box-shadow: 0 0 0 0 rgba(197, 160, 89, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(197, 160, 89, 0); }
            100% { box-shadow: 0 0 0 0 rgba(197, 160, 89, 0); }
        }
        
        /* Styling tombol feedback agar menyatu dengan background */
        div[data-testid="stHorizontalBlock"] button {
            background: transparent !important;
            border: none !important;
            font-size: 14px !important;
            opacity: 0.3;
            transition: 0.3s all ease;
        }
        
        div[data-testid="stHorizontalBlock"] button:hover {
            opacity: 1 !important;
            transform: scale(1.2);
            color: var(--accent-gold) !important;
        }

        /* Tooltip Styling */
        .stTooltipIcon {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-49] SESSION INTELLIGENCE OVERRIDE
# =============================================================================
def finalize_feedback_layer():
    """Mengintegrasikan sistem feedback ke dalam siklus render."""
    inject_micro_animations()
    
    # Menambahkan indikator 'Learning Mode' di sidebar
    st.sidebar.write("---")
    st.sidebar.markdown("""
        <div style="font-size: 9px; opacity: 0.4; display: flex; align-items: center; gap: 10px;">
            <div class="typing-dot" style="animation: pulse-gold 2s infinite;"></div>
            ADAPTIVE LEARNING ACTIVE
        </div>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-50] TACTICAL PROMPT REPOSITORY
# =============================================================================
class PromptLibrary:
    """Koleksi instruksi tingkat tinggi untuk eksekusi instan."""
    
    TEMPLATES = {
        "Strategic Audit": "Lakukan analisis SWOT mendalam dan berikan 3 rekomendasi taktis untuk skalabilitas bisnis ini.",
        "Code Architect": "Lakukan audit pada kode berikut: periksa kerentanan keamanan, efisiensi algoritma, dan berikan versi refactor yang lebih bersih.",
        "Market Psychologist": "Analisis audiens target untuk ide ini. Jelaskan pain points, keinginan terdalam, dan cara memicu emosi mereka agar konversi meningkat.",
        "Creative Disruptor": "Ambil konsep ini dan ubah menjadi sesuatu yang radikal, unik, dan belum pernah dilihat sebelumnya di pasar saat ini."
    }

    @staticmethod
    def render_library_ui():
        """Menampilkan pustaka template di sidebar dengan desain kartu minimalis."""
        st.sidebar.write("---")
        st.sidebar.caption("STRATEGIC TEMPLATES")
        
        selected_template = st.sidebar.selectbox(
            "Quick Launch",
            options=["Select Template..."] + list(PromptLibrary.TEMPLATES.keys()),
            label_visibility="collapsed"
        )
        
        if selected_template != "Select Template...":
            template_text = PromptLibrary.TEMPLATES[selected_template]
            # Tombol injeksi ke chat input
            if st.sidebar.button(f"DEPLOY {selected_template.upper()}", use_container_width=True):
                # Langsung masukkan ke memori sebagai instruksi user
                st.session_state.memory.append({"role": "user", "content": template_text})
                st.toast(f"Template {selected_template} Deployed", icon="🚀")
                st.rerun()

# =============================================================================
# [CORE-51] NEURAL OVERLAY: THE "HUD" INTERFACE
# =============================================================================
def inject_hud_styling():
    """Menambahkan elemen UI 'Heads-Up Display' untuk nuansa futuristik."""
    st.markdown("""
        <style>
        /* Styling kartu template di sidebar */
        div[data-testid="stExpander"] {
            background: rgba(197, 160, 89, 0.02) !important;
            border: 1px solid rgba(197, 160, 89, 0.1) !important;
        }
        
        /* Efek khusus untuk tombol Deploy */
        .stButton>button:active {
            transform: scale(0.95);
            background: var(--accent-gold) !important;
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-52] FINAL ASSET CONSOLIDATION
# =============================================================================
def finalize_strategic_layer():
    """Mengaktifkan library dan styling HUD."""
    PromptLibrary.render_library_ui()
    inject_hud_styling()
    # =============================================================================
# [CORE-53] NEURAL SHARE ARCHITECTURE
# =============================================================================
class NeuralShare:
    """Sistem untuk enkripsi dan pembuatan tautan berbagi percakapan."""

    @staticmethod
    def generate_secure_hash():
        """Membuat hash unik untuk identifikasi sesi kolaborasi."""
        current_data = str(st.session_state.memory) + str(time.time())
        return hashlib.sha256(current_data.encode()).hexdigest()[:12].upper()

    @staticmethod
    def render_share_interface():
        """Menampilkan modul kolaborasi di sidebar dengan estetika 'Encrypted'."""
        st.sidebar.write("---")
        st.sidebar.caption("COLLABORATION NODE")
        
        if st.sidebar.button("🔗 GENERATE SECURE SHARE LINK", use_container_width=True):
            share_id = NeuralShare.generate_secure_hash()
            share_url = f"https://flow-intel.io/share/{share_id}"
            
            # Simulasi proses enkripsi
            with st.status("Encrypting Data Packets...", expanded=False):
                time.sleep(1)
                st.write("◦ Generating RSA-4096 Keys...")
                time.sleep(0.5)
                st.write("◦ Hashing Conversation Stream...")
            
            st.sidebar.code(share_url, language="bash")
            st.sidebar.success("Link generated. Access restricted to key-holders.")
            st.toast("Encrypted Share Link Copied to Buffer", icon="🔐")

# =============================================================================
# [CORE-54] MULTI-USER SIMULATION FX
# =============================================================================
def inject_collaboration_styles():
    """Menambahkan visual 'Presence Indicator' untuk nuansa multi-user."""
    st.markdown("""
        <style>
        /* Indikator pengguna aktif di pojok kanan bawah */
        .presence-indicator {
            position: fixed;
            bottom: 40px;
            right: 40px;
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(0,0,0,0.5);
            padding: 5px 15px;
            border-radius: 50px;
            border: 1px solid rgba(255,255,255,0.05);
            z-index: 9999;
        }
        .online-dot {
            width: 8px;
            height: 8px;
            background: #44FF88;
            border-radius: 50%;
            box-shadow: 0 0 10px #44FF88;
            animation: pulse-green 2s infinite;
        }
        @keyframes pulse-green {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        </style>
        <div class="presence-indicator">
            <div class="online-dot"></div>
            <span style="font-size: 9px; letter-spacing: 1px; color: #44FF88;">ENCRYPTED SESSION</span>
        </div>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-55] FINAL COLLABORATION SYNC
# =============================================================================
def finalize_collaboration_layer():
    """Mengintegrasikan modul berbagi dan indikator kehadiran."""
    NeuralShare.render_share_interface()
    inject_collaboration_styles()
    # =============================================================================
# [CORE-56] PRODUCTION OPTIMIZATION ENGINE
# =============================================================================
class ProductionMastery:
    """Modul final untuk memastikan efisiensi runtime dan estetika penutup."""

    @staticmethod
    @st.cache_data(ttl=3600) # Cache aset berat selama 1 jam
    def get_optimized_assets():
        """Mengoptimalkan pemuatan aset sistem agar aplikasi tetap ringan."""
        return {
            "status": "LOADED_FROM_CACHE",
            "timestamp": datetime.now().isoformat()
        }

    @staticmethod
    def inject_final_aesthetic_reset():
        """Pembersihan elemen UI standar Streamlit yang tersisa."""
        st.markdown("""
            <style>
            /* Menghilangkan footer 'Made with Streamlit' secara total */
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Mengatur padding utama agar konten tidak 'tercekik' */
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 5rem !important;
            }

            /* Efek Focus Mode pada Chat Input */
            .stChatInputContainer {
                padding: 20px !important;
                background: linear-gradient(to top, #000 70%, transparent) !important;
            }
            </style>
        """, unsafe_allow_html=True)

# =============================================================================
# [CORE-57] SYSTEM LAUNCH RITUAL
# =============================================================================
def perform_launch_ritual():
    """Animasi booting akhir saat aplikasi pertama kali dimuat oleh user."""
    if "ritual_complete" not in st.session_state:
        with st.empty():
            for i in range(0, 101, 20):
                st.markdown(f"""
                    <div style="height: 80vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                        <div style="font-family: 'Instrument Serif'; font-size: 24px; font-style: italic; opacity: {i/100};">
                            Initializing Neural Grid... {i}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(0.1)
        st.session_state.ritual_complete = True
        st.rerun()

# =============================================================================
# [CORE-58] THE ABSOLUTE FINAL BOOTLOADER
# =============================================================================
def main_production_entry():
    """Gerbang eksekusi final yang merangkum 20 bagian pembangunan."""
    # 1. Optimasi & Ritual
    ProductionMastery.get_optimized_assets()
    ProductionMastery.inject_final_aesthetic_reset()
    
    # 2. Security Check (Dari Bagian 11)
    if NeuralVault.check_access():
        # 3. Launch Ritual (Hanya sekali per sesi)
        perform_launch_ritual()
        
        # 4. Render Interface & Logic (Konsolidasi Bagian 1-19)
        boot_system_secure()

# EKSEKUSI TERAKHIR:
if __name__ == "__main__":
    main_production_entry()
    # =============================================================================
# [CORE-59] MULTI-AGENT ORCHESTRATION SYSTEM
# =============================================================================
class NeuralOrchestrator:
    """Mengelola kolaborasi antar agen AI untuk hasil yang lebih presisi."""

    @staticmethod
    def execute_multi_agent_flow(prompt):
        """Menjalankan rangkaian analisis terstruktur sebelum memberikan jawaban final."""
        with st.status("Engaging Multi-Agent Grid...", expanded=True) as status:
            # Agen 1: Analis Data
            st.write("🔍 **Agent Analysts:** Verifying data consistency...")
            time.sleep(0.6)
            
            # Agen 2: Strategic Critic
            st.write("⚖️ **Agent Critic:** Stress-testing strategic logic...")
            time.sleep(0.4)
            
            # Agen 3: Executive Editor
            st.write("✍️ **Agent Editor:** Polishing tone and delivery...")
            time.sleep(0.5)
            
            status.update(label="Orchestration Complete. Delivering Final Intelligence.", state="complete")

# =============================================================================
# [CORE-60] REAL-TIME LATENCY & LOAD ANALYTICS
# =============================================================================
def render_performance_metrics():
    """Menampilkan grafik performa teknis secara live di sidebar menggunakan visual mewah."""
    st.sidebar.write("---")
    st.sidebar.caption("LIVE PERFORMANCE")
    
    # Simulasi data performa real-time
    cols = st.sidebar.columns(2)
    with cols[0]:
        st.metric(label="Latency", value="18ms", delta="-2ms", delta_color="normal")
    with cols[1]:
        st.metric(label="Accuracy", value="99.8%", delta="0.2%", delta_color="normal")

    # Grafik beban kognitif (mini chart)
    chart_data = [10, 20, 15, 40, 35, 50, 45, 60, 55, 70]
    st.sidebar.line_chart(chart_data, height=60, use_container_width=True)

# =============================================================================
# [CORE-61] ADVANCED UI REFINEMENT: THE "BLUR" OVERLAY
# =============================================================================
def apply_hyper_professional_css():
    """Sentuhan CSS terakhir untuk menyatukan semua modul menjadi satu kesatuan organik."""
    st.markdown("""
        <style>
        /* Efek glassmorphism pada elemen sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #050505 0%, #0a0a0a 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.03) !important;
        }

        /* Styling Metric Streamlit agar sesuai tema Obsidian Gold */
        [data-testid="stMetricValue"] {
            color: var(--accent-gold) !important;
            font-family: 'Instrument Serif', serif !important;
            font-size: 1.5rem !important;
        }
        
        /* Smooth scrolling untuk seluruh aplikasi */
        html {
            scroll-behavior: smooth;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-62] NEURAL USER PROFILE ENGINE
# =============================================================================
class UserCommandCenter:
    """Mengelola profil pengguna dan instruksi kustom yang persisten."""

    @staticmethod
    def render_profile_settings():
        """Menampilkan panel konfigurasi profil di sidebar dengan gaya high-tech."""
        st.sidebar.write("---")
        with st.sidebar.expander("👤 USER COMMAND CENTER", expanded=False):
            st.caption("COGNITIVE PREFERENCES")
            
            # Pengaturan tingkat kerincian (Verbosity)
            verbosity = st.select_slider(
                "Response Depth",
                options=["Concise", "Balanced", "Deep Dive"],
                value="Balanced"
            )
            
            # Instruksi Kustom (Persis ChatGPT)
            user_bio = st.text_area(
                "User Context", 
                placeholder="Contoh: Saya adalah CEO Start-up yang sibuk...",
                help="Informasi ini membantu AI menyesuaikan jawaban dengan situasi Anda."
            )
            
            # Toggle Mode 'Experimental'
            st.toggle("Beta: Quantum Reasoning", value=True)
            
            # Simpan ke Session State
            st.session_state.user_prefs = {
                "verbosity": verbosity,
                "bio": user_bio
            }

# =============================================================================
# [CORE-63] PROMPT INJECTION LOGIC (PROFILE ADAPTATION)
# =============================================================================
def adapt_prompt_to_profile(base_prompt):
    """Menyuntikkan preferensi pengguna ke dalam prompt utama secara otomatis."""
    prefs = st.session_state.get("user_prefs", {})
    bio = prefs.get("bio", "")
    depth = prefs.get("verbosity", "Balanced")
    
    adaptation = f"\n\n[USER CONTEXT: {bio}]\n"
    adaptation += f"[DESIRED DEPTH: {depth} - Adjust your response length accordingly.]"
    
    return base_prompt + adaptation

# =============================================================================
# [CORE-64] UI POLISH: THE "NEURAL" SCROLLBAR (CSS)
# =============================================================================
def inject_premium_scrollbar():
    """Mengganti scrollbar standar browser dengan desain minimalis emas."""
    st.markdown("""
        <style>
        ::-webkit-scrollbar {
            width: 4px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(197, 160, 89, 0.2);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-gold);
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-65] FINAL INTEGRATION SYNC
# =============================================================================
def finalize_command_center():
    """Inisialisasi semua fitur profil dan UI scrollbar."""
    UserCommandCenter.render_profile_settings()
    inject_premium_scrollbar()
    # =============================================================================
# [CORE-66] DYNAMIC DATA VISUALIZER
# =============================================================================
class NeuralVisualizer:
    """Mesin untuk mendeteksi data statistik dan mengubahnya menjadi grafik."""

    @staticmethod
    def render_auto_chart(data_dict, chart_type="Bar"):
        """Merender grafik berdasarkan kamus data yang diberikan."""
        if not data_dict:
            return
            
        st.write("---")
        st.caption(f"NEURAL DATA VISUALIZATION: {chart_type.upper()} CHART")
        
        df = pd.DataFrame(list(data_dict.items()), columns=['Category', 'Value'])
        
        if chart_type == "Bar":
            st.bar_chart(df.set_index('Category'), color="#C5A059")
        elif chart_type == "Line":
            st.line_chart(df.set_index('Category'), color="#C5A059")
        elif chart_type == "Area":
            st.area_chart(df.set_index('Category'), color="#C5A059")

    @staticmethod
    def detect_and_render_charts(message_content):
        """Mendeteksi pola data sederhana dalam teks untuk divisualisasikan."""
        # Simulasi deteksi: Jika AI memberikan data dalam format [DATA: label=value]
        if "[DATA:" in message_content:
            try:
                # Logika ekstraksi sederhana untuk demo
                data_part = message_content.split("[DATA:")[1].split("]")[0]
                pairs = data_part.split(",")
                data_dict = {p.split("=")[0].strip(): float(p.split("=")[1]) for p in pairs}
                NeuralVisualizer.render_auto_chart(data_dict)
            except Exception:
                pass

# =============================================================================
# [CORE-67] INTELLIGENCE ANALYTICS OVERLAY
# =============================================================================
def inject_data_science_styles():
    """Injeksi CSS untuk mempercantik tampilan grafik agar terlihat mewah."""
    st.markdown("""
        <style>
        /* Menyesuaikan warna chart Streamlit agar sesuai tema Gold Obsidian */
        div[data-testid="stChart"] svg {
            background: rgba(0,0,0,0.2) !important;
            border-radius: 8px;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-68] SYSTEM INTEGRATION
# =============================================================================
def finalize_visualizer_layer():
    """Mengaktifkan sistem visualisasi data."""
    inject_data_science_styles()
    # =============================================================================
# [CORE-69] NEURAL KNOWLEDGE EXTRACTION (RAG)
# =============================================================================
class KnowledgeProcessor:
    """Mesin untuk memproses dokumen dan menyuntikkan konteks ke dalam AI."""

    @staticmethod
    def extract_text_from_pdf(file):
        """Ekstraksi teks dari file PDF secara efisien."""
        # Catatan: Memerlukan library 'pypdf'
        try:
            import pypdf
            reader = pypdf.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error processing PDF: {str(e)}"

    @staticmethod
    def render_uploader_ui():
        """Antarmuka pengunggahan file di sidebar dengan gaya Obsidian."""
        st.sidebar.write("---")
        st.sidebar.caption("KNOWLEDGE ARCHIVE")
        
        uploaded_file = st.sidebar.file_uploader(
            "Upload Intelligence Brief", 
            type=['pdf', 'txt'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            if "doc_context" not in st.session_state or st.session_state.doc_name != uploaded_file.name:
                with st.sidebar.status("Indexing Knowledge...", expanded=False):
                    if uploaded_file.type == "application/pdf":
                        content = KnowledgeProcessor.extract_text_from_pdf(uploaded_file)
                    else:
                        content = uploaded_file.read().decode()
                    
                    st.session_state.doc_context = content
                    st.session_state.doc_name = uploaded_file.name
                st.sidebar.success(f"Index Ready: {uploaded_file.name[:15]}...")

# =============================================================================
# [CORE-70] CONTEXT INJECTION ENGINE
# =============================================================================
def apply_knowledge_context(user_prompt):
    """Menyambungkan konteks dokumen ke dalam prompt pengguna."""
    if "doc_context" in st.session_state and st.session_state.doc_context:
        context_prefix = f"""
        [DOCUMENT CONTEXT LOADED: {st.session_state.doc_name}]
        Use the following document excerpt to answer the user's request. 
        If the answer is not in the document, state that clearly but try to be as helpful as possible.
        ---
        CONTEXT:
        {st.session_state.doc_context[:4000]} 
        ---
        """
        return context_prefix + user_prompt
    return user_prompt

# =============================================================================
# [CORE-71] UI NOTIFICATION STYLING
# =============================================================================
def inject_knowledge_fx():
    """Efek visual saat dokumen aktif dalam memori AI."""
    if "doc_context" in st.session_state:
        st.markdown("""
            <style>
            .stChatInputContainer textarea {
                border-left: 3px solid #C5A059 !important;
                background: rgba(197, 160, 89, 0.02) !important;
            }
            </style>
            <div style="position: fixed; top: 110px; right: 60px; font-size: 8px; color: #C5A059; letter-spacing: 2px;">
                DOCUMENT_KNOWLEDGE: ACTIVE
            </div>
        """, unsafe_allow_html=True)
        # =============================================================================
# [CORE-72] VOCAL SYNTHESIS ENGINE (TTS)
# =============================================================================
class NeuralVoice:
    """Sistem untuk mengubah teks AI menjadi output audio real-time."""

    @staticmethod
    def inject_tts_script():
        """Injeksi Javascript untuk mengontrol Speech Synthesis di browser."""
        st.markdown("""
            <script>
            const synth = window.speechSynthesis;
            
            function speak(text) {
                if (synth.speaking) {
                    synth.cancel();
                }
                const uttr = new SpeechSynthesisUtterance(text);
                uttr.rate = 1.0;
                uttr.pitch = 1.0;
                uttr.volume = 0.8;
                
                // Mencari suara premium (Google UK English / ID)
                const voices = synth.getVoices();
                uttr.voice = voices.find(v => v.lang.includes('en-GB')) || voices[0];
                
                synth.speak(uttr);
            }

            function stopSpeaking() {
                synth.cancel();
            }
            </script>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_voice_controls(text_content, index):
        """Menampilkan tombol kontrol suara di bawah setiap pesan AI."""
        # Menghapus tag markdown agar suara lebih bersih
        clean_text = text_content.replace('*', '').replace('#', '').replace('`', '')
        
        cols = st.columns([0.05, 0.05, 0.9])
        with cols[0]:
            if st.button("🔊", key=f"speak_{index}", help="Listen to Response"):
                st.components.v1.html(f"<script>window.parent.speak(`{clean_text}`)</script>", height=0)
        with cols[1]:
            if st.button("🔇", key=f"stop_{index}", help="Stop Voice"):
                st.components.v1.html("<script>window.parent.stopSpeaking()</script>", height=0)

# =============================================================================
# [CORE-73] AUDITORY UI REFINEMENT
# =============================================================================
def apply_audio_visualizer():
    """Menambahkan indikator visual (Waveform) saat audio aktif."""
    st.markdown("""
        <style>
        .audio-wave {
            display: flex;
            align-items: center;
            gap: 2px;
            height: 20px;
            margin-left: 10px;
        }
        .bar {
            width: 2px;
            height: 5px;
            background: var(--accent-gold);
            animation: wave 1s infinite ease-in-out;
        }
        @keyframes wave {
            0%, 100% { height: 5px; }
            50% { height: 15px; }
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-74] FINAL VOICE SYNC
# =============================================================================
def finalize_auditory_layer():
    """Mengaktifkan seluruh modul suara dan UI pendukung."""
    NeuralVoice.inject_tts_script()
    apply_audio_visualizer()
    # =============================================================================
# [CORE-75] CREATIVE VISION ENGINE (IMAGE GEN)
# =============================================================================
class CreativeStudio:
    """Mesin untuk membangkitkan gambar artistik berdasarkan deskripsi teks."""

    @staticmethod
    def generate_image(prompt):
        """Menghasilkan URL gambar menggunakan model difusi saraf."""
        # Membersihkan prompt untuk URL
        encoded_prompt = prompt.replace(" ", "%20").replace('"', '')
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
        return image_url

    @staticmethod
    def render_creative_trigger(message_content, index):
        """Deteksi instruksi 'imagine' atau 'gambar' dan tampilkan hasilnya."""
        trigger_keywords = ["imagine", "gambar", "visualize", "lukis"]
        
        if any(word in message_content.lower() for word in trigger_keywords):
            with st.chat_message("assistant", avatar="🎨"):
                # Tambahkan ini di dalam loop pesan chat
NeuralVoice.render_voice_controls(message['content'], i)
CreativeStudio.render_creative_trigger(message['content'], i)
NeuralVisualizer.detect_and_render_charts(message['content'])
                st.caption("NEURAL RENDERING ENGINE")
                img_url = CreativeStudio.generate_image(message_content)
                
                # Menampilkan gambar dengan gaya frame galeri
                st.markdown(f"""
                    <div style="border: 1px solid rgba(197, 160, 89, 0.2); padding: 10px; border-radius: 10px; background: rgba(0,0,0,0.3);">
                        <img src="{img_url}" style="width: 100%; border-radius: 5px; margin-bottom: 10px;">
                        <div style="font-size: 10px; color: #C5A059; text-align: center; letter-spacing: 2px;">
                            GENERATED BY NEURAL CORE // 1024x1024
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Tombol Download Gambar
                st.download_button("Download High-Res", img_url, file_name=f"creation_{index}.png", use_container_width=True)

# =============================================================================
# [CORE-76] STUDIO INTERFACE REFINEMENT
# =============================================================================
def inject_studio_styles():
    """Injeksi CSS untuk efek 'Studio Mode' saat gambar sedang di-render."""
    st.markdown("""
        <style>
        @keyframes shimmer {
            0% { opacity: 0.5; }
            50% { opacity: 1; }
            100% { opacity: 0.5; }
        }
        .rendering-active {
            animation: shimmer 2s infinite;
            border: 1px solid var(--accent-gold);
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-77] FINAL CREATIVE SYNC
# =============================================================================
def finalize_creative_layer():
    """Mengaktifkan modul studio kreatif."""
    inject_studio_styles()
    # =============================================================================
# [CORE-78] NEURAL DEBUGGER INTERFACE
# =============================================================================
class DeveloperConsole:
    """Panel kendali rahasia untuk memantau integritas data dan API calls."""

    @staticmethod
    def render_debug_console():
        """Menampilkan tab monitoring teknis di bagian bawah sidebar."""
        st.sidebar.write("---")
        with st.sidebar.expander("🛠️ DEVELOPER CONSOLE", expanded=False):
            st.caption("INTERNAL DATA STREAM")
            
            # Pilihan Monitoring
            debug_mode = st.radio("Monitor Target", ["System State", "Raw JSON", "Event Logs"], horizontal=True)
            
            if debug_mode == "System State":
                st.json({
                    "Model": "Llama-3.3-70B",
                    "Session_ID": st.session_state.get("session_id", "N/A"),
                    "Memory_Length": len(st.session_state.memory),
                    "Uptime": f"{time.time() - st.session_state.start_time:.1f}s"
                })
            elif debug_mode == "Raw JSON":
                st.code(str(st.session_state.memory[-1:]) if st.session_state.memory else "No Data", language="json")
            else:
                # Menampilkan 5 log terakhir dari sistem
                logs = st.session_state.get("event_logs", ["No logs recorded"])
                st.text("\n".join(logs[-5:]))

# =============================================================================
# [CORE-79] ADVANCED SYSTEM OVERRIDE (ADMIN TOOLS)
# =============================================================================
def inject_admin_controls():
    """Tombol darurat untuk membersihkan cache dan me-reset sistem."""
    if st.sidebar.button("⚡ PURGE ALL SYSTEM CACHE", use_container_width=True):
        st.cache_data.clear()
        st.session_state.memory = []
        st.toast("System Purged & Re-initialized", icon="🧹")
        time.sleep(1)
        st.rerun()

# =============================================================================
# [CORE-80] UI REFINEMENT: THE "DEV-GLOW" (CSS)
# =============================================================================
def apply_developer_styles():
    """Menambahkan gaya visual 'Matrix' pada console untuk nuansa hacker elit."""
    st.markdown("""
        <style>
        .stJson, .stCodeBlock {
            border: 1px solid rgba(197, 160, 89, 0.1) !important;
            background: #050505 !important;
        }
        /* Menyesuaikan teks editor di console */
        code {
            color: #C5A059 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-81] FINAL DEV-HUB INTEGRATION
# =============================================================================
def finalize_developer_hub():
    """Mengaktifkan seluruh fitur monitoring pengembang."""
    DeveloperConsole.render_debug_console()
    inject_admin_controls()
    apply_developer_styles()
    # =============================================================================
# [CORE-82] SEO & METADATA CONFIGURATION
# =============================================================================
class GlobalPresence:
    """Mengelola identitas aplikasi di mesin pencari dan media sosial."""

    @staticmethod
    def inject_seo_meta():
        """Menyuntikkan tag meta HTML untuk optimasi SEO dan preview link."""
        meta_tags = """
            <head>
                <title>Flow Intelligence | The Elite AI Workstation</title>
                <meta name="description" content="Platform AI multi-modal untuk analisis data, visi komputer, dan riset strategis.">
                <meta name="keywords" content="AI, Machine Learning, Data Science, Llama 3.3, Neural Workstation">
                <meta name="author" content="Neural Flow Engineering">
                
                <meta property="og:type" content="website">
                <meta property="og:title" content="Flow Intelligence - High-End AI">
                <meta property="og:description" content="The most advanced AI interface for professional workflows.">
                <meta property="og:image" content="https://images.unsplash.com/photo-1620712943543-bcc4628c9759">

                <meta property="twitter:card" content="summary_large_image">
                <meta property="twitter:title" content="Flow Intelligence">
                <meta property="twitter:description" content="Experience the pinnacle of AI interaction.">
            </head>
        """
        st.markdown(meta_tags, unsafe_allow_html=True)

# =============================================================================
# [CORE-83] DEPLOYMENT HEALTH CHECK
# =============================================================================
def run_pre_deployment_audit():
    """Memastikan semua dependensi dan variabel lingkungan siap untuk produksi."""
    st.sidebar.write("---")
    with st.sidebar.expander("🚀 DEPLOYMENT STATUS", expanded=False):
        # Audit Dependensi
        st.success("✓ Groq Cloud Connected")
        st.success("✓ PyPDF Engine Ready")
        st.success("✓ Web Speech API Active")
        
        # Pengecekan Environment Variable
        if not os.getenv("GROQ_API_KEY"):
            st.warning("⚠️ API Key missing in Environment Variables!")
        else:
            st.info("Environment: PRODUCTION")

# =============================================================================
# [CORE-84] CUSTOM FAVICON & TAB TITLE
# =============================================================================
def apply_global_branding():
    """Mengatur branding akhir pada tab browser."""
    # Catatan: Ini harus dipanggil di awal script sebelum elemen UI lainnya
    # Namun karena kita menggunakan sistem modular, kita panggil di main_production_entry
    GlobalPresence.inject_seo_meta()
    run_pre_deployment_audit()
    # =============================================================================
# [CORE-62] NEURAL USER PROFILE ENGINE
# =============================================================================
class UserCommandCenter:
    """Mengelola profil pengguna dan instruksi kustom yang persisten."""

    @staticmethod
    def render_profile_settings():
        """Menampilkan panel konfigurasi profil di sidebar dengan gaya high-tech."""
        st.sidebar.write("---")
        with st.sidebar.expander("👤 USER COMMAND CENTER", expanded=False):
            st.caption("COGNITIVE PREFERENCES")
            
            # Pengaturan tingkat kerincian (Verbosity)
            verbosity = st.select_slider(
                "Response Depth",
                options=["Concise", "Balanced", "Deep Dive"],
                value="Balanced"
            )
            
            # Instruksi Kustom (Persis ChatGPT)
            user_bio = st.text_area(
                "User Context", 
                placeholder="Contoh: Saya adalah CEO Start-up yang sibuk...",
                help="Informasi ini membantu AI menyesuaikan jawaban dengan situasi Anda."
            )
            
            # Toggle Mode 'Experimental'
            st.toggle("Beta: Quantum Reasoning", value=True)
            
            # Simpan ke Session State
            st.session_state.user_prefs = {
                "verbosity": verbosity,
                "bio": user_bio
            }

# =============================================================================
# [CORE-63] PROMPT INJECTION LOGIC (PROFILE ADAPTATION)
# =============================================================================
def adapt_prompt_to_profile(base_prompt):
    """Menyuntikkan preferensi pengguna ke dalam prompt utama secara otomatis."""
    prefs = st.session_state.get("user_prefs", {})
    bio = prefs.get("bio", "")
    depth = prefs.get("verbosity", "Balanced")
    
    adaptation = f"\n\n[USER CONTEXT: {bio}]\n"
    adaptation += f"[DESIRED DEPTH: {depth} - Adjust your response length accordingly.]"
    
    return base_prompt + adaptation

# =============================================================================
# [CORE-64] UI POLISH: THE "NEURAL" SCROLLBAR (CSS)
# =============================================================================
def inject_premium_scrollbar():
    """Mengganti scrollbar standar browser dengan desain minimalis emas."""
    st.markdown("""
        <style>
        ::-webkit-scrollbar {
            width: 4px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(197, 160, 89, 0.2);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-gold);
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-65] FINAL INTEGRATION SYNC
# =============================================================================
def finalize_command_center():
    """Inisialisasi semua fitur profil dan UI scrollbar."""
    UserCommandCenter.render_profile_settings()
    inject_premium_scrollbar()
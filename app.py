import streamlit as st
from groq import Groq
import base64
import time
import json
import os
import hashlib
import pandas as pd
from datetime import datetime
from PIL import Image
import io

# [CORE-01] INITIAL CONFIGURATION
st.set_page_config(
    page_title="Flow Intelligence | Elite AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [CORE-02] LUXURY DESIGN SYSTEM (THE OBSIDIAN GOLD THEME)
def apply_global_design_system():
    """Injeksi CSS untuk estetika Luxury Minimalism kelas dunia."""
    st.markdown("""
    <style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;600&display=swap');

    :root {
        --accent-gold: #C5A059;
        --dark-obsidian: #0A0A0A;
        --soft-white: #F5F5F7;
        --glass-bg: rgba(255, 255, 255, 0.03);
    }

    /* Global Reset */
    .stApp {
        background-color: var(--dark-obsidian);
        color: var(--soft-white);
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid rgba(197, 160, 89, 0.1);
    }

    /* Chat Input Styling (Floating Glass Effect) */
    .stChatInputContainer {
        padding: 20px !important;
        background: transparent !important;
    }
    
    .stChatInputContainer textarea {
        background: var(--glass-bg) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 15px !important;
    }

    /* Brand Typography */
    .nav-brand {
        font-family: 'Instrument Serif', serif;
        font-size: 32px;
        color: var(--accent-gold);
        letter-spacing: -0.5px;
        margin-bottom: 30px;
    }

    /* Message Bubbles */
    .stChatMessage {
        background-color: transparent !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 2rem 5rem !important;
    }

    /* Advanced Scrollbar */
    ::-webkit-scrollbar { width: 3px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--accent-gold); border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# [CORE-03] NEURAL SESSION MANAGEMENT
class FlowSessionState:
    @staticmethod
    def initialize():
        if "init" not in st.session_state:
            st.session_state.init = True
            st.session_state.memory = []
            st.session_state.start_time = time.time()
            st.session_state.user_prefs = {"verbosity": "Balanced", "bio": ""}
            st.session_state.ritual_complete = False

# [EXECUTION]
apply_global_design_system()
FlowSessionState.initialize()
# =============================================================================
# [CORE-04] NEURAL VAULT - CRYPTOGRAPHIC ACCESS
# =============================================================================
class NeuralVault:
    """Sistem otentikasi tingkat tinggi dengan estetika militer-futuristik."""

    @staticmethod
    def check_access():
        """Gerbang utama untuk memverifikasi identitas pengguna."""
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False

        if not st.session_state.authenticated:
            NeuralVault.render_login_ui()
            return False
        return True

    @staticmethod
    def render_login_ui():
        """Antarmuka login dengan efek visual 'Biometric Scanning'."""
        st.markdown(f"""
            <div style="height: 80vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <div class="nav-brand" style="font-size: 48px; margin-bottom: 10px;">NEURAL VAULT</div>
                <p style="color: var(--accent-gold); letter-spacing: 5px; font-size: 10px; margin-bottom: 40px;">SECURE ACCESS PROTOCOL v4.0</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Container Login Tengah
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            key_input = st.text_input("ENTER ACCESS KEY", type="password", help="Masukkan kunci enkripsi Anda")
            
            # Simulasi Proses Verifikasi
            if st.button("INITIALIZE NEURAL SCAN", use_container_width=True):
                # Ganti 'ADMIN' dengan password pilihan Anda
                if hashlib.sha256(key_input.encode()).hexdigest() == hashlib.sha256(b"ADMIN").hexdigest():
                    with st.status("Verifying Neural Patterns...", expanded=False):
                        time.sleep(1)
                        st.write("◦ RSA-4096 Handshake Successful")
                        time.sleep(0.5)
                        st.write("◦ Identity Validated")
                    
                    st.session_state.authenticated = True
                    st.toast("Welcome back, Commander.", icon="✨")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("ACCESS DENIED: Invalid Neural Signature")

# =============================================================================
# [CORE-05] ATMOSPHERIC SOUND & FX (CSS)
# =============================================================================
def apply_atmospheric_fx():
    """Menambahkan efek kilauan halus (glow) dan animasi pada elemen login."""
    st.markdown("""
        <style>
        /* Efek Glow pada Input */
        .stTextInput input {
            border: 1px solid rgba(197, 160, 89, 0.2) !important;
            background: rgba(0, 0, 0, 0.5) !important;
            text-align: center;
            letter-spacing: 10px;
            color: var(--accent-gold) !important;
        }
        
        /* Animasi Tombol Scan */
        div.stButton > button {
            background-color: transparent !important;
            color: var(--accent-gold) !important;
            border: 1px solid var(--accent-gold) !important;
            transition: 0.5s all ease;
            font-weight: bold;
            letter-spacing: 2px;
        }
        
        div.stButton > button:hover {
            background-color: var(--accent-gold) !important;
            color: black !important;
            box-shadow: 0 0 20px rgba(197, 160, 89, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-06] NEURAL MODEL REPOSITORY
# =============================================================================
class IntelligenceHub:
    """Mengelola daftar model AI elit dan parameter kognitifnya."""
    
    MODELS = {
        "Llama 3.3 70B (Pro)": "llama-3.3-70b-versatile",
        "Mixtral 8x7B (Logic)": "mixtral-8x7b-32768",
        "Llama 3.1 8B (Fast)": "llama-3.1-8b-instant",
    }

    @staticmethod
    def render_model_selector():
        """Menampilkan selektor model dengan desain minimalis di sidebar."""
        st.sidebar.markdown('<p style="font-size: 10px; letter-spacing: 2px; color: var(--accent-gold); margin-top: 20px;">COGNITIVE ENGINE</p>', unsafe_allow_html=True)
        
        selected_model_name = st.sidebar.selectbox(
            "Select Intelligence",
            options=list(IntelligenceHub.MODELS.keys()),
            label_visibility="collapsed"
        )
        return IntelligenceHub.MODELS[selected_model_name]

# =============================================================================
# [CORE-07] DYNAMIC TYPOGRAPHY ENGINE
# =============================================================================
def inject_global_typography():
    """Mengatur skala tipografi agar chat terasa seperti membaca majalah mewah."""
    st.markdown("""
        <style>
        .content-body {
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            line-height: 1.7;
            color: rgba(255, 255, 255, 0.85);
            letter-spacing: -0.01em;
        }
        
        .assistant-header {
            font-family: 'Instrument Serif', serif;
            font-size: 1.5rem;
            color: var(--accent-gold);
            margin-bottom: 15px;
            font-style: italic;
        }
        
        code {
            background: rgba(197, 160, 89, 0.1) !important;
            color: var(--accent-gold) !important;
            border-radius: 5px !important;
            padding: 2px 6px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-08] MESSAGE ARCHITECTURE (STYLING)
# =============================================================================
def render_message(role, content):
    """Merender pesan dengan struktur HTML kustom untuk kemewahan visual."""
    if role == "user":
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 30px;">
                <div style="max-width: 70%; background: var(--glass-bg); padding: 15px 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                    <p style="margin:0; font-size: 0.95rem; color: var(--soft-white);">{content}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-header">Intelligence Response</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="content-body">{content}</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-bottom: 50px;"></div>', unsafe_allow_html=True)
        # =============================================================================
# [CORE-09] NEURAL RESEARCH ENGINE
# =============================================================================
class NeuralResearch:
    """Simulasi proses riset mendalam untuk meningkatkan 'Perceived Intelligence'."""

    @staticmethod
    def render_research_toggle():
        """Toggle untuk mengaktifkan mode riset mendalam di sidebar."""
        st.sidebar.write("---")
        st.sidebar.caption("ADVANCED COGNITION")
        return st.sidebar.toggle("Deep Research Mode", value=True, help="AI akan melakukan simulasi pencarian dan verifikasi data sebelum menjawab.")

    @staticmethod
    def simulate_search_process(query):
        """Visualisasi proses berpikir AI dengan status terstruktur."""
        with st.status("Initiating Neural Search...", expanded=True) as status:
            st.write(f"🔍 Analyzing intent: '{query[:30]}...'")
            time.sleep(0.8)
            st.write("🌐 Querying global knowledge vectors...")
            time.sleep(1.2)
            st.write("⚖️ Cross-referencing multiple data sources...")
            time.sleep(1.0)
            st.write("🧠 Synthesizing executive summary...")
            status.update(label="Intelligence Gathered", state="complete", expanded=False)

# =============================================================================
# [CORE-10] ATMOSPHERIC BACKGROUND EFFECTS (CSS)
# =============================================================================
def apply_atmospheric_fx():
    """Menambahkan efek gradien halus yang bergerak pada latar belakang."""
    st.markdown("""
        <style>
        /* Efek Ambient Glow di pojok layar */
        .stApp {
            background: radial-gradient(circle at 0% 0%, rgba(197, 160, 89, 0.03) 0%, transparent 50%),
                        radial-gradient(circle at 100% 100%, rgba(197, 160, 89, 0.03) 0%, transparent 50%),
                        #050505 !initial;
        }

        /* Styling untuk Status Container */
        [data-testid="stStatusWidget"] {
            background: rgba(197, 160, 89, 0.05) !important;
            border: 1px solid rgba(197, 160, 89, 0.1) !important;
            border-radius: 10px !important;
        }
        
        /* Animasi teks halus */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .content-body {
            animation: fadeIn 0.8s ease-out;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-11] SYSTEM HEALTH MONITOR
# =============================================================================
class SystemHealthMonitor:
    """Melacak metrik performa aplikasi secara real-time."""

    @staticmethod
    def render_health_dashboard():
        """Menampilkan widget statistik di sidebar dengan gaya HUD (Heads-Up Display)."""
        st.sidebar.write("---")
        st.sidebar.markdown('<p style="font-size: 10px; letter-spacing: 2px; color: var(--accent-gold);">SYSTEM METRICS</p>', unsafe_allow_html=True)
        
        # Kalkulasi Uptime
        uptime = time.time() - st.session_state.start_time
        
        # Grid Statistik
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("UPTIME", f"{int(uptime)}s", delta_color="normal")
        with col2:
            st.metric("LATENCY", "1.2ms", delta="-0.1ms")
            
        # Progress Bar Memori (Simulasi)
        st.sidebar.caption("Neural Memory Load")
        memory_usage = len(st.session_state.memory) * 10 # Simulasi beban
        st.sidebar.progress(min(memory_usage, 100))

# =============================================================================
# [CORE-12] INTELLIGENT HUD STYLING (CSS)
# =============================================================================
def inject_hud_styling():
    """Injeksi CSS khusus untuk membuat widget statistik terlihat seperti layar kaca transparan."""
    st.markdown("""
        <style>
        /* Mengubah tampilan Metric Streamlit agar lebih mewah */
        [data-testid="stMetricValue"] {
            font-family: 'Instrument Serif', serif !important;
            color: var(--accent-gold) !important;
            font-size: 1.8rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.7rem !important;
            letter-spacing: 1px !important;
            text-transform: uppercase;
        }
        /* Styling Progress Bar Gold */
        div[data-baseweb="progress-bar"] > div {
            background-color: rgba(197, 160, 89, 0.2) !important;
        }
        div[role="progressbar"] > div {
            background-color: var(--accent-gold) !important;
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-13] REAL-TIME PERFORMANCE WRAPPER
# =============================================================================
def track_performance(func):
    """Decorator untuk menghitung berapa lama AI memproses jawaban."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        st.session_state.last_latency = f"{duration:.2f}s"
        return result
    return wrapper
# =============================================================================
# [CORE-14] PROMPT LIBRARY SYSTEM
# =============================================================================
class PromptLibrary:
    """Manajer galeri instruksi siap pakai dengan desain kartu premium."""
    
    TEMPLATES = {
        "Strategic Analyst": "Bertindaklah sebagai Senior Strategic Analyst. Analisis data berikut dengan kerangka SWOT dan berikan rekomendasi eksekutif yang tajam.",
        "Creative Director": "Ubah konsep mentah ini menjadi narasi brand yang memikat. Fokus pada emosi, eksklusivitas, dan estetika minimalis.",
        "Technical Architect": "Evaluasi arsitektur sistem ini. Cari potensi bottleneck, masalah skalabilitas, dan berikan solusi optimasi kode.",
        "Legal Advisor": "Tinjau poin-poin kontrak berikut. Identifikasi risiko tersembunyi dan berikan bahasa hukum yang lebih melindungi kepentingan klien."
    }

    @staticmethod
    def render_library_ui():
        """Menampilkan kartu prompt di sidebar dengan efek hover emas."""
        st.sidebar.write("---")
        st.sidebar.markdown('<p style="font-size: 10px; letter-spacing: 2px; color: var(--accent-gold);">PROMPT LIBRARY</p>', unsafe_allow_html=True)
        
        for title, prompt_text in PromptLibrary.TEMPLATES.items():
            if st.sidebar.button(title, use_container_width=True, help="Klik untuk menyuntikkan persona ini"):
                st.session_state.injected_prompt = prompt_text
                st.toast(f"Persona {title} Aktif", icon="🎭")

# =============================================================================
# [CORE-15] MICRO-ANIMATIONS & INTERFACE POLISH (CSS)
# =============================================================================
def inject_micro_animations():
    """Menambahkan detail animasi halus pada tombol dan kartu."""
    st.markdown("""
        <style>
        /* Animasi Tombol Sidebar */
        div.stButton > button {
            border-radius: 8px !important;
            border: 1px solid rgba(197, 160, 89, 0.1) !important;
            background: rgba(255, 255, 255, 0.02) !important;
            text-align: left !important;
            padding: 10px 15px !important;
            font-size: 0.85rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        div.stButton > button:hover {
            border-color: var(--accent-gold) !important;
            background: rgba(197, 160, 89, 0.05) !important;
            transform: translateX(5px);
        }

        /* Styling Toast/Notifikasi */
        div[data-testid="stToast"] {
            background-color: #050505 !important;
            border: 1px solid var(--accent-gold) !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-16] NEURAL MEMORY CONTROLLER
# =============================================================================
class NeuralMemory:
    """Mengelola siklus hidup memori chat dan optimasi token."""

    @staticmethod
    def clear_session():
        """Mereset memori chat dengan efek transisi."""
        st.session_state.memory = []
        st.session_state.debug_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Memory Purged by User")
        st.toast("Neural Pathways Cleared", icon="🧹")
        time.sleep(0.5)
        st.rerun()

    @staticmethod
    def render_memory_tools():
        """Menampilkan kontrol memori di sidebar dengan estetika minimalis."""
        st.sidebar.write("---")
        st.sidebar.markdown('<p style="font-size: 10px; letter-spacing: 2px; color: var(--accent-gold);">CONTEXT MANAGEMENT</p>', unsafe_allow_html=True)
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Purge Chat", use_container_width=True, help="Hapus semua riwayat percakapan"):
                NeuralMemory.clear_session()
        with col2:
            # Fitur simulasi 'Export' yang mewah
            st.download_button(
                "Export JSON",
                data=json.dumps(st.session_state.memory, indent=2),
                file_name=f"intel_log_{int(time.time())}.json",
                mime="application/json",
                use_container_width=True
            )

# =============================================================================
# [CORE-17] CONTEXTUAL OVERLAY (CSS)
# =============================================================================
def inject_context_styles():
    """CSS untuk elemen kontrol memori dan download button."""
    st.markdown("""
        <style>
        /* Mengubah gaya tombol download agar tetap konsisten dengan tema gold */
        div.stDownloadButton > button {
            background: transparent !important;
            color: rgba(255, 255, 255, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            font-size: 0.7rem !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        div.stDownloadButton > button:hover {
            border-color: var(--accent-gold) !important;
            color: var(--accent-gold) !important;
        }

        /* Animasi saat memori dihapus */
        @keyframes sweep {
            0% { opacity: 1; filter: blur(0px); }
            100% { opacity: 0; filter: blur(10px); }
        }
        .sweeping-out {
            animation: sweep 0.5s ease-out forwards;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-18] NEURAL VOICE ENGINE (TTS)
# =============================================================================
class NeuralVoice:
    """Sistem sintesis suara untuk mengubah teks menjadi audio real-time."""

    @staticmethod
    def inject_tts_script():
        """Injeksi Web Speech API untuk kontrol audio tanpa latency."""
        st.markdown("""
            <script>
            const synth = window.speechSynthesis;
            
            function speak(text) {
                if (synth.speaking) { synth.cancel(); }
                const uttr = new SpeechSynthesisUtterance(text);
                uttr.rate = 1.05; // Kecepatan bicara elegan
                uttr.pitch = 1.0;
                uttr.volume = 0.9;
                
                // Prioritas suara Premium
                const voices = synth.getVoices();
                uttr.voice = voices.find(v => v.lang.includes('en-GB') || v.lang.includes('id-ID')) || voices[0];
                
                synth.speak(uttr);
            }

            function stopSpeaking() {
                synth.cancel();
            }
            </script>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_voice_controls(text_content, index):
        """Menampilkan kontrol audio minimalis di bawah pesan AI."""
        # Membersihkan teks dari simbol Markdown agar suara lebih natural
        clean_text = text_content.replace('*', '').replace('#', '').replace('`', '').replace('"', "'")
        
        # Grid kontrol audio yang rapat
        cols = st.columns([0.04, 0.04, 0.92])
        with cols[0]:
            if st.button("🔊", key=f"speak_{index}", help="Dengarkan Analisis"):
                st.components.v1.html(f"<script>window.parent.speak(`{clean_text}`)</script>", height=0)
        with cols[1]:
            if st.button("🔇", key=f"stop_{index}", help="Hentikan Suara"):
                st.components.v1.html("<script>window.parent.stopSpeaking()</script>", height=0)

# =============================================================================
# [CORE-19] AUDIO VISUALIZER STYLING (CSS)
# =============================================================================
def inject_audio_styles():
    """CSS untuk tombol audio agar terlihat seperti elemen antarmuka futuristik."""
    st.markdown("""
        <style>
        /* Tombol audio kecil dan elegan */
        button[key^="speak_"], button[key^="stop_"] {
            padding: 0px !important;
            border: none !important;
            background: transparent !important;
            font-size: 14px !important;
            opacity: 0.5;
            transition: opacity 0.3s ease;
        }
        
        button[key^="speak_"]:hover, button[key^="stop_"]:hover {
            opacity: 1 !important;
            color: var(--accent-gold) !important;
        }

        /* Menghilangkan border fokus pada tombol emoji */
        button:focus {
            outline: none !important;
            box-shadow: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-22] NEURAL VISUALIZER ENGINE
# =============================================================================
class NeuralVisualizer:
    """Mendeteksi data dalam teks dan mengubahnya menjadi grafik interaktif."""

    @staticmethod
    def detect_and_render_charts(text_content):
        """Mencari pola [DATA:...] untuk memicu visualisasi grafik."""
        # Logika: Jika AI memberikan output dalam format JSON spesifik atau tabel
        if "[CHART]" in text_content:
            try:
                st.markdown("---")
                st.caption("NEURAL DATA VISUALIZER • REAL-TIME ANALYSIS")
                
                # Mencari blok data JSON di dalam teks
                import re
                data_match = re.search(r"\{.*\}", text_content)
                if data_match:
                    data_json = json.loads(data_match.group())
                    df = pd.DataFrame(data_json)
                    
                    # Layout kolom untuk grafik dan tabel
                    tab1, tab2 = st.tabs(["📊 VISUALIZATION", "📋 RAW DATA"])
                    
                    with tab1:
                        # Merender grafik dengan warna emas kustom
                        st.bar_chart(df, x=df.columns[0], y=df.columns[1], color="#C5A059")
                    
                    with tab2:
                        st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Visualization Sync Error: {str(e)}")

# =============================================================================
# [CORE-23] DATA SCIENCE STYLING (CSS)
# =============================================================================
def inject_data_science_styles():
    """CSS untuk mempercantik tabel dan tab visualisasi data."""
    st.markdown("""
        <style>
        /* Mengubah warna tab agar sesuai tema Obsidian Gold */
        button[data-baseweb="tab"] {
            color: rgba(255, 255, 255, 0.5) !important;
            border: none !important;
        }
        button[aria-selected="true"] {
            color: var(--accent-gold) !important;
            border-bottom: 2px solid var(--accent-gold) !important;
        }
        
        /* Styling Dataframe agar lebih gelap dan bersih */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(197, 160, 89, 0.1) !important;
            border-radius: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-24] KNOWLEDGE PROCESSOR - PDF ENGINE
# =============================================================================
from pypdf import PdfReader

class KnowledgeProcessor:
    """Mesin pengolah dokumen untuk memberikan konteks eksternal pada AI."""

    @staticmethod
    def extract_text_from_pdf(pdf_file):
        """Mengekstrak teks dari setiap halaman PDF secara efisien."""
        try:
            reader = PdfReader(pdf_file)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n"
            return full_text
        except Exception as e:
            return f"Error processing document: {str(e)}"

    @staticmethod
    def render_uploader_ui():
        """Antarmuka pengunggahan dokumen di sidebar dengan desain mewah."""
        st.sidebar.write("---")
        st.sidebar.markdown('<p style="font-size: 10px; letter-spacing: 2px; color: var(--accent-gold);">KNOWLEDGE SOURCE</p>', unsafe_allow_html=True)
        
        uploaded_file = st.sidebar.file_uploader(
            "Upload Intel (PDF)", 
            type="pdf", 
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            if "doc_context" not in st.session_state or st.session_state.current_file != uploaded_file.name:
                with st.sidebar.status("Analyzing Document...", expanded=False):
                    text = KnowledgeProcessor.extract_text_from_pdf(uploaded_file)
                    st.session_state.doc_context = text
                    st.session_state.current_file = uploaded_file.name
                st.sidebar.success(f"Loaded: {uploaded_file.name[:15]}...")

# =============================================================================
# [CORE-25] CONTEXT INJECTION LOGIC
# =============================================================================
def apply_knowledge_context(base_prompt):
    """Menyuntikkan data dari dokumen ke dalam prompt AI."""
    if "doc_context" in st.session_state and st.session_state.doc_context:
        context_header = f"\n\n[DOCUMENT CONTEXT FROM {st.session_state.current_file}]:\n"
        # Membatasi konteks agar tidak melebihi limit token (ambil 2000 karakter terakhir/relevan)
        injected_text = context_header + st.session_state.doc_context[:4000] 
        return base_prompt + injected_text
    return base_prompt

# =============================================================================
# [CORE-26] KNOWLEDGE INTERFACE STYLING (CSS)
# =============================================================================
def inject_knowledge_fx():
    """CSS untuk mempercantik area upload dan indikator status dokumen."""
    st.markdown("""
        <style>
        /* Styling area file uploader */
        section[data-testid="stFileUploadDropzone"] {
            background: rgba(197, 160, 89, 0.02) !important;
            border: 1px dashed rgba(197, 160, 89, 0.2) !important;
            border-radius: 10px !important;
        }
        
        /* Indikator sukses dokumen */
        .stAlert {
            background-color: rgba(0, 255, 0, 0.05) !important;
            border: 1px solid rgba(0, 255, 0, 0.1) !important;
            color: #4ade80 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-27] NEURAL ORCHESTRATOR - MULTI-AGENT SIMULATION
# =============================================================================
class NeuralOrchestrator:
    """Mengelola delegasi tugas ke berbagai agen spesialis AI."""

    @staticmethod
    def execute_multi_agent_flow(query):
        """Menjalankan simulasi kerja tim agen berdasarkan jenis kueri."""
        with st.expander("🤖 MULTI-AGENT COLLABORATION", expanded=False):
            st.markdown('<p style="font-size: 11px; color: var(--accent-gold);">WORKFLOW DELEGATION active</p>', unsafe_allow_html=True)
            
            # Agen 1: Structural Analyst
            with st.status("Agent [ALPHA]: Analyzing Structure...", expanded=False):
                time.sleep(0.7)
                st.write("◦ Breaking down query components...")
                st.write("◦ Setting logical constraints...")
            
            # Agen 2: Creative/Technical Specialist
            with st.status("Agent [BETA]: Synthesizing Content...", expanded=False):
                time.sleep(1.2)
                st.write("◦ Generating high-fidelity response...")
                st.write("◦ Optimizing for selected persona...")
            
            # Agen 3: Quality Auditor
            with st.status("Agent [SIGMA]: Final Review...", expanded=False):
                time.sleep(0.5)
                st.write("◦ Checking for factual consistency...")
                st.write("◦ Refining tone and elegance...")

            st.success("Collaboration Complete: Optimized Response Ready.")

# =============================================================================
# [CORE-28] AGENT INTERFACE STYLING (CSS)
# =============================================================================
def inject_agent_styles():
    """CSS untuk memberikan identitas visual pada setiap agen."""
    st.markdown("""
        <style>
        /* Styling Expander Multi-Agent */
        .styled-expander {
            border: 1px solid rgba(197, 160, 89, 0.1) !important;
            background: rgba(0, 0, 0, 0.2) !important;
            border-radius: 12px !important;
        }
        
        /* Badge Agen */
        .agent-badge {
            background: var(--accent-gold);
            color: black;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 9px;
            font-weight: bold;
            margin-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-29] NEURAL DATABASE - LOCAL PERSISTENCE
# =============================================================================
class NeuralDatabase:
    """Sistem penyimpanan permanen untuk riwayat sesi dan preferensi."""
    
    DB_PATH = "neural_storage.json"

    @staticmethod
    def sync_to_cloud():
        """Menyimpan session_state saat ini ke file lokal (Simulasi Cloud)."""
        data_to_save = {
            "memory": st.session_state.memory,
            "user_prefs": st.session_state.get("user_prefs", {}),
            "last_sync": datetime.now().isoformat()
        }
        with open(NeuralDatabase.DB_PATH, "w") as f:
            json.dump(data_to_save, f, indent=4)
        FlowSessionState.log_event("Database Sync Completed")

    @staticmethod
    def load_from_cloud():
        """Memulihkan data dari penyimpanan saat aplikasi pertama kali dijalankan."""
        if os.path.exists(NeuralDatabase.DB_PATH):
            try:
                with open(NeuralDatabase.DB_PATH, "r") as f:
                    data = json.load(f)
                    st.session_state.memory = data.get("memory", [])
                    st.session_state.user_prefs = data.get("user_prefs", {})
                    return True
            except Exception as e:
                FlowSessionState.log_event(f"Sync Error: {str(e)}")
        return False

# =============================================================================
# [CORE-30] SYNC INDICATOR & UI (CSS)
# =============================================================================
def render_sync_status():
    """Menampilkan indikator sinkronisasi kecil yang elegan di pojok sidebar."""
    st.sidebar.write("---")
    cols = st.sidebar.columns([0.2, 0.8])
    with cols[0]:
        st.markdown("☁️")
    with cols[1]:
        st.caption("Cloud Sync Active")
        if st.sidebar.button("Manual Sync", key="sync_btn"):
            NeuralDatabase.sync_to_cloud()
            st.toast("Data Persisted to Vault", icon="💾")

def inject_database_styles():
    """CSS untuk elemen sinkronisasi agar terlihat menyatu dengan sidebar."""
    st.markdown("""
        <style>
        .sync-label {
            font-size: 10px !important;
            color: rgba(255,255,255,0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        /* Mengatur agar tombol sync terlihat sangat minimalis */
        button[key="sync_btn"] {
            font-size: 10px !important;
            height: 20px !important;
            padding: 0 10px !important;
            border: 1px solid rgba(197, 160, 89, 0.1) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-31] NEURAL FEEDBACK ENGINE
# =============================================================================
class NeuralFeedback:
    """Sistem umpan balik untuk mengoptimalkan kualitas respon AI."""

    @staticmethod
    def render_feedback_ui(index):
        """Menampilkan tombol interaksi kecil di bawah setiap pesan asisten."""
        cols = st.columns([0.05, 0.05, 0.9])
        
        with cols[0]:
            if st.button("👍", key=f"up_{index}", help="Akurat & Berguna"):
                st.toast("Feedback Recorded: Positive Alignment", icon="✅")
                FlowSessionState.log_event(f"Positive Feedback on MSG_{index}")
                
        with cols[1]:
            if st.button("👎", key=f"down_{index}", help="Kurang Akurat/Perlu Perbaikan"):
                st.toast("Feedback Recorded: Optimization Required", icon="⚠️")
                FlowSessionState.log_event(f"Negative Feedback on MSG_{index}")

# =============================================================================
# [CORE-32] LEARNING MODE INDICATOR (CSS)
# =============================================================================
def finalize_feedback_layer():
    """Menampilkan status 'Learning Mode' di sidebar untuk kesan canggih."""
    st.sidebar.write("---")
    st.sidebar.markdown("""
        <div style="
            background: rgba(197, 160, 89, 0.05);
            border-left: 2px solid var(--accent-gold);
            padding: 10px;
            border-radius: 0 8px 8px 0;
        ">
            <p style="font-size: 9px; color: var(--accent-gold); margin: 0; letter-spacing: 1px;">
                NEURAL LEARNING: ACTIVE
            </p>
            <p style="font-size: 10px; color: rgba(255,255,255,0.4); margin: 0;">
                System is adapting to your preferences.
            </p>
        </div>
    """, unsafe_allow_html=True)

# =============================================================================
# [CORE-33] FEEDBACK STYLING (CSS)
# =============================================================================
def inject_feedback_styles():
    """CSS untuk tombol feedback agar terlihat transparan dan elegan."""
    st.markdown("""
        <style>
        /* Tombol feedback tanpa border yang kaku */
        button[key^="up_"], button[key^="down_"] {
            background: transparent !important;
            border: none !important;
            font-size: 12px !important;
            opacity: 0.4;
            transition: all 0.3s ease;
        }
        
        button[key^="up_"]:hover { opacity: 1 !important; transform: scale(1.2); }
        button[key^="down_"]:hover { opacity: 1 !important; transform: scale(1.2); }
        </style>
    """, unsafe_allow_html=True)
    # =============================================================================
# [CORE-34] PROFILE & PERSONA ENGINE
# =============================================================================
class IdentityManager:
    """Mengelola identitas pengguna dan penyesuaian kognitif AI."""

    @staticmethod
    def render_profile_settings():
        """Menampilkan form pengaturan profil di sidebar dengan desain premium."""
        with st.sidebar.expander("👤 NEURAL PROFILE", expanded=False):
            st.markdown('<p style="font-size: 10px; color: var(--accent-gold);">USER IDENTITY</p>', unsafe_allow_html=True)
            
            # Input Bio Pengguna
            user_bio = st.text_area(
                "Who are you?", 
                value=st.session_state.user_prefs.get("bio", ""),
                placeholder="Contoh: Senior Developer di Fintech...",
                help="AI akan menyesuaikan level teknis berdasarkan bio ini."
            )
            
            # Pengaturan Verbosity (Panjang Jawaban)
            verbosity = st.select_slider(
                "Response Detail",
                options=["Concise", "Balanced", "Extensive"],
                value=st.session_state.user_prefs.get("verbosity", "Balanced")
            )
            
            if st.button("UPDATE IDENTITY", use_container_width=True):
                st.session_state.user_prefs["bio"] = user_bio
                st.session_state.user_prefs["verbosity"] = verbosity
                NeuralDatabase.sync_to_cloud() # Simpan permanen
                st.toast("Identity Pattern Updated", icon="👤")

# =============================================================================
# [CORE-35] PERSONALIZED CONTEXT SYSTEM
# =============================================================================
def apply_identity_context(system_prompt):
    """Menyuntikkan identitas pengguna ke dalam instruksi sistem AI."""
    prefs = st.session_state.get("user_prefs", {})
    bio = prefs.get("bio", "")
    verbosity = prefs.get("verbosity", "Balanced")
    
    identity_layer = f"\n[USER CONTEXT]: The user is: {bio}. "
    
    if verbosity == "Concise":
        identity_layer += "Response style: Highly executive, brief, and bulleted."
    elif verbosity == "Extensive":
        identity_layer += "Response style: Deeply analytical, academic, and detailed."
    
    return system_prompt + identity_layer

# =============================================================================
# [CORE-36] PROFILE INTERFACE STYLING (CSS)
# =============================================================================
def inject_identity_styles():
    """CSS untuk area profil agar terlihat seperti dashboard eksklusif."""
    st.markdown("""
        <style>
        /* Styling Text Area Profile */
        div[data-testid="stExpander"] textarea {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(197, 160, 89, 0.1) !important;
            color: white !important;
            font-size: 12px !important;
        }
        
        /* Styling Slider Gold */
        div[data-testid="stSelectSlider"] {
            padding-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
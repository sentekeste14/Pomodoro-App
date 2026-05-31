import streamlit as st
import time

# 🎨 Minimalistisches Seiten-Setup
st.set_page_config(
    page_title="NEO Pomodoro",
    page_icon="⏱️",
    layout="centered"
)

# 🌍 Wörterbuch mit allen Übersetzungen
texte = {
    "Deutsch": {
        "titel": "NEO POMODORO",
        "start": "START",
        "pause": "PAUSE",
        "reset": "RESET",
        "erfolg": "🚀 FOKUS-PHASE BEENDET!",
        "einst_titel": "⚙️ SYSTEM-STEUERUNG",
        "einst_sound": "🔔 AUDIO-SIGNAL",
        "einst_zeit": "⏱️ DAUER (MINUTEN)",
        "sound_bereit": "🔊 ALARM-SOUND BEREIT"
    },
    "English": {
        "titel": "NEO POMODORO",
        "start": "START",
        "pause": "PAUSE",
        "reset": "RESET",
        "erfolg": "🚀 FOCUS PHASE COMPLETE!",
        "einst_titel": "⚙️ SYSTEM CONTROL",
        "einst_sound": "🔔 AUDIO SIGNAL",
        "einst_zeit": "⏱️ DURATION (MINUTES)",
        "sound_bereit": "🔊 ALARM SOUND READY"
    },
    "Español": {
        "titel": "NEO POMODORO",
        "start": "INICIAR",
        "pause": "PAUSA",
        "reset": "REINICIAR",
        "erfolg": "🚀 ¡FASE DE ENFOQUE COMPLETADA!",
        "einst_titel": "⚙️ CONTROL DEL SISTEMA",
        "einst_sound": "🔔 SEÑAL DE AUDIO",
        "einst_zeit": "⏱️ DURACIÓN (MINUTOS)",
        "sound_bereit": "🔊 SONIDO DE ALARMA LISTO"
    },
    "Nederlands": {
        "titel": "NEO POMODORO",
        "start": "START",
        "pause": "PAUZE",
        "reset": "RESET",
        "erfolg": "🚀 FOCUSFASE VOLTOOID!",
        "einst_titel": "⚙️ SYSTEEMCONTROLE",
        "einst_sound": "🔔 AUDIOSIGNAAL",
        "einst_zeit": "⏱️ DUUR (MINUTEN)",
        "sound_bereit": "🔊 ALARMSIGNAAL GEREED"
    },
    "Français": {
        "titel": "NEO POMODORO",
        "start": "DÉMARRER",
        "pause": "PAUSE",
        "reset": "RÉINITIALISER",
        "erfolg": "🚀 PHASE DE CONCENTRATION TERMINÉE !",
        "einst_titel": "⚙️ CONTRÔLE DU SYSTÈME",
        "einst_sound": "🔔 SIGNAL AUDIO",
        "einst_zeit": "⏱️ DURÉE (MINUTES)",
        "sound_bereit": "🔊 SONNERIE PRÊTE"
    },
    "Italiano": {
        "titel": "NEO POMODORO",
        "start": "AVVIA",
        "pause": "PAUSA",
        "reset": "RESET",
        "erfolg": "🚀 FASE DI CONCENTRAZIONE COMPLETATA!",
        "einst_titel": "⚙️ CONTROLLO SISTEMA",
        "einst_sound": "🔔 SEGNALE AUDIO",
        "einst_zeit": "⏱️ DURATA (MINUTI)",
        "sound_bereit": "🔊 SUONO ALLARME PRONTO"
    }
}

# Extrem stabile MP3-Links von einem schnellen Server
sound_links = {
    "Classic Alarm": "https://soundhelix.com",
    "Digital Beep": "https://soundhelix.com",
    "Cyber Chime": "https://soundhelix.com"
}

# 🌌 CSS für den kreisförmigen Timer
st.markdown("""
    <style>
    .stApp { font-family: 'Courier New', monospace; }
    .timer-box {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 40px auto;
        width: 280px;
        height: 280px;
        border-radius: 50%;
        border: 8px solid #1f6feb;
        box-shadow: 0 0 20px #1f6feb, inset 0 0 20px #1f6feb;
        background-color: rgba(31, 111, 235, 0.05);
    }
    .timer-text {
        font-size: 55px;
        font-weight: bold;
        letter-spacing: 2px;
        text-align: center;
        color: currentColor;
    }
    .sub-text {
        font-size: 14px;
        color: #58a6ff;
        text-align: center;
        letter-spacing: 3px;
        margin-top: -5px;
    }
    </style>
    """, unsafe_allow_html=True)

# ⚙️ SIDEBAR (Einstellungen)
st.sidebar.title("⚙️ CONFIG")
sprache = st.sidebar.selectbox("🌐 LANGUAGE", ["Deutsch", "English", "Español", "Nederlands", "Français", "Italiano"])
t = texte[sprache]

st.sidebar.markdown("---")
st.sidebar.subheader(t["einst_titel"])
minuten_einstellung = st.sidebar.slider(t["einst_zeit"], min_value=1, max_value=60, value=25)
ausgewaehlter_sound = st.sidebar.selectbox(t["einst_sound"], list(sound_links.keys()))
sound_url = sound_links[ausgewaehlter_sound]

# 📱 HAUPTBILDSCHIRM
st.title(t["titel"])
st.markdown("---")

# 🧠 TIMER LOGIK
if "zeit_uebrig" not in st.session_state:
    st.session_state.zeit_uebrig = minuten_einstellung * 60
if "status" not in st.session_state:
    st.session_state.status = "bereit"

if st.session_state.status == "bereit":
    st.session_state.zeit_uebrig = minuten_einstellung * 60

display_placeholder = st.empty()
audio_placeholder = st.empty()

# 🎛️ BUTTONS (Zentriert)
col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.status in ["bereit", "pausiert"]:
        if st.button(t['start'], use_container_width=True):
            st.session_state.status = "laeuft"
            st.rerun()

with col2:
    if st.session_state.status == "laeuft":
        if st.button(t['pause'], use_container_width=True):
            st.session_state.status = "pausiert"
            st.rerun()

with col3:
    if st.session_state.status != "bereit":
        if st.button(t['reset'], use_container_width=True):
            st.session_state.status = "bereit"
            st.session_state.zeit_uebrig = minuten_einstellung * 60
            st.rerun()

# ⏱️ COUNTDOWN-LOOP
if st.session_state.status == "laeuft":
    while st.session_state.zeit_uebrig > 0 and st.session_state.status == "laeuft":
        mins, secs = divmod(st.session_state.zeit_uebrig, 60)
        zeit_format = f"{mins:02d}:{secs:02d}"
        
        display_placeholder.markdown(f"""
            <div class="timer-box">
                <div>
                    <div class="timer-text">{zeit_format}</div>
                    <div class="sub-text">FOCUS</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        time.sleep(1)
        st.session_state.zeit_uebrig -= 1

    if st.session_state.zeit_uebrig == 0:
        st.session_state.status = "bereit"
        st.session_state.zeit_uebrig = minuten_einstellung * 60
        st.balloons()
        st.success(t["erfolg"])
        
        # 🔥 SAMSUNG FIX: Der offizielle Player wird direkt eingeblendet und gestartet
        with audio_placeholder.container():
            st.write(t["sound_bereit"])
            st.audio(sound_url, format="audio/mp3", autoplay=True)

# ZUSTANDS-ANZEIGEN
if st.session_state.status == "pausiert":
    mins, secs = divmod(st.session_state.zeit_uebrig, 60)
    display_placeholder.markdown(f"""<div class="timer-box"><div><div class="timer-text">{mins:02d}:{secs:02d}</div><div class="sub-text">PAUSED</div></div></div>""", unsafe_allow_html=True)
elif st.session_state.status == "bereit":
    mins, secs = divmod(st.session_state.zeit_uebrig, 60)
    display_placeholder.markdown(f"""<div class="timer-box"><div><div class="timer-text">{mins:02d}:{secs:02d}</div><div class="sub-text">READY</div></div></div>""", unsafe_allow_html=True)

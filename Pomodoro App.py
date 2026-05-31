import streamlit as st
import time

# 🎨 Seiten-Setup
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
        "player_titel": "🔊 KLICKE RECHTS AUF DAS DREIECK FÜR DEN TON:"
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
        "player_titel": "🔊 CLICK THE PLAY TRIANGLE FOR AUDIO:"
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
        "player_titel": "🔊 HAZ CLIC EN EL TRIÁNGULO PARA EL SONIDO:"
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
        "player_titel": "🔊 KLIK OP DE DRIEHOEK VOOR GELUID:"
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
        "player_titel": "🔊 CLIQUEZ SUR LE TRIANGLE POUR LE SON:"
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
        "player_titel": "🔊 CLICCA SUL TRIANGOLO PER IL SUONO:"
    }
}

# Extrem stabile und zuverlässige Songs, die jeder Browser sofort abspielen kann
sound_links = {
    "Song 1": "https://soundhelix.com",
    "Song 2": "https://soundhelix.com",
    "Song 3": "https://soundhelix.com"
}

# 🌌 CSS: Macht den Kreis chic und bringt den Player ganz nach vorne!
st.markdown("""
    <style>
    .stApp { font-family: 'Courier New', monospace; }
    .timer-box {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px auto;
        width: min(260px, 60vw);
        height: min(260px, 60vw);
        border-radius: 50%;
        border: 6px solid #1f6feb;
        box-shadow: 0 0 15px #1f6feb, inset 0 0 15px #1f6feb;
        background-color: rgba(31, 111, 235, 0.05);
    }
    .timer-text {
        font-size: min(45px, 10vw);
        font-weight: bold;
        letter-spacing: 2px;
        text-align: center;
        color: currentColor;
    }
    .sub-text {
        font-size: min(12px, 3vw);
        color: #58a6ff;
        text-align: center;
        letter-spacing: 3px;
        margin-top: -5px;
    }
    /* 🔥 Klick-Rettung: Zwingt den HTML-Player in den absoluten Vordergrund */
    .audio-container {
        position: relative;
        z-index: 99999 !important;
        margin: 30px auto;
        padding: 15px;
        background: rgba(31, 111, 235, 0.1);
        border-radius: 10px;
        border: 1px solid #1f6feb;
        text-align: center;
    }
    audio {
        width: 100%;
        max-width: 350px;
        height: 54px;
    }
    </style>
    """, unsafe_allow_html=True)

# ⚙️ SIDEBAR (Einstellungen)
st.sidebar.title("⚙️ CONFIG")
sprache = st.sidebar.selectbox("🌐 LANGUAGE", ["Deutsch", "English", "Español", "Nederlands", "Français", "Italiano"])
t = texte[sprache]

st.sidebar.markdown("---")
st.sidebar.subheader(t["einst_titel"])

# 🧠 WICHTIG: Eindeutige "key"-Zuweisung, damit sich der Slider nicht aufhängt!
minuten_einstellung = st.sidebar.slider(t["einst_zeit"], min_value=1, max_value=60, value=25, key="pomodoro_slider")
ausgewaehlter_sound = st.sidebar.selectbox(t["einst_sound"], list(sound_links.keys()))
sound_url = sound_links[ausgewaehlter_sound]

# 📱 HAUPTBILDSCHIRM
st.title(t["titel"])
st.markdown("---")

# Session State Variablen initialisieren
if "zeit_uebrig" not in st.session_state:
    st.session_state.zeit_uebrig = minuten_einstellung * 60
if "status" not in st.session_state:
    st.session_state.status = "bereit"

# Wenn die Uhr bereitsteht, folgt sie dem Slider sofort
if st.session_state.status == "bereit":
    st.session_state.zeit_uebrig = minuten_einstellung * 60

display_placeholder = st.empty()
audio_placeholder = st.empty()

# 🎛️ BUTTONS
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

# ⏱️ COUNTDOWN-SCHLEIFE
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
        
        display_placeholder.markdown(f"""<div class="timer-box"><div><div class="timer-text">00:00</div><div class="sub-text">DONE</div></div></div>""", unsafe_allow_html=True)
        st.balloons()
        st.success(t["erfolg"])
        
        # 🔥 DIE ABSOLUTE RETTUNG: Verpackt in einer klickbaren CSS-Box im absoluten Vordergrund!
        audio_placeholder.markdown(
            f"""
            <div class="audio-container">
                <p style="font-weight: bold; margin-bottom: 10px; color: #58a6ff;">{t['player_titel']}</p>
                <audio controls autoplay>
                    <source src="{sound_url}" type="audio/mp3">
                </audio>
            </div>
            """,
            unsafe_allow_html=True
        )

# ANZEIGE WENN PAUSIERT
if st.session_state.status == "pausiert":
    mins, secs = divmod(st.session_state.zeit_uebrig, 60)
    display_placeholder.markdown(f"""<div class="timer-box"><div><div class="timer-text">{mins:02d}:{secs:02d}</div><div class="sub-text">PAUSED</div></div></div>""", unsafe_allow_html=True)

# ANZEIGE WENN BEREIT
elif st.session_state.status == "bereit":
    mins, secs = divmod(st.session_state.zeit_uebrig, 60)
    display_placeholder.markdown(f"""<div class="timer-box"><div><div class="timer-text">{mins:02d}:{secs:02d}</div><div class="sub-text">READY</div></div></div>""", unsafe_allow_html=True)

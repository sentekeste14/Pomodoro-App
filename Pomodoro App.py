import streamlit as st
import time

# 🎨 Futuristisches Seiten-Setup
st.set_page_config(
    page_title="NEO Pomodoro",
    page_icon="⚡",
    layout="centered"
)

# 🌍 Wörterbuch mit allen Übersetzungen
texte = {
    "Deutsch": {
        "titel": "⚡ NEO POMODORO",
        "untertitel": "FUTURISTISCHES FOKUS-SYSTEM",
        "start": "START",
        "reset": "RESET",
        "erfolg": "🚀 FOKUS-PHASE BEENDET!",
        "einst_titel": "⚙️ SYSTEM-STEUERUNG",
        "einst_sound": "🔔 AUDIO-SIGNAL",
        "einst_zeit": "⏱️ DAWER (MINUTEN)"
    },
    "English": {
        "titel": "⚡ NEO POMODORO",
        "untertitel": "FUTURISTIC FOCUS SYSTEM",
        "start": "START",
        "reset": "RESET",
        "erfolg": "🚀 FOCUS PHASE COMPLETE!",
        "einst_titel": "⚙️ SYSTEM CONTROL",
        "einst_sound": "🔔 AUDIO SIGNAL",
        "einst_zeit": "⏱️ DURATION (MINUTES)"
    },
    "Español": {
        "titel": "⚡ NEO POMODORO",
        "untertitel": "SISTEMA DE ENFOQUE FUTURISTA",
        "start": "INICIAR",
        "reset": "REINICIAR",
        "erfolg": "🚀 ¡FASE DE ENFOQUE COMPLETADA!",
        "einst_titel": "⚙️ CONTROL DEL SISTEMA",
        "einst_sound": "🔔 SEÑAL DE AUDIO",
        "einst_zeit": "⏱️ DURACIÓN (MINUTOS)"
    },
    "Nederlands": {
        "titel": "⚡ NEO POMODORO",
        "untertitel": "FUTURISTISCH FOCUS SYSTEEM",
        "start": "START",
        "reset": "RESET",
        "erfolg": "🚀 FOCUSFASE VOLTOOID!",
        "einst_titel": "⚙️ SYSTEEMCONTROLE",
        "einst_sound": "🔔 AUDIOSIGNAAL",
        "einst_zeit": "⏱️ DUUR (MINUTEN)"
    },
    "Français": {
        "titel": "⚡ NEO POMODORO",
        "untertitel": "SYSTÈME DE CONCENTRATION FUTURISTE",
        "start": "DÉMARRER",
        "reset": "RÉINITIALISER",
        "erfolg": "🚀 PHASE DE CONCENTRATION TERMINÉE !",
        "einst_titel": "⚙️ CONTRÔLE DU SYSTÈME",
        "einst_sound": "🔔 SIGNAL AUDIO",
        "einst_zeit": "⏱️ DURÉE (MINUTES)"
    },
    "Italiano": {
        "titel": "⚡ NEO POMODORO",
        "untertitel": "SISTEMA DI CONCENTRAZIONE FUTURISTICO",
        "start": "AVVIA",
        "reset": "RESET",
        "erfolg": "🚀 FASE DI CONCENTRAZIONE COMPLETATA!",
        "einst_titel": "⚙️ CONTROLO SISTEMA",
        "einst_sound": "🔔 SEGNALE AUDIO",
        "einst_zeit": "⏱️ DURATA (MINUTI)"
    }
}

sound_links = {
    "Digital Watch": "https://google.com",
    "Cyber Bell": "https://google.com",
    "Energy Horn": "https://google.com"
}

# 🌌 CSS für den flexiblen Neon-Kreis mit automatischer Schriftfarbe (currentColor)
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
        color: currentColor; /* 💡 Wechselt automatisch zwischen Schwarz und Weiß! */
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
st.caption(t["untertitel"])
st.markdown("---")

display_placeholder = st.empty()

# Start-Button direkt unter der Uhr
if st.button(t['start'], use_container_width=True):
    gesamt_sekunden = minuten_einstellung * 60
    
    # Der echte Live-Countdown
    for verbleibend in range(gesamt_sekunden, -1, -1):
        mins, secs = divmod(verbleibend, 60)
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
    
    # Wenn fertig
    st.balloons()
    st.success(t["erfolg"])
    
    # Sound abspielen
    st.markdown(f'<iframe src="{sound_url}" allow="autoplay" style="display:none;"></iframe>', unsafe_allow_html=True)

else:
    # Standard-Anzeige im Ruhezustand
    zeit_format = f"{minuten_einstellung:02d}:00"
    display_placeholder.markdown(f"""
        <div class="timer-box">
            <div>
                <div class="timer-text">{zeit_format}</div>
                <div class="sub-text">READY</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

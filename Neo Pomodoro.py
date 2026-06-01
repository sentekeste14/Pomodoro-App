import streamlit as st
import time
st.markdown('<meta name="google-site-verification" content="DEIN_CODE_VON_GOOGLE" />', unsafe_allow_html=True)

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
        "einst_zeit": "⏱️ DAUER (MINUTEN)",
        "einst_stimme": "🗣️ STIMME",
        "maennlich": "Männlich",
        "weiblich": "Weiblich",
        "stimme_code": "de-DE",
        "stimme_text": "Zeit vorbei! Mach eine wohlverdiente Pause."
    },
    "English": {
        "titel": "NEO POMODORO",
        "start": "START",
        "pause": "PAUSE",
        "reset": "RESET",
        "erfolg": "🚀 FOCUS PHASE COMPLETE!",
        "einst_titel": "⚙️ SYSTEM CONTROL",
        "einst_zeit": "⏱️ DURATION (MINUTES)",
        "einst_stimme": "🗣️ VOICE GENDER",
        "maennlich": "Male",
        "weiblich": "Female",
        "stimme_code": "en-US",
        "stimme_text": "Time is up! Take a well deserved break."
    },
    "Español": {
        "titel": "NEO POMODORO",
        "start": "INICIAR",
        "pause": "PAUSA",
        "reset": "REINICIAR",
        "erfolg": "🚀 ¡FASE DE ENFOQUE COMPLETADA!",
        "einst_titel": "⚙️ CONTROL DEL SISTEMA",
        "einst_zeit": "⏱️ DURACIÓN (MINUTOS)",
        "einst_stimme": "🗣️ VOZ",
        "maennlich": "Masculino",
        "weiblich": "Femenino",
        "stimme_code": "es-ES",
        "stimme_text": "Tiempo agotado. Tomate un merecido descanso."
    },
    "Nederlands": {
        "titel": "NEO POMODORO",
        "start": "START",
        "pause": "PAUZE",
        "reset": "RESET",
        "erfolg": "🚀 FOCUSFASE VOLTOOID!",
        "einst_titel": "⚙️ SYSTEEMCONTROLE",
        "einst_zeit": "⏱️ DUUR (MINUTEN)",
        "einst_stimme": "🗣️ STEM",
        "maennlich": "Mannelijk",
        "weiblich": "Vrouwelijk",
        "stimme_code": "nl-NL",
        "stimme_text": "Tijd is om. Neem een welverdiende pauze."
    },
    "Français": {
        "titel": "NEO POMODORO",
        "start": "DÉMARRER",
        "pause": "PAUSE",
        "reset": "RÉINITIALISER",
        "erfolg": "🚀 PHASE DE CONCENTRATION TERMINÉE !",
        "einst_titel": "⚙️ CONTRÔLE DU SYSTÈME",
        "einst_zeit": "⏱️ DURÉE (MINUTES)",
        "einst_stimme": "🗣️ VOIX",
        "maennlich": "Masculin",
        "weiblich": "Féminin",
        "stimme_code": "fr-FR",
        "stimme_text": "Le temps est ecoule. Prenez une pause bien meritee."
    },
    "Italiano": {
        "titel": "NEO POMODORO",
        "start": "AVVIA",
        "pause": "PAUSA",
        "reset": "RESET",
        "erfolg": "🚀 FASE DI CONCENTRAZIONE COMPLETATA!",
        "einst_titel": "⚙️ CONTROLLO SISTEMA",
        "einst_zeit": "⏱️ DURATA (MINUTI)",
        "einst_stimme": "🗣️ VOCE",
        "maennlich": "Maschile",
        "weiblich": "Femminile",
        "stimme_code": "it-IT",
        "stimme_text": "Tempo scaduto. Fai una meritata pausa."
    }
}

# 🌌 CSS: Layout-Optimierung
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
    </style>
    """, unsafe_allow_html=True)

# ⚙️ SIDEBAR (Einstellungen)
st.sidebar.title("⚙️ CONFIG")
sprache = st.sidebar.selectbox("🌐 LANGUAGE", ["Deutsch", "English", "Español", "Nederlands", "Français", "Italiano"])
t = texte[sprache]

st.sidebar.markdown("---")
st.sidebar.subheader(t["einst_titel"])

# Zeitschieber
minuten_einstellung = st.sidebar.slider(t["einst_zeit"], min_value=1, max_value=60, value=25, key="pomodoro_slider")

# Auswahl des Geschlechts der Stimme
geschlecht_auswahl = st.sidebar.selectbox(t["einst_stimme"], [t["weiblich"], t["maennlich"]])
js_geschlecht = "female" if geschlecht_auswahl == t["weiblich"] else "male"

# 📱 HAUPTBILDSCHIRM
st.title(t["titel"])
st.markdown("---")

# Session State initialisieren
if "zeit_uebrig" not in st.session_state:
    st.session_state.zeit_uebrig = minuten_einstellung * 60
if "status" not in st.session_state:
    st.session_state.status = "bereit"

if st.session_state.status == "bereit":
    st.session_state.zeit_uebrig = minuten_einstellung * 60

display_placeholder = st.empty()
audio_trigger = False

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
        audio_trigger = True
        st.balloons()
        st.success(t["erfolg"])

# ANZEIGE PAUSIERT / BEREIT
if st.session_state.status == "pausiert":
    mins, secs = divmod(st.session_state.zeit_uebrig, 60)
    display_placeholder.markdown(f"""<div class="timer-box"><div><div class="timer-text">{mins:02d}:{secs:02d}</div><div class="sub-text">PAUSED</div></div></div>""", unsafe_allow_html=True)
elif st.session_state.status == "bereit" and not audio_trigger:
    display_placeholder.markdown(f"""<div class="timer-box"><div><div class="timer-text">{minuten_einstellung:02d}:00</div><div class="sub-text">READY</div></div></div>""", unsafe_allow_html=True)

# 🗣️ REPARIERTE JAVASCRIPT-SPRACHAUSGABE (Ohne f-string Konflikt)
if audio_trigger:
    javascript_code = """
    <script>
        var msg = new SpeechSynthesisUtterance("STIMME_TEXT_PLACEHOLDER");
        msg.lang = "STIMME_CODE_PLACEHOLDER";
        
        function setVoiceAndSpeak() {
            var voices = window.speechSynthesis.getVoices();
            var gewaehltesGeschlecht = "JS_GESCHLECHT_PLACEHOLDER";
            var sprachCode = "STIMME_CODE_PLACEHOLDER";
            
            for (var i = 0; i < voices.length; i++) {
                if (voices[i].lang.startsWith(sprachCode.split('-')[0])) {
                    var nameLower = voices[i].name.toLowerCase();
                    if (gewaehltesGeschlecht === "male" && (nameLower.includes("male") || nameLower.includes("david") || nameLower.includes("stefan") || nameLower.includes("christoph"))) {
                        msg.voice = voices[i];
                        break;
                    } else if (gewaehltesGeschlecht === "female" && (nameLower.includes("female") || nameLower.includes("hazel") || nameLower.includes("hedda") || nameLower.includes("katja") || nameLower.includes("amalie"))) {
                        msg.voice = voices[i];
                        break;
                    }
                }
            }
            window.speechSynthesis.speak(msg);
        }

        if (window.speechSynthesis.onvoiceschanged !== undefined) {
            window.speechSynthesis.onvoiceschanged = setVoiceAndSpeak;
        }
        
        var voices = window.speechSynthesis.getVoices();
        if (voices.length > 0) {
            setVoiceAndSpeak();
        }
    </script>
    """
    # Hier werden die Python-Variablen sicher ohne f-string Fehler in den Text eingesetzt:
    javascript_code = javascript_code.replace("STIMME_TEXT_PLACEHOLDER", t['stimme_text'])
    javascript_code = javascript_code.replace("STIMME_CODE_PLACEHOLDER", t['stimme_code'])
    javascript_code = javascript_code.replace("JS_GESCHLECHT_PLACEHOLDER", js_geschlecht)
    
    st.components.v1.html(javascript_code, height=0)

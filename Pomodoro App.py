import streamlit as st
import time

# 🌍 Wörterbuch mit allen Übersetzungen
texte = {
    "Deutsch": {
        "titel": "⏱️ Mein Handy-Lerntimer",
        "untertitel": "Fokussiere dich auf deine Aufgaben!",
        "frage": "Wie lange möchtest du lernen?",
        "button": "Timer starten 🚀",
        "info": "Der Timer läuft für {} Minuten. Bleib fokussiert!",
        "erfolg": "🎉 Zeit vorbei! Mach eine wohlverdienst Pause."
    },
    "English": {
        "titel": "⏱️ My Study Timer",
        "untertitel": "Focus on your tasks!",
        "frage": "How long do you want to study?",
        "button": "Start Timer 🚀",
        "info": "The timer is running for {} minutes. Stay focused!",
        "erfolg": "🎉 Time's up! Take a well-deserved break."
    },
    "Español": {
        "titel": "⏱️ Mi Temporizador de Estudio",
        "untertitel": "¡Concéntrate en tus tareas!",
        "frage": "¿Cuánto tiempo quieres estudiar?",
        "button": "Iniciar Temporizador 🚀",
        "info": "El temporizador está corriendo por {} minutos. ¡Mantente concentrado!",
        "erfolg": "🎉 ¡Tiempo agotado! Tómate un merecido descanso."
    },
    "Nederlands": {
        "titel": "⏱️ Mijn Studietimer",
        "untertitel": "Concentreer je op je taken!",
        "frage": "Hoe lang wil je studeren?",
        "button": "Start Timer 🚀",
        "info": "De timer loopt voor {} minuten. Blijf gefocust!",
        "erfolg": "🎉 Tijd is om! Neem een welverdiende pauze."
    },
    "Français": {
        "titel": "⏱️ Mon Minuteur d'Étude",
        "untertitel": "Restez concentré sur vos tâches !",
        "frage": "Combien de temps voulez-vous étudier ?",
        "button": "Démarrer le Minuteur 🚀",
        "info": "Le minuteur tourne pendant {} minutes. Restez concentré !",
        "erfolg": "🎉 Le temps est écoulé ! Prenez une pause bien méritée."
    },
    "Italiano": {
        "titel": "⏱️ Il mio Timer di Studio",
        "untertitel": "Concentrati sui tuoi compiti!",
        "frage": "Quanto tempo vuoi studiare?",
        "button": "Avvia Timer 🚀",
        "info": "Il timer è attivo per {} minuti. Rimani concentrato!",
        "erfolg": "🎉 Tempo scaduto! Fai una meritata pausa."
    }
}

# 1. Sprachauswahl auf der Webseite anzeigen
sprache = st.selectbox("🌐 Language / Sprache / Idioma",
                       ["Deutsch", "English", "Español", "Nederlands", "Français", "Italiano"])

# Aktuelle Texte basierend auf der Auswahl laden
t = texte[sprache]

# 2. Webseite mit den gewählten Texten aufbauen
st.title(t["titel"])
st.write(t["untertitel"])

# Zeitauswahl
minuten = st.selectbox(t["frage"], [5, 10, 15, 25, 45, 60])

# Start-Button
if st.button(t["button"]):
    st.info(t["info"].format(minuten))

    # Fortschrittsbalken
    fortschritt = st.progress(0)
    gesamt_sekunden = minuten * 60

    for sekunde in range(gesamt_sekunden):
        time.sleep(1)
        prozent = int((sekunde + 1) / gesamt_sekunden * 100)
        fortschritt.progress(prozent)

    st.balloons()  # Feier-Effekt
    st.success(t["erfolg"])
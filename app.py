import streamlit as st
from pydub import AudioSegment
from pydub.playback import play
import os
from xttsv2 import TTSmodel

# Funzione per estrarre testo da PDF
def extract_text_from_pdf(file):
    return "Testo estratto dal PDF"

# Funzione per riprodurre audio
def play_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    play(audio)

# Interfaccia Streamlit
st.title('Applicazione PDF e Audio con Streamlit')

st.info("Caricamento modello TTS")
tts = TTSmodel("tts_models/multilingual/multi-dataset/xtts_v2")
st.info("Modello TTS caricato con successo")

# Box per inserire un PDF
uploaded_pdf = st.file_uploader("Carica il tuo libro in formato PDF", type="pdf")

# Select box per selezionare un file audio
audio_folder = "references_audio"  # Sostituisci con il percorso della tua cartella audio
audio_files = [f for f in os.listdir(audio_folder) if f.endswith(('.mp3', '.wav'))]
selected_audio = st.selectbox("Seleziona una voce da usare per la narrazione", audio_files)

# Bottone di generazione
if st.button('Genera e Riproduci'):
    if uploaded_pdf is not None and selected_audio is not None:
        # Estrazione testo dal PDF
        text = extract_text_from_pdf(uploaded_pdf)
        st.text_area("Testo estratto dal PDF", text, height=200)

        # Riproduzione audio
        audio_path = os.path.join(audio_folder, selected_audio)
        st.write(f"Riproduzione di: {selected_audio}")
        # Suite per ascoltare l'audio generato
        st.audio(audio_path)
    else:
        st.warning("Per favore, carica un file PDF e seleziona un file audio.")


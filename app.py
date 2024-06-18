import streamlit as st
import time
from xttsv2 import TTSmodel
import os

# Function to simulate model loading
def load_models():
    st.info("Caricamento modello TTS...")
    tts = TTSmodel()
    st.success("Modello TTS caricato con successo")
    return tts

# Function to extract basic stats from PDF
def extract_pdf_stats(file):
    return 5, 100, 500

# Streamlit app
st.title("CantastorIA")

# Section to load neural models
st.header("Load Neural Models")
if 'tts_model' not in st.session_state:
    st.session_state.tts_model = None

if st.button("Carica Modelli"):
    with st.spinner("Caricamento in corso..."):
        st.session_state.tts_model = load_models()
    st.success("Tutti i modelli sono stati caricati con successo!")

# Section to upload PDF and show stats
st.header("Upload PDF and Show Stats")
uploaded_file = st.file_uploader("Scegli un file PDF", type="pdf")

if uploaded_file is not None:
    num_pages, num_words, num_chars = extract_pdf_stats(uploaded_file)

    st.subheader("Statistiche del PDF")
    st.write(f"Numero di pagine: {num_pages}")
    st.write(f"Numero di parole: {num_words}")
    st.write(f"Numero di caratteri: {num_chars}")

# Select box per selezionare un file audio
audio_folder = "references_audio"  # Sostituisci con il percorso della tua cartella audio
audio_files = [f for f in os.listdir(audio_folder) if f.endswith(('.mp3', '.wav'))]
selected_audio = st.selectbox("Seleziona una voce da usare per la narrazione", audio_files)

text = st.text_area("Testo da convertire in audio")
# Bottone di generazione
if st.button('Genera e Riproduci'):
    if st.session_state.tts_model:
        # Generazione audio
        st.session_state.tts_model(text=text, file_path="output.wav", speaker_wav=os.path.join(audio_folder, selected_audio), language="it")
        # Riproduzione audio
        st.audio("output.wav")
    else:
        st.error("Modello TTS non caricato. Per favore, carica il modello prima di generare l'audio.")

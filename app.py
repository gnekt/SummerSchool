import streamlit as st
import time
from xttsv2 import TTSmodel
from sound_generator import TTAmodel
import os

# Function to simulate model loading
def load_models():
    st.info("Caricamento modello TTS...")
    tts = TTSmodel()
    st.success("Modello TTS caricato con successo")

    tta = TTAmodel()
    st.success("Modello TTA caricato con successo")
    
    return tts, tta

# Function to extract basic stats from PDF
def extract_pdf_stats(file):
    return 5, 100, 500

# Streamlit app
st.title("CantastorIA")

# Section to load neural models
st.header("Load Neural Models")
if 'tts_model' not in st.session_state:
    st.session_state.tts_model = None

if 'tta_model' not in st.session_state:
    st.session_state.tta_model = None

if st.button("Carica Modelli"):
    with st.spinner("Caricamento in corso..."):
        st.session_state.tts_model, st.session_state.tta_model = load_models()
    st.success("Tutti i modelli sono stati caricati con successo!")

# Section to upload PDF and show stats
st.header("Upload PDF and Show Stats")
uploaded_file = st.file_uploader("Scegli un file PDF", type="pdf")

if uploaded_file is not None:
    num_pages, num_words, num_chars = extract_pdf_stats(uploaded_file)
    #######
    # Analisi Testo
    #######
    # Direi di fare quel discorso dei paragrafi e della descrizione
    # Quindi tipo un array di tuple [(paragrafo, descrizione_per_musica), ...]

# Select box per selezionare un file audio
audio_folder = "references_audio"  # Sostituisci con il percorso della tua cartella audio
audio_files = [f for f in os.listdir(audio_folder) if f.endswith(('.mp3', '.wav'))]
selected_audio = st.selectbox("Seleziona una voce da usare per la narrazione", audio_files)

####### 
# Christian
#######
# Per ogni paragrafo genero il corrispettivo audio
# La struttura e' sempre un array di tuple del tipo [(audio, durata_in_secondi), ...]
 
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

#######
# Cristian
#######
# Sezione per generare la soundtrack
# a partire dalla tupla dei paragrafi e quelli degli audio.
# Per ogni elemento di entrambi gli array, generare una soundtrack che richiede
# La descrizione audio del paragrafo e la durata attesa dello spezzone audio
#
#parametri che servono per generare audio sottofondo, quindi per richiamare tta_model:
#prompt, seconds_total, steps, cfg_scale, api_name, output_path
# promp viene preso da GPT-4 con API
# seconds_total viene preso dalla lunghezza dell'audio generato da tts
# il resto dei parametri (tranne output_path) sono da tunare




####### Fase finale
# Viene fatto un merge di soundtrack e parlato per generare l'audio finale
# Vengono concatenati i vari spezzoni audio e generato un unico file audio
# Ogni spezzone entra in fade in e fade out per evitare discontinuita' audio
# L'audio finale viene riprodotto
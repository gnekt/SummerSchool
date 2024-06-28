import streamlit as st
import time
from xttsv2 import TTSmodel
# from sound_generator import TTAmodel
import os
import pandas as pd
import librosa
import soundfile as sf
# from our_gpt import query_GPT


available_books = {
    "Cappuccetto Rosso": "libri/cappuccetto_rosso.csv"
}

# Function to simulate model loading
# def load_models():
#     st.info("Caricamento modello TTS...")
#     # tts = TTSmodel()
#     st.success("Modello TTS caricato con successo")
#     st.info("Caricamento modello TTA...")
#     # tta = TTAmodel()
#     st.success("Modello TTA caricato con successo")
#     return tts, tta

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
st.divider()

# Section to upload PDF and show stats
st.header("Seleziona un libro")
selected_book = st.selectbox("Seleziona un libro", list(available_books.keys()))

if selected_book is not None:
    book_path = available_books[selected_book]
    book = pd.read_csv(book_path, sep="|")
    st.success("Libro caricato con successo!")
    # Do some stats on the book
    st.write(f"#Paragraphs: {len(book)}")
    st.write(f"Average length of each paragraph: {book['text'].str.len().mean()}")
    st.write(f"Words count: {book['text'].str.split().str.len().sum()}")
st.divider()

st.header("Configurazioni")
# Select box per selezionare un file audio
audio_folder = "references_audio"  # Sostituisci con il percorso della tua cartella audio
audio_files = [f for f in os.listdir(audio_folder) if f.endswith(('.mp3', '.wav'))]
selected_audio = st.selectbox("Seleziona una voce da usare per la narrazione", audio_files)
language = st.selectbox("Seleziona la lingua", ["it", "en"])

st.divider()

# Bottone di generazione
if st.button('Genera e Riproduci'):
    ####### 
    # Christian
    #######
    # Per ogni paragrafo genero il corrispettivo audio
    # La struttura e' sempre un array di tuple del tipo [(audio, durata_in_secondi), ...]
    generated_speeches = []
    if st.session_state.tts_model:
        # Generazione audio
        for index, row in book.iterrows():
            text = row["text"]
            if len(text) > 213:
                _splitted_text = text.split("...")
                _audio_gen = []
                for _text in _splitted_text:
                    if len(_text) == 0:
                        continue
                    _audio_gen += st.session_state.tts_model._tts.tts(text=_text, speaker_wav=os.path.join(audio_folder, selected_audio), language=language)
                st.write(f"Audio for paragraph {index} generated, duration: {len(_audio_gen)//24e3} seconds")
                # Save wav file
                generated_speeches.append((_audio_gen, len(_audio_gen)//24e3))
                sf.write(f"./temp/voice/{index}.wav", _audio_gen, int(24e3))    
            else:        
                _audio_gen = st.session_state.tts_model(text=text, file_path=f"./temp/voice/{index}.wav", speaker_wav=os.path.join(audio_folder, selected_audio), language=language)
                # Evaluate audio duration
                generated_speeches.append((_audio_gen, len(_audio_gen)//24e3))
                st.write(f"Audio for paragraph {index} generated, duration: {len(_audio_gen)//24e3} seconds")            
                # Riproduzione audio
            st.audio(f"./temp/voice/{index}.wav")
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

    if st.session_state.tta_model:
        # Generazione audio
        generated_music = []
        for (audio, duration),(index, row) in zip(generated_speeches, book.iterrows()):
            _audio_gen = st.session_state.tta_model(prompt=row["music_prompt"], seconds_total=duration, steps=100, cfg_scale=10, api_name="/predict", output_path=f"./temp/music/{index}.wav")
            generated_music.append(_audio_gen)
            st.write(f"Audio for paragraph {index} generated, duration: {len(_audio_gen)//44100} seconds")
            # Riproduzione audio
            st.audio(f"./temp/music/{index}.wav")

    ####### Fase finale
    # Viene fatto un merge di soundtrack e parlato per generare l'audio finale
    # Vengono concatenati i vari spezzoni audio e generato un unico file audio
    # Ogni spezzone entra in fade in e fade out per evitare discontinuita' audio
    # L'audio finale viene riprodotto
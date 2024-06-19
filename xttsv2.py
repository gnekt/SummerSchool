from typing import Any
from TTS.api import TTS

        
class TTSmodel:
    def __init__(self):
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        self.tts.to("cuda")
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.tts.tts_to_file(*args, **kwds)
    

tts = TTSmodel()
tts(text="It took me quite a long time to develop a voice.It took me quite a long time to develop a voice.It took me quite a long time to develop a voice.It took me quite a long time to develop a voice.It took me quite a long time to develop a voice, and now that I have it I'm not going to be silent. Vorrei provare un testo che superi i 200 caratteri per fare in modo che le cose vadano meglio",
                file_path="output.wav",
                speaker_wav="",
                language="en")

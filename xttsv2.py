from typing import Any
from TTS.api import TTS

        
class TTSmodel:
    def __init__(self, model_path):
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.tts(*args, **kwds)
    

from typing import Any
from TTS.api import TTS

        
class TTSmodel:
    def __init__(self):
        self._tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        self._tts.to("cuda")
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self._tts.synthesize(*args, **kwds)
    

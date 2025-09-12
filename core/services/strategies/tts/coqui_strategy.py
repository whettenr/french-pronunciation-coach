import tempfile
import torch
from TTS.api import TTS  # from coqui-tts
from core.services.strategies.tts.base_strategy import TTSSynthesisStrategy

class CoquiTTSStrategy(TTSSynthesisStrategy):
    def __init__(self, model_name="tts_models/fr/css10/vits"):
        print(f"Loading Coqui TTS model: {model_name}")
        self.tts = TTS(model_name)
        print("Coqui TTS loaded!")

    def synthesize(self, text: str) -> str:
        tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        self.tts.tts_to_file(text=text, file_path=tmp_file.name)
        return tmp_file.name
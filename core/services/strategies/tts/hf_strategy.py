import tempfile
import torch
from transformers import VitsModel, AutoTokenizer
from core.services.strategies.tts.base_strategy import TTSSynthesisStrategy
import soundfile as sf

class HuggingStrategy(TTSSynthesisStrategy):
    def __init__(self, model_name="facebook/mms-tts-fra"):
        print(f"Loading Hugging Face VITS model: {model_name}")
        self.model = VitsModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model.eval()
        print("Hugging Face VITS loaded!")

    def synthesize(self, text: str) -> str:
        inputs = self.tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)
            waveform = outputs.waveform.squeeze().cpu().numpy()

        # Save to temp wav file
        tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(tmp_file.name, waveform, self.model.config.sampling_rate)

        return tmp_file.name
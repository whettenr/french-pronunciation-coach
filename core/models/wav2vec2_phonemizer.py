from .base import BasePhonemeModel
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

class Wav2Vec2Phonemizer(BasePhonemeModel):
    def __init__(self, model_name="Cnam-LMSSC/wav2vec2-french-phonemizer", device=None):
        if device:
            self.device = device
        elif torch.backends.mps.is_available():
            self.device = "mps"
        elif torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def transcribe(self, audio_path: str) -> str:
        # Load audio
        waveform, sample_rate = torchaudio.load(audio_path)
        # Resample if needed
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)
        # Convert to mono
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
        # Get input values
        input_values = self.processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt").input_values
        input_values = input_values.to(self.device)
        # Forward pass
        with torch.no_grad():
            logits = self.model(input_values).logits
        # Decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)
        return transcription[0]
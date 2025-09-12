from pathlib import Path
import shutil
import os
import uuid
from pydub import AudioSegment
from core.models.wav2vec2_phonemizer import Wav2Vec2Phonemizer

class PhonemizerService:
    def __init__(self):
        self.model = Wav2Vec2Phonemizer()

    def webm_to_wav(self, webm_path: Path, wav_path: Path) -> Path:
        """Convert a WebM audio file to WAV format."""
        # this is a work around to handle chrome webm files
        try:
            audio = AudioSegment.from_file(webm_path, format="webm")
            audio.export(wav_path, format="wav")
            os.remove(webm_path)  # Remove the original webm after conversion
            return wav_path
        except Exception as e:
            print(f"Error converting {webm_path} to WAV: {e}")
            return webm_path

    def audio_to_phonemes(self, file_path: Path) -> str:
        """
        Transcribe an audio file to phonemes.
        """
        phonemes = self.model.transcribe(str(file_path))
        os.remove(file_path)  # Clean up the audio file after processing
        return phonemes

    def save_audio(self, file, save_dir: Path) -> Path:
        """
        Save uploaded audio file and convert if needed.
        Returns the final file path (WAV if converted).
        """
        save_dir.mkdir(exist_ok=True, parents=True)
        # Use random filename to avoid conflicts
        ext = file.filename.split('.')[-1] if '.' in file.filename else 'webm'
        random_name = f"{uuid.uuid4()}.{ext}"
        save_path = save_dir / random_name

        # Save uploaded file
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Auto-convert WebM to WAV
        if save_path.suffix.lower() == ".webm":
            wav_path = save_path.with_suffix(".wav")
            print(f"the current save_path is {save_path}")
            save_path = self.webm_to_wav(save_path, wav_path)
            print(f"the new save_path is {save_path}")

        return save_path
from abc import ABC, abstractmethod

class BasePhonemeModel(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str) -> str:
        """Return the phonemes from the audio file"""
        pass
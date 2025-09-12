# services/strategies/tts/base_strategy.py
from abc import ABC, abstractmethod

class TTSSynthesisStrategy(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> str:
        """Generate speech audio from text. Returns path to WAV file."""
        pass
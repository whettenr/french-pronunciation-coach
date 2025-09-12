# services/tts_service.py
from core.services.strategies.tts.base_strategy import TTSSynthesisStrategy

class TTSService:
    def __init__(self, strategy: TTSSynthesisStrategy):
        if strategy is None:
            raise ValueError("TTSService requires a strategy, none provided.")
        self.strategy = strategy

    def synthesize(self, text: str) -> str:
        return self.strategy.synthesize(text)
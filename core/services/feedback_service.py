from core.services.strategies.feedback.base_strategy import FeedbackStrategy

class FeedbackService:
    def __init__(self, strategy: FeedbackStrategy):
        self.strategy = strategy

    def get_feedback(self, word: str, expected_phonemes: str, user_phonemes: str):
        return self.strategy.generate_feedback(word, expected_phonemes, user_phonemes)
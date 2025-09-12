from abc import ABC, abstractmethod

class FeedbackStrategy(ABC):
    @abstractmethod
    def generate_feedback(self, word: str, expected: str, attempt: str) -> str:
        pass
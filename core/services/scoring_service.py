import Levenshtein

class ScoringService:
    @staticmethod
    def score(correct: str, attempt: str) -> float:
        correct = correct.strip()
        attempt = attempt.strip()
        if not correct:
            return 0.0
        distance = Levenshtein.distance(correct, attempt)
        max_len = max(len(correct), len(attempt))
        return max(0.0, 1 - distance / max_len)
from core.phonetics import Phonetics

class SpeechService:
    """
    Service layer for text-based speech operations.
    Handles text -> IPA conversion.
    """
    def __init__(self):
        self.phonetics = Phonetics()

    def get_ipa(self, word: str) -> str:
        """
        Return IPA transcription of the given word.
        """
        return self.phonetics.text_to_ipa(word)
from phonemizer import phonemize

class Phonetics:
    def text_to_ipa(self, text: str) -> str:
        ipa = phonemize(
            text,
            language="fr-fr",
            backend="espeak",
            strip=True,
            preserve_punctuation=False,
            njobs=1,
        )
        return ipa
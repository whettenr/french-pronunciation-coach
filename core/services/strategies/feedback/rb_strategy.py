from __future__ import annotations
from difflib import SequenceMatcher
from typing import List, Tuple, Dict
from abc import ABC
import unicodedata

from core.services.feedback_service import FeedbackStrategy  # your abstract

def _nfkc(s: str) -> str:
    return unicodedata.normalize("NFKC", s)

def _tokenize_ipa(ipa: str) -> List[str]:
    ipa = _nfkc(ipa.strip())
    return [p for p in ipa.split() if p]

class RuleBasedFeedbackStrategy(FeedbackStrategy):
    """
    Enhanced rule-based French pronunciation feedback.
    Works on IPA sequences (space-separated).
    """

    SUB_MAP: Dict[Tuple[str, str], str] = {
        # Vowels
        ("y", "u"): "French **u** /y/ is like 'ee' with rounded lips. Avoid English 'oo'.",
        ("u", "y"): "French **ou** /u/ is a pure 'oo' sound. Relax tongue, lips slightly rounded.",
        ("e", "ɛ"): "Close **é** /e/ needs higher tongue than **è** /ɛ/. Smile gently.",
        ("ɛ", "e"): "Open **è** /ɛ/ needs more open mouth than **é** /e.",
        ("o", "ɔ"): "Close **o** /o/ is tenser than **ɔ**. Round lips firmly.",
        ("ɔ", "o"): "Open **ɔ** is laxer than /o/. Open mouth slightly.",
        # Nasals
        ("ɑ̃", "a"): "Nasal **an** /ɑ̃/: let air resonate through nose, don't add /n/.",
        ("ɛ̃", "e"): "Nasal **in** /ɛ̃/: open vowel, nasalize gently, avoid final /n/.",
        ("ɔ̃", "o"): "Nasal **on** /ɔ̃/: start near /ɔ/, nasalize, avoid 'on' with /n/.",
        ("œ̃", "ø"): "Nasal **un** /œ̃/: start from /ø/ and nasalize.",
        # French R
        ("ʁ", "r"): "French **r** /ʁ/ is uvular, not English tap. Think gentle gargle.",
        # Sibilants
        ("s", "z"): "Voiceless **s** /s/, whisper it.",
        ("z", "s"): "Voiced **z** /z/, feel vibration in throat.",
        ("ʃ", "ʒ"): "**ch** /ʃ/ is voiceless, keep it soft.",
        ("ʒ", "ʃ"): "**j** /ʒ/ is voiced, add gentle buzz.",
        # Glides
        ("ɥ", "j"): "French **u-glide** /ɥ/ (as in 'huit'), round lips.",
        # Additional vowels
        ("i", "e"): "French **i** /i/ is tense and high. Avoid laxing toward /e/.",
        ("ø", "œ"): "French **eu** /ø/ vs /œ/: round lips, adjust tongue height.",
        # Plosives / Stops
        ("p", "b"): "Voiceless **p** /p/ is unvoiced. Avoid sounding like English 'b'.",
        ("b", "p"): "Voiced **b** /b/ is voiced. Don't under-voice it.",
        ("t", "d"): "Voiceless **t** /t/ should not sound like 'd'. Place tongue on alveolar ridge.",
        ("d", "t"): "Voiced **d** /d/ should buzz slightly; don't overvoice like English 'd'.",
        ("k", "g"): "Voiceless **k** /k/ should not sound like 'g'. Tongue back and firm.",
        ("g", "k"): "Voiced **g** /g/ should sound firm, not like English 'k'.",
        # Additional learner confusions
        ("f", "v"): "Voiceless **f** /f/ should not buzz. English 'v' is voiced.",
        ("v", "f"): "Voiced **v** /v/ should buzz. Avoid under-voicing."
    }

    GENERIC_SUB = "Adjust this sound toward the French target. Repeat slowly and compare with a native speaker."
    GENERIC_INS = "You added an extra sound. Keep it smooth and avoid inserting this phone."
    GENERIC_DEL = "You skipped a sound. Repeat slowly and pronounce each phone."

    EXAMPLES: Dict[str, str] = {
        "y": "u in **lune**",
        "u": "ou in **tout**",
        "e": "é in **été**",
        "ɛ": "è in **mère**",
        "o": "o in **zéro**",
        "ɔ": "o in **port**",
        "ɑ̃": "an in **sans**",
        "ɛ̃": "in in **vin**",
        "ɔ̃": "on in **nom**",
        "œ̃": "un in **brun**",
        "ʁ": "r in **Paris**",
        "ʃ": "ch in **chat**",
        "ʒ": "j in **journal**",
        "s": "s in **sans**",
        "z": "z in **zéro**",
        "ɥ": "u-glide in **huit**",
        "j": "y-glide in **fille**",
        "p": "p in **pain**",
        "b": "b in **beau**",
        "t": "t in **temps**",
        "d": "d in **dame**",
        "k": "c in **clé**",
        "g": "g in **gare**",
        "f": "f in **faim**",
        "v": "v in **vin**",
    }

    def _align(self, expected: List[str], produced: List[str]):
        sm = SequenceMatcher(a=expected, b=produced, autojunk=False)
        return sm.get_opcodes()

    def _human_patch(self, expected_tokens: List[str], produced_tokens: List[str]):
        ops = self._align(expected_tokens, produced_tokens)
        issues = []
        for tag, i1, i2, j1, j2 in ops:
            if tag == "equal":
                continue
            if tag == "replace":
                for k in range(max(i2-i1, j2-j1)):
                    exp = expected_tokens[i1+k] if i1+k < i2 else None
                    got = produced_tokens[j1+k] if j1+k < j2 else None
                    if exp and got:
                        issues.append(("sub", exp, got))
            elif tag == "insert":
                for got in produced_tokens[j1:j2]:
                    issues.append(("ins", None, got))
            elif tag == "delete":
                for exp in expected_tokens[i1:i2]:
                    issues.append(("del", exp, None))
        return issues

    def _tip_for_issue(self, kind: str, exp: str | None, got: str | None) -> str:
        if kind == "sub" and exp and got:
            tip = self.SUB_MAP.get((exp, got), self.GENERIC_SUB)
            example = self.EXAMPLES.get(exp) or self.EXAMPLES.get(got)
            if example:
                tip += f" Example: {example}."
            return f"Replace **{got}** with **{exp}** → {tip}"
        if kind == "ins" and got:
            return f"Extra sound **{got}** → {self.GENERIC_INS}"
        if kind == "del" and exp:
            ex = self.EXAMPLES.get(exp)
            extra = f" Example: {ex}." if ex else ""
            return f"Missed **{exp}** → {self.GENERIC_DEL}{extra}"
        return "Minor mismatch. Slow down and match each sound."

    def generate_feedback(self, word: str, expected: str, attempt: str) -> str:
        exp_tokens = _tokenize_ipa(expected)
        got_tokens = _tokenize_ipa(attempt)
        issues = self._human_patch(exp_tokens, got_tokens)
        if not issues:
            return f"Great! Your pronunciation of “{word}” is very close. 👏"
        tips = [self._tip_for_issue(k, e, g) for k, e, g in issues]
        summary = (
            f"Let's improve “{word}”. Focus on the highlighted sounds below. "
            "Use the English-style hints and repeat slowly."
        )
        return f"{summary}\n" + "\n".join(tips)
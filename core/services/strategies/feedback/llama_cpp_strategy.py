from llama_cpp import Llama
from core.services.strategies.feedback.base_strategy import FeedbackStrategy

class LLamaCppFeedbackStrategy(FeedbackStrategy):
    def __init__(
        self,
        model_path: str = "models/Lucie-7B-Instruct-v1.1-q4_k_m.gguff",
        max_tokens: int = 512,
    ):
        """
        Initialize llama.cpp Llama model for local inference.
        """
        self.llm = Llama(
            model_path=model_path
        )
        self.max_tokens = max_tokens
        # Initial dummy request to warm up model
        try:
            self.generate_feedback("bonjour", "/bɔ̃ʒuʁ/", "/bonʒuʁ/")
        except Exception:
            pass

    def generate_feedback(self, word: str, expected_phonemes: str, user_phonemes: str) -> str:
        """
        Generate beginner-friendly pronunciation feedback in English and French.
        """
        messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a friendly French pronunciation coach for beginners. "
                        "Give clear, simple feedback, explain how to pronounce words using English approximations, "
                        "give one short example, and tips to improve. Do not focus only on phonetic symbols."
                    )
                },
                # Example 1
                {
                    "role": "user",
                    "content": (
                        "The user said: 'merci'\n"
                        "Expected pronunciation (IPA): /mɛʁsi/\n"
                        "User pronunciation (IPA): /mursi/\n"
                        "Identify any pronunciation mistakes and give concise, beginner-friendly feedback "
                        "using English approximations, with one example and tips to improve. Only provide the feedback text."
                    )
                },
                {
                    "role": "assistant",
                    "content": (
                        "Good attempt! In 'merci', the first vowel should sound like 'eh' in 'bed' (/ɛ/), "
                        "but you made it closer to 'oo' (/u/). Try 'mehr-see' instead of 'moor-see'. "
                        "Tip: open your mouth slightly more for the 'eh' sound."
                    )
                },
                # Example 2
                {
                    "role": "user",
                    "content": (
                        "The user said: 'bonjour'\n"
                        "Expected pronunciation (IPA): /bɔ̃ʒuʁ/\n"
                        "User pronunciation (IPA): /bonʒuʁ/\n"
                        "Identify any pronunciation mistakes and give concise, beginner-friendly feedback "
                        "using English approximations, with one example and tips to improve. Only provide the feedback text."
                    )
                },
                {
                    "role": "assistant",
                    "content": (
                        "Nice try! In 'bonjour', the 'on' is nasal (/ɔ̃/), but you pronounced it like a normal 'on'. "
                        "Think of 'bohn' but let the sound come through your nose: 'bõn-zhoor'. "
                        "Tip: practice by humming while saying 'on'."
                    )
                },
                # Actual user input
                {
                    "role": "user",
                    "content": (
                        f"The user said: '{word}'\n"
                        f"Expected pronunciation (IPA): {expected_phonemes}\n"
                        f"User pronunciation (IPA): {user_phonemes}\n"
                        f"Identify any pronunciation mistakes and give concise, beginner-friendly feedback "
                        f"using English approximations, with one example and tips to improve. Only provide the feedback text."
                    )
                }
            ]

        # Run chat completion
        response = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=self.max_tokens,
        )
        # Extract the text safely
        feedback_text = response["choices"][0]["message"]["content"].strip()
        return feedback_text
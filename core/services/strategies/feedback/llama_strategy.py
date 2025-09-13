import torch
from transformers import pipeline
from core.services.strategies.feedback.base_strategy import FeedbackStrategy

class LlamaFeedbackStrategy(FeedbackStrategy):
    def __init__(self, model_name="meta-llama/Llama-3.2-3B-Instruct"):
        self.generator = pipeline(
            "text-generation",
            model=model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        # Initial dummy request to warm up model
        try:
            self.generate_feedback("bonjour", "/bɔ̃ʒuʁ/", "/bonʒuʁ/")
        except Exception:
            pass

    def generate_feedback(self, word: str, expected_phonemes: str, user_phonemes: str) -> str:
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

        outputs = self.generator(messages, max_new_tokens=200)

        # Extract from Hugging Face pipeline output
        generated_text = outputs[0]["generated_text"][-1]['content']

        return generated_text.strip()
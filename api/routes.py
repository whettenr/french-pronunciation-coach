from fastapi import APIRouter, Query, UploadFile, File, Form
from pathlib import Path
from core.services.phonemizer_service import PhonemizerService
from core.services.speech_service import SpeechService
from core.services.scoring_service import ScoringService
from core.services.feedback_service import FeedbackService
from core.services.tts_service import TTSService
from fastapi.responses import FileResponse
import time
import json

router = APIRouter()

# Load configuration
with open('config.json') as f:
    config = json.load(f)

# Initialize feedback service based on config
feedback_strategy = config['feedback_strategy']
if feedback_strategy == 'llama-cpp':
    from core.services.strategies.feedback.llama_cpp_strategy import LLamaCppFeedbackStrategy
    feedback_instance = LLamaCppFeedbackStrategy(config['feedback_model'])
elif feedback_strategy == 'llama':
    from core.services.strategies.feedback.llama_strategy import LlamaFeedbackStrategy
    feedback_instance = LlamaFeedbackStrategy()
elif feedback_strategy == 'rb':
    from core.services.strategies.feedback.rb_strategy import RuleBasedFeedbackStrategy
    feedback_instance = RuleBasedFeedbackStrategy()
else:
    raise ValueError(f"Unknown feedback strategy: {feedback_strategy}")

llm_feedback_service = FeedbackService(feedback_instance)

# Initialize TTS service based on config
tts_strategy = config['tts_strategy']
if tts_strategy == 'hf':
    from core.services.strategies.tts.hf_strategy import HuggingStrategy
    tts_instance = HuggingStrategy(config.get('tts_model', 'facebook/mms-tts-fra'))
elif tts_strategy == 'coqui':
    from core.services.strategies.tts.coqui_strategy import CoquiTTSStrategy
    tts_instance = CoquiTTSStrategy()
elif tts_strategy == 'kyutai':
    from core.services.strategies.tts.kyutai_strategy import KyutaiTTSStrategy
    tts_instance = KyutaiTTSStrategy()
else:
    raise ValueError(f"Unknown TTS strategy: {tts_strategy}")

tts_service = TTSService(tts_instance)

# Initialize other services
speech_service = SpeechService()
phonemizer_service = PhonemizerService()
scoring_service = ScoringService()


# Text → IPA
@router.get("/ipa")
async def get_ipa(word: str):
    ipa = speech_service.get_ipa(word)
    return {"word": word, "ipa": ipa}


# IPA scoring
@router.get("/score")
async def get_score(word: str, attempt: str = Query(...)):
    correct_ipa = speech_service.get_ipa(word)
    score = scoring_service.score(correct_ipa, attempt)
    return {
        "word": word,
        "correct_ipa": correct_ipa,
        "your_attempt": attempt,
        "score": round(score, 2)
    }


# Audio → phonemes
@router.post("/audio-phonemes")
async def audio_to_phonemes(file: UploadFile = File(...)):
    save_path = phonemizer_service.save_audio(file, Path("temp_audio"))
    phonemes = phonemizer_service.audio_to_phonemes(save_path)
    return {"phonemes": phonemes}



@router.post("/audio-score")
async def score_audio_basic(
    text: str = Form(...),
    file: UploadFile = File(...)
):
    save_path = phonemizer_service.save_audio(file, Path("temp_audio"))

    correct_ipa = speech_service.get_ipa(text)
    attempt_ipa = phonemizer_service.audio_to_phonemes(save_path)
    score = scoring_service.score(correct_ipa, attempt_ipa)

    return {
        "text": text,
        "correct_ipa": correct_ipa,
        "attempt_ipa": attempt_ipa,
        "score": round(score, 2)
    }



@router.post("/llm-feedback")
async def llm_feedback(
    text: str = Form(...),
    correct_ipa: str = Form(...),
    attempt_ipa: str = Form(...),
    score: float = Form(...)
):
    time_start = time.time()
    if score == 1:
        return {"feedback": "Perfect pronunciation! Well done!"}
    feedback = llm_feedback_service.get_feedback(
        word=text,
        expected_phonemes=correct_ipa,
        user_phonemes=attempt_ipa
    )
    time_end = time.time()
    print(f"LLM feedback generation took {time_end - time_start:.2f} seconds")
    return {"feedback": feedback}




@router.post("/tts")
async def tts_endpoint(text: str = Form(...)):
    start_time = time.time()
    path = tts_service.synthesize(text)


    elapsed_time = time.time() - start_time
    print(f"TTS generation took {elapsed_time:.2f} seconds")
    return FileResponse(path, media_type="audio/wav", filename=str(path))
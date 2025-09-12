# services/strategies/tts/kyutai_strategy.py
import tempfile
import torch
import sphn
import numpy as np
from moshi.models.loaders import CheckpointInfo
from moshi.models.tts import DEFAULT_DSM_TTS_REPO, TTSModel
from core.services.strategies.tts.base_strategy import TTSSynthesisStrategy

class KyutaiTTSStrategy(TTSSynthesisStrategy):
    def __init__(self, device="mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"):
        print("Loading Kyutai TTS model...")
        print(DEFAULT_DSM_TTS_REPO)
        checkpoint_info = CheckpointInfo.from_hf_repo(DEFAULT_DSM_TTS_REPO)
        self.model = TTSModel.from_checkpoint_info(
            checkpoint_info, n_q=32, temp=0.6, device=device
        )
        voice_path = self.model.get_voice_path("cml-tts/fr/10087_11650_000028-0002.wav")
        self.condition_attributes = self.model.make_condition_attributes([voice_path], cfg_coef=2.0)
        print("TTS model loaded!")

    def synthesize(self, text: str) -> str:
        entries = self.model.prepare_script([text], padding_between=1)
        result = self.model.generate([entries], [self.condition_attributes])

        with self.model.mimi.streaming(1), torch.no_grad():
            pcms = []
            for frame in result.frames[self.model.delay_steps:]:
                pcm = self.model.mimi.decode(frame[:, 1:, :]).cpu().numpy()
                pcms.append(pcm[0, 0])
            pcm = np.concatenate(pcms, axis=-1)

        tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sphn.write_wav(tmp_file.name, pcm, self.model.mimi.sample_rate)
        tmp_file.flush()
        return tmp_file.name
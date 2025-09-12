🎙️ French Pronunciation App

**Note:** This project is in **early stage development**. Your contributions and feedback are highly appreciated to help make it better!

French Pronunciation App helps learners practice and improve their French pronunciation through phoneme recognition, text-to-speech synthesis, and AI-powered feedback.

It provides:
• Phoneme-level analysis
• Beginner-friendly feedback with examples
• Basic pronunciation scoring
• Interactive practice via a web interface

⸻

## Table of Contents
- [Features](#-features)
- [Requirements](#-requirements)
- [Setup](#️-setup)
- [Configuration](#-configuration)
- [Run the App](#-run-the-app)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)

⸻

✨ Features
• Phoneme Recognition → Detects and analyzes French phonemes from user speech
• Personalized Feedback → AI compares expected vs. spoken phonemes and explains mistakes in simple English
• Basic Scoring → Uses Levenshtein distance to quantify accuracy (⚠️ very basic, future improvements needed)
• Text-to-Speech (TTS) → Choose from Hugging Face, Coqui, or Kyutai models
• Web Frontend → User-friendly, interactive practice interface
• Cross-Browser Support → Works on Firefox and Chrome ✅, not yet supported on Safari ❌

⸻

📦 Requirements
• Python 3.11 (recommended)
• FFmpeg (for audio format conversion)

### Installing FFmpeg
• macOS (Homebrew):

```
brew install ffmpeg
```

• Ubuntu/Debian:

```
sudo apt update && sudo apt install ffmpeg
```

• Windows (Chocolatey):

```
choco install ffmpeg
```

• Or download from the FFmpeg website and add the bin folder to your PATH.

⸻

⚙️ Setup
1. Create a virtual environment

```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Create the models directory

```
mkdir models
```

4. Download language models (choose one or more):
• Lucie-7B → French-optimized (recommended)

```
huggingface-cli download OpenLLM-France/Lucie-7B-Instruct-v1.1-gguf Lucie-7B-Instruct-v1.1-q4_k_m.gguf --local-dir models --local-dir-use-symlinks False
```

• Mistral-7B → General-purpose, strong all-around model

```
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q5_K_M.gguf --local-dir models --local-dir-use-symlinks False
```

• Llama-3.2-3B → Lightweight, efficient model

```
huggingface-cli download unsloth/Llama-3.2-3B-Instruct-GGUF Llama-3.2-3B-Instruct-Q5_K_S.gguf --local-dir models --local-dir-use-symlinks False
```

⸻

🔧 Configuration

The app uses a config.json file to select strategies and models.

### Feedback Strategies
• cpp → Runs on llama.cpp with GGUF models ⚡ (recommended for speed and memory efficiency)
• llama → Standard Hugging Face Llama backend
• rb → Rule-based fallback feedback

### TTS Strategies
• hf → Hugging Face models
• facebook/mms-tts-fra → ⚡ Much faster, recommended for interactive use
• coqui → Coqui TTS
• kyutai → 🎵 Higher quality and more natural speech, but slower than Hugging Face

### Example config.json

```json
{
  "feedback_strategy": "cpp",
  "tts_strategy": "hf",
  "feedback_model": "models/Lucie-7B-Instruct-v1.1-q4_k_m.gguf",
  "tts_model": "facebook/mms-tts-fra"
}
```

📌 Notes:
• cpp = llama.cpp → best for fast, efficient inference with GGUF models.
• Recommended models: Lucie-7B (French-focused) or Mistral-7B (general-purpose).
• TTS trade-off: facebook/mms-tts-fra (fast) vs Kyutai (better quality, slower).
• First LLM inference may be slower due to model loading.

⸻

🚀 Run the App

```
python app.py
```

Open in your browser:
👉 http://localhost:8000

⚠️ Supported browsers: Firefox and Chrome ✅ | Safari ❌ (not supported yet).

⸻

📂 Project Structure
• app.py → Main FastAPI app
• api/ → API routes and endpoints
• core/ → Core logic: phoneme recognition, scoring, feedback, TTS
• frontend/ → Web interface (HTML, JS, CSS)
• models/ → Local directory for downloaded models

⸻

🤝 Contributing

Welcome to the French Pronunciation App community! This project is in its early stages, and every contribution counts—no matter how big or small. Whether you want to improve the scoring system, add new TTS or feedback strategies, enhance the frontend, fix bugs, or optimize performance, your help is invaluable.

Feel free to submit a Pull Request or open an Issue anytime. Together, we can build a fantastic tool for French learners. Thank you for being part of this journey!

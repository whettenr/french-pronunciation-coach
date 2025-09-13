# 🎙️ French Pronunciation App

Welcome to the **French Pronunciation App**! This tool helps learners improve their French pronunciation using phoneme recognition, text-to-speech synthesis, and AI-powered feedback.

---

## 🚀 Overview

This app provides:

- **Phoneme Recognition**: Detects and analyzes French phonemes from user speech.
- **Personalized Feedback**: AI compares expected vs. spoken phonemes and explains mistakes in simple English.
- **Basic Scoring**: Uses Levenshtein distance to quantify pronunciation accuracy.
- **Text-to-Speech (TTS)**: Supports Hugging Face, Coqui, and Kyutai models.
- **Interactive Web Interface**: User-friendly and engaging practice environment.
- **Cross-Browser Support**: Works on Firefox and Chrome (Safari not yet supported).

---

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Setup](#-setup)
- [Configuration](#-configuration)
- [Running the App](#-running-the-app)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **Phoneme Recognition**: Analyze French phonemes from speech input.
- **AI-Driven Feedback**: Clear, beginner-friendly explanations of pronunciation errors.
- **Pronunciation Scoring**: Simple scoring based on phoneme similarity.
- **Multiple TTS Options**: Choose from fast or high-quality speech synthesis models.
- **Web Frontend**: Accessible and interactive practice interface.
- **Browser Compatibility**: Tested on Firefox and Chrome.

---

## 📦 Requirements

- **Python 3.11** (recommended)
- **FFmpeg** (for audio format conversion)

### Installing FFmpeg

- **macOS (Homebrew):**

  ```bash
  brew install ffmpeg
  ```

- **Ubuntu/Debian:**

  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```

- **Windows (Chocolatey):**

  ```bash
  choco install ffmpeg
  ```

- Or download directly from the [FFmpeg website](https://ffmpeg.org/) and add the `bin` folder to your system PATH.

---

## ⚙️ Setup

0. **Clone the repository**

  ```bash
  git clone https://github.com/othman-istaiteh/french-pronunciation-coach.git
  cd french-pronunciation-coach
  ```

1. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create the models directory**

   ```bash
   mkdir models
   ```

4. **Download language models** (choose one or more):

   - **Lucie-7B** (French-optimized, recommended):

     ```bash
     huggingface-cli download OpenLLM-France/Lucie-7B-Instruct-v1.1-gguf Lucie-7B-Instruct-v1.1-q4_k_m.gguf --local-dir models --local-dir-use-symlinks False
     ```

   - **Mistral-7B** (General-purpose, strong all-around):

     ```bash
     huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q5_K_M.gguf --local-dir models --local-dir-use-symlinks False
     ```

   - **Llama-3.2-3B** (Lightweight and efficient):

     ```bash
     huggingface-cli download unsloth/Llama-3.2-3B-Instruct-GGUF Llama-3.2-3B-Instruct-Q5_K_S.gguf --local-dir models --local-dir-use-symlinks False
     ```

---

## 🔧 Configuration

The app uses a `config.json` file to select feedback and TTS strategies as well as models.

### Feedback Strategies

- `llama-cpp`: Runs on llama.cpp with GGUF models (⚡ recommended for speed and memory efficiency)
- `llama`: Standard Hugging Face Llama backend
- `rb`: Rule-based fallback feedback

### TTS Strategies

- `hf`: Hugging Face models
- `facebook/mms-tts-fra`: ⚡ Much faster, recommended for interactive use
- `coqui`: Coqui TTS
- `kyutai`: 🎵 Higher quality and more natural speech, but slower than Hugging Face

### Example `config.json`

```json
{
  "feedback_strategy": "llama-cpp",
  "tts_strategy": "hf",
  "feedback_model": "models/Lucie-7B-Instruct-v1.1-q4_k_m.gguf",
  "tts_model": "facebook/mms-tts-fra"
}
```

> **Notes:**
> - `llama-cpp` offers fast and efficient inference with GGUF models.
> - Recommended feedback models: Lucie-7B (French-focused) or Mistral-7B (general-purpose).
> - TTS trade-offs: `facebook/mms-tts-fra` is faster; `kyutai` provides better quality but is slower.
> - The first LLM inference may take longer due to model loading.

---

## ▶️ Running the App

Start the app with:

```bash
python app.py
```

Then open your browser and navigate to:

👉 [http://localhost:8000](http://localhost:8000)

> **Supported browsers:** Firefox and Chrome ✅  
> Safari is currently **not supported** ❌

---

## 📂 Project Structure

```
French Pronunciation App/
├── app.py                 # Main FastAPI application
├── api/                   # API routes and endpoints
├── core/                  # Core logic: phoneme recognition, scoring, feedback, TTS
├── frontend/              # Web interface (HTML, JS, CSS)
└── models/                # Directory for downloaded models
```

---

## 🤝 Contributing

We welcome contributions! Whether you want to improve scoring, add new TTS or feedback strategies, enhance the frontend, fix bugs, or optimize performance, your help is invaluable.

- Fork the repository
- Create a feature branch
- Submit a Pull Request or open an Issue to discuss your ideas

Thank you for helping make this app better for French learners worldwide!

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

Thank you for being part of this journey!  
Happy learning and bon courage!

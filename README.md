# French Pronunciation App

This application helps users improve their French pronunciation through interactive practice, phoneme recognition, and AI-powered personalized feedback. It provides phonetic analysis, text-to-speech synthesis, speech recognition, and basic scoring using Levenshtein distance to guide learners in mastering French sounds.

## Requirements

- Python 3.11 (recommended for optimal performance)
- FFmpeg (for audio format conversion)

### Installing FFmpeg

FFmpeg is required for processing audio files uploaded from web browsers.

- **macOS** (with Homebrew):
  ```
  brew install ffmpeg
  ```

- **Ubuntu/Debian**:
  ```
  sudo apt update
  sudo apt install ffmpeg
  ```

- **Windows** (with Chocolatey):
  ```
  choco install ffmpeg
  ```

- Or download from the [FFmpeg website](https://ffmpeg.org/download.html) and add the `bin` directory to your PATH.

## Setup Instructions

1. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create the models directory:
   ```
   mkdir models
   ```

4. Download the language models (choose one or more based on your needs):
   - **Mistral-7B** (General-purpose instruction model):
     ```
     huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q5_K_M.gguf --local-dir models --local-dir-use-symlinks False
     ```
   - **Llama-3.2-3B** (Efficient 3B parameter model):
     ```
     huggingface-cli download unsloth/Llama-3.2-3B-Instruct-GGUF Llama-3.2-3B-Instruct-Q5_K_S.gguf --local-dir models --local-dir-use-symlinks False
     ```
   - **Lucie-7B** (French-optimized model):
     ```
     huggingface-cli download OpenLLM-France/Lucie-7B-Instruct-v1.1-gguf Lucie-7B-Instruct-v1.1-q4_k_m.gguf --local-dir models --local-dir-use-symlinks False
     ```

## Configuration

The application uses a JSON configuration file (`config.json`) to select strategies and models. Create or edit `config.json` in the root directory.

### Available Strategies

- **Feedback Strategies** (for AI-powered personalized pronunciation feedback):
  - `llama-cpp`: Optimized for speed and performance balance using llama.cpp (recommended)
  - `llama`: Standard Llama-based feedback
  - `rb`: Rule-based feedback

- **TTS Strategies** (for text-to-speech synthesis):
  - `hf`: Hugging Face models (recommended for French: `facebook/mms-tts-fra`)
  - `coqui`: Coqui TTS
  - `kyutai`: Kyutai TTS

### Example Configuration

```json
{
  "feedback_strategy": "llama-cpp",
  "tts_strategy": "hf",
  "feedback_model": "models/Lucie-7B-Instruct-v1.1-q4_k_m.gguf",
  "tts_model": "facebook/mms-tts-fra"
}
```

- If `llama-cpp` is selected for feedback, specify the model path (e.g., one of the downloaded GGUF models). Lucie-7B is recommended for French language tasks.
- For Hugging Face TTS, use `facebook/mms-tts-fra` for optimal French pronunciation.
- **Note**: The first LLM inference may be slower due to model loading and initialization.

## Running the Application

Start the app with:
```
python app.py
```

The application will launch a web server, and you can access the frontend through your browser.

## Features

- **Phoneme Recognition**: Accurate detection and analysis of French phonemes from user speech
- **Personalized Feedback**: AI-driven feedback tailored to individual pronunciation errors
- **Basic Scoring**: Pronunciation scoring based on Levenshtein distance to quantify pronunciation accuracy
- **Text-to-Speech (TTS)**: Multiple TTS strategies including Coqui, Hugging Face, and Kyutai
- **Speech Recognition**: Real-time speech input processing using Wav2Vec2 (requires FFmpeg for audio format conversion; works on Firefox and Chrome, Safari support pending)
- **Web Frontend**: User-friendly interface for interactive learning
- **Scoring Service**: Automated pronunciation evaluation and scoring

## Project Structure

- `app.py`: Main Flask application
- `api/`: API routes and endpoints
- `core/`: Core functionality including phonetics, scoring, and services
- `frontend/`: Web interface files (HTML, JS, CSS)
- `models/`: Directory for downloaded language models (not included in repo)

## Contributing

This is an ongoing collaboration project, and contributions are welcome! If you'd like to improve the app, add features, or fix issues, please feel free to submit pull requests or open issues on the repository.

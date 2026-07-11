import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
HOTKEY = os.getenv("HOTKEY", "<alt>+3")
AUDIO_FILE = os.getenv("AUDIO_FILE", "temp_speech.wav")
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))
STT_MODEL = os.getenv("STT_MODEL", "whisper-large-v3-turbo")
STT_LANGUAGE = os.getenv("STT_LANGUAGE", "ru")

def save_config(api_key, base_url, hotkey, sample_rate, stt_model="whisper-large-v3-turbo", stt_language="ru"):
    global GROQ_API_KEY, GROQ_BASE_URL, HOTKEY, SAMPLE_RATE, STT_MODEL, STT_LANGUAGE
    GROQ_API_KEY = api_key
    GROQ_BASE_URL = base_url
    HOTKEY = hotkey
    SAMPLE_RATE = sample_rate
    STT_MODEL = stt_model
    STT_LANGUAGE = stt_language
    lines = [
        f"GROQ_API_KEY={api_key}",
        f"GROQ_BASE_URL={base_url}",
        f"HOTKEY={hotkey}",
        f"SAMPLE_RATE={sample_rate}",
        "AUDIO_FILE=temp_speech.wav",
        f"STT_MODEL={stt_model}",
        f"STT_LANGUAGE={stt_language}"
    ]
    with open(".env", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
HOTKEY = os.getenv("HOTKEY", "<alt>+3")
AUDIO_FILE = os.getenv("AUDIO_FILE", "temp_speech.wav")
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))

def save_config(api_key, base_url, hotkey, sample_rate):
    global GROQ_API_KEY, GROQ_BASE_URL, HOTKEY, SAMPLE_RATE
    GROQ_API_KEY = api_key
    GROQ_BASE_URL = base_url
    HOTKEY = hotkey
    SAMPLE_RATE = sample_rate
    lines = [
        f"GROQ_API_KEY={api_key}",
        f"GROQ_BASE_URL={base_url}",
        f"HOTKEY={hotkey}",
        f"SAMPLE_RATE={sample_rate}",
        "AUDIO_FILE=temp_speech.wav"
    ]
    with open(".env", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL

class STTService:
    def __init__(self):
        self.client = OpenAI(
            base_url=GROQ_BASE_URL,
            api_key=GROQ_API_KEY
        )

    def transcribe(self, file_path):
        with open(file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                language="ru"
            )
        return transcript.text
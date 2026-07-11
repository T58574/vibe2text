import config
from openai import OpenAI

class STTService:
    def __init__(self):
        self.client = OpenAI(
            base_url=config.GROQ_BASE_URL,
            api_key=config.GROQ_API_KEY
        )

    def transcribe(self, file_path):
        with open(file_path, "rb") as audio_file:
            kwargs = {
                "model": config.STT_MODEL,
                "file": audio_file
            }
            if config.STT_LANGUAGE:
                kwargs["language"] = config.STT_LANGUAGE
                
            transcript = self.client.audio.transcriptions.create(**kwargs)
        return transcript.text
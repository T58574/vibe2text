import os
import sys
import importlib
from unittest import mock
import config

def test_config_defaults():
    with mock.patch("dotenv.load_dotenv"), mock.patch.dict(os.environ, {}, clear=True):
        importlib.reload(config)
        assert config.GROQ_API_KEY == ""
        assert config.GROQ_BASE_URL == "https://api.groq.com/openai/v1"
        assert config.HOTKEY == "<alt>+3"
        assert config.AUDIO_FILE == "temp_speech.wav"
        assert config.SAMPLE_RATE == 16000

def test_config_env_vars():
    custom_env = {
        "GROQ_API_KEY": "test_key",
        "GROQ_BASE_URL": "https://test.base.url",
        "HOTKEY": "<ctrl>+a",
        "AUDIO_FILE": "test_audio.wav",
        "SAMPLE_RATE": "44100"
    }
    with mock.patch("dotenv.load_dotenv"), mock.patch.dict(os.environ, custom_env, clear=True):
        importlib.reload(config)
        assert config.GROQ_API_KEY == "test_key"
        assert config.GROQ_BASE_URL == "https://test.base.url"
        assert config.HOTKEY == "<ctrl>+a"
        assert config.AUDIO_FILE == "test_audio.wav"
        assert config.SAMPLE_RATE == 44100

def test_save_config():
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        config.save_config("new_key", "new_url", "<alt>+4", 44100)
        assert config.GROQ_API_KEY == "new_key"
        assert config.GROQ_BASE_URL == "new_url"
        assert config.HOTKEY == "<alt>+4"
        assert config.SAMPLE_RATE == 44100
        mock_file.assert_called_once_with(".env", "w", encoding="utf-8")

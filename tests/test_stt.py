from unittest import mock
from stt import STTService

def test_stt_service():
    mock_openai_inst = mock.MagicMock()
    mock_transcription = mock.MagicMock()
    mock_transcription.text = "транскрипция"
    mock_openai_inst.audio.transcriptions.create.return_value = mock_transcription

    with mock.patch("stt.OpenAI", return_value=mock_openai_inst), \
         mock.patch("builtins.open", mock.mock_open(read_data=b"dummy_audio")):
        
        service = STTService()
        result = service.transcribe("test.wav")
        
        assert result == "транскрипция"
        mock_openai_inst.audio.transcriptions.create.assert_called_once_with(
            model="whisper-large-v3-turbo",
            file=mock.ANY,
            language="ru"
        )

from unittest import mock
import numpy as np
from audio import AudioRecorder

def test_audio_recorder():
    mock_stream = mock.MagicMock()
    mock_input_stream = mock.MagicMock(return_value=mock_stream)
    mock_sound_file = mock.MagicMock()

    with mock.patch("sounddevice.InputStream", mock_input_stream), \
         mock.patch("soundfile.SoundFile", return_value=mock_sound_file) as mock_sf_cls:
        
        recorder = AudioRecorder("test.wav", samplerate=16000)
        recorder.start()
        
        mock_input_stream.assert_called_once()
        mock_stream.start.assert_called_once()
        
        dummy_data = np.zeros((1024, 1))
        recorder.callback(dummy_data, None, None, None)
        
        recorder.stop()
        
        mock_stream.stop.assert_called_once()
        mock_stream.close.assert_called_once()
        mock_sf_cls.assert_called_once_with("test.wav", mode="w", samplerate=16000, channels=1)
        mock_sound_file.__enter__.return_value.write.assert_called_once()

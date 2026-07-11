import ui
from unittest import mock

def test_overlay_widget():
    widget = ui.OverlayWidget()
    widget.show_at_cursor()
    assert widget.x == 115
    assert widget.y == 215
    assert widget.visible is True

    # Test states and paint events
    mock_recorder = mock.MagicMock()
    mock_recorder.last_rms = 0.05
    widget.recorder = mock_recorder

    widget.set_state("recording")
    widget.paintEvent(None)

    widget.set_state("transcribing")
    widget.on_timer_tick()
    widget.paintEvent(None)

    widget.set_state("success")
    widget.paintEvent(None)

    widget.set_state("error", "какая-то ошибка")
    widget.paintEvent(None)

def test_settings_dialog():
    dialog = ui.SettingsDialog()
    assert dialog.api_key_input.text() is not None
    assert dialog.base_url_input.text() is not None
    assert dialog.model_input.text() is not None
    assert dialog.language_input.text() is not None
    
    dialog.sample_rate_input.setText("22050")
    vals = dialog.get_values()
    assert vals["sample_rate"] == 22050

    dialog.sample_rate_input.setText("invalid")
    vals = dialog.get_values()
    assert vals["sample_rate"] == 16000

    dialog.model_input.setText("new-model")
    dialog.language_input.setText("en")
    vals = dialog.get_values()
    assert vals["stt_model"] == "new-model"
    assert vals["stt_language"] == "en"

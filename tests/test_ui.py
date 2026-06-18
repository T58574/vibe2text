import ui

def test_overlay_widget():
    widget = ui.OverlayWidget()
    widget.show_at_cursor()
    assert widget.x == 115
    assert widget.y == 215
    assert widget.visible is True

def test_settings_dialog():
    dialog = ui.SettingsDialog()
    assert dialog.api_key_input.text() is not None
    assert dialog.base_url_input.text() is not None
    
    dialog.sample_rate_input.setText("22050")
    vals = dialog.get_values()
    assert vals["sample_rate"] == 22050

    dialog.sample_rate_input.setText("invalid")
    vals = dialog.get_values()
    assert vals["sample_rate"] == 16000

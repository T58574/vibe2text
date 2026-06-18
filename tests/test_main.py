from unittest import mock
import importlib
import config
importlib.reload(config)
import main

def test_dictation_app_init():
    with mock.patch("main.AudioRecorder"), \
         mock.patch("main.STTService"), \
         mock.patch("main.TextInjector"), \
         mock.patch("main.OverlayWidget"):
        app = main.DictationApp()
        assert app.is_recording is False
        
        with mock.patch.object(app.signals.toggle, "emit") as mock_emit:
            app.trigger_toggle()
            mock_emit.assert_called_once()

def test_dictation_app_toggle_flow():
    mock_recorder = mock.MagicMock()
    mock_stt = mock.MagicMock()
    mock_stt.transcribe.return_value = "hello"
    mock_injector = mock.MagicMock()
    mock_ui = mock.MagicMock()
    
    with mock.patch("main.AudioRecorder", return_value=mock_recorder), \
         mock.patch("main.STTService", return_value=mock_stt), \
         mock.patch("main.TextInjector", return_value=mock_injector), \
         mock.patch("main.OverlayWidget", return_value=mock_ui):
        
        app = main.DictationApp()
        
        app.handle_toggle()
        assert app.is_recording is True
        mock_ui.show_at_cursor.assert_called_once()
        mock_recorder.start.assert_called_once()
        
        app.handle_toggle()
        assert app.is_recording is False
        mock_ui.hide.assert_called_once()
        mock_recorder.stop.assert_called_once()
        mock_stt.transcribe.assert_called_once()
        mock_injector.inject.assert_called_once_with("hello")

def test_dictation_app_toggle_flow_empty_text():
    mock_recorder = mock.MagicMock()
    mock_stt = mock.MagicMock()
    mock_stt.transcribe.return_value = ""
    mock_injector = mock.MagicMock()
    mock_ui = mock.MagicMock()
    
    with mock.patch("main.AudioRecorder", return_value=mock_recorder), \
         mock.patch("main.STTService", return_value=mock_stt), \
         mock.patch("main.TextInjector", return_value=mock_injector), \
         mock.patch("main.OverlayWidget", return_value=mock_ui):
        
        app = main.DictationApp()
        app.is_recording = True
        app.handle_toggle()
        assert app.is_recording is False
        mock_stt.transcribe.assert_called_once()
        mock_injector.inject.assert_not_called()

def test_dictation_app_toggle_flow_stt_exception():
    mock_recorder = mock.MagicMock()
    mock_stt = mock.MagicMock()
    mock_stt.transcribe.side_effect = Exception("API error")
    mock_injector = mock.MagicMock()
    mock_ui = mock.MagicMock()
    
    with mock.patch("main.AudioRecorder", return_value=mock_recorder), \
         mock.patch("main.STTService", return_value=mock_stt), \
         mock.patch("main.TextInjector", return_value=mock_injector), \
         mock.patch("main.OverlayWidget", return_value=mock_ui):
        
        app = main.DictationApp()
        app.is_recording = True
        app.handle_toggle()
        assert app.is_recording is False
        mock_stt.transcribe.assert_called_once()
        mock_injector.inject.assert_not_called()

def test_dictation_app_run():
    with mock.patch("main.AudioRecorder"), \
         mock.patch("main.STTService"), \
         mock.patch("main.TextInjector"), \
         mock.patch("main.OverlayWidget"), \
         mock.patch("sys.exit") as mock_exit:
        app = main.DictationApp()
        app.run()
        mock_exit.assert_called_once_with(0)

def test_dictation_app_setup_tray():
    with mock.patch("main.AudioRecorder"), \
         mock.patch("main.STTService"), \
         mock.patch("main.TextInjector"), \
         mock.patch("main.OverlayWidget"):
        app = main.DictationApp()
        assert app.tray_icon is not None
        assert app.tray_menu is not None

def test_dictation_app_quit():
    with mock.patch("main.AudioRecorder"), \
         mock.patch("main.STTService"), \
         mock.patch("main.TextInjector"), \
         mock.patch("main.OverlayWidget"):
        app = main.DictationApp()
        with mock.patch.object(app.listener, "stop") as mock_stop, \
             mock.patch.object(app.app, "quit") as mock_quit:
            app.quit_app()
            mock_stop.assert_called_once()
            mock_quit.assert_called_once()

def test_dictation_app_open_settings():
    with mock.patch("main.AudioRecorder"), \
         mock.patch("main.STTService"), \
         mock.patch("main.TextInjector"), \
         mock.patch("main.OverlayWidget"):
        config.HOTKEY = "<alt>+3"
        app = main.DictationApp()
        
        mock_dialog_inst = mock.MagicMock()
        mock_dialog_inst.exec.return_value = 1
        mock_dialog_inst.get_values.return_value = {
            "api_key": "new_key",
            "base_url": "new_url",
            "hotkey": "<alt>+4",
            "sample_rate": 22050
        }
        
        mock_class = mock.MagicMock()
        mock_class.return_value = mock_dialog_inst
        mock_class.DialogCode.Accepted = 1
        
        with mock.patch("main.SettingsDialog", new=mock_class), \
             mock.patch("main.config.save_config") as mock_save, \
             mock.patch.object(app.listener, "stop") as mock_stop, \
             mock.patch.object(main.keyboard, "GlobalHotKeys") as mock_hotkeys:
            
            app.open_settings()
            
            mock_save.assert_called_once_with("new_key", "new_url", "<alt>+4", 22050)
            mock_stop.assert_called_once()
            mock_hotkeys.assert_called_once_with({"<alt>+4": app.trigger_toggle})

def test_dictation_app_open_settings_same_hotkey():
    with mock.patch("main.AudioRecorder"), \
         mock.patch("main.STTService"), \
         mock.patch("main.TextInjector"), \
         mock.patch("main.OverlayWidget"):
        config.HOTKEY = "<alt>+3"
        app = main.DictationApp()
        
        mock_dialog_inst = mock.MagicMock()
        mock_dialog_inst.exec.return_value = 1
        mock_dialog_inst.get_values.return_value = {
            "api_key": "new_key",
            "base_url": "new_url",
            "hotkey": "<alt>+3",
            "sample_rate": 22050
        }
        
        mock_class = mock.MagicMock()
        mock_class.return_value = mock_dialog_inst
        mock_class.DialogCode.Accepted = 1
        
        with mock.patch("main.SettingsDialog", new=mock_class), \
             mock.patch("main.config.save_config") as mock_save, \
             mock.patch.object(app.listener, "stop") as mock_stop, \
             mock.patch.object(main.keyboard, "GlobalHotKeys") as mock_hotkeys:
            
            app.open_settings()
            
            mock_save.assert_called_once_with("new_key", "new_url", "<alt>+3", 22050)
            mock_stop.assert_not_called()
            mock_hotkeys.assert_not_called()

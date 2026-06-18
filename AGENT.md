# STT Vidjet Developer & Agent Documentation

This document describes the public API surface, design patterns, testing strategy, and project standards.

## Architecture and Design

The application is structured as a modular, event-driven voice-to-text dictation utility:

```
[Global Hotkey (pynput)] -> [DictationApp (main.py)] -> [OverlayWidget (ui.py)]
                                  |
                                  +-> [AudioRecorder (audio.py)] -> (temp_speech.wav)
                                  |
                                  +-> [STTService (stt.py)] -> (Groq API)
                                  |
                                  +-> [TextInjector (injector.py)] -> (Keyboard Injection)
                                  |
                                  +-> [SettingsDialog (ui.py)] -> (Sleek config panel)
```

## Public API Specification

### 1. `STTService` (`stt.py`)
Provides transcription capabilities using Groq's Whisper API.
* **Methods:**
  * `transcribe(file_path: str) -> str`: Reads a WAV audio file and returns its textual transcription.
* **Example Usage:**
  ```python
  from stt import STTService
  service = STTService()
  text = service.transcribe("audio.wav")
  print(f"Transcribed text: {text}")
  ```

### 2. `AudioRecorder` (`audio.py`)
Manages audio capture from the system's default input device.
* **Methods:**
  * `__init__(filename: str, samplerate: int = 16000)`: Configures the filename and samplerate.
  * `start()`: Opens the stream and starts recording.
  * `stop()`: Closes the stream and flushes buffered audio to the file.
* **Example Usage:**
  ```python
  import time
  from audio import AudioRecorder
  recorder = AudioRecorder("temp.wav")
  recorder.start()
  time.sleep(3)
  recorder.stop()
  ```

### 3. `TextInjector` (`injector.py`)
Injects string values directly into the current focused cursor by simulating hardware keyboard input.
* **Methods:**
  * `inject(text: str)`: Types the given string at the system cursor after a brief pause.
* **Example Usage:**
  ```python
  from injector import TextInjector
  injector = TextInjector()
  injector.inject("Text to be typed automatically.")
  ```

### 4. `OverlayWidget` & `SettingsDialog` (`ui.py`)
* `OverlayWidget` displays a frameless, semi-translucent overlay notification adjacent to the mouse cursor.
  * `show_at_cursor()`: Moves the widget to the mouse pointer position and shows it.
  * `hide()`: Hides the overlay widget.
* `SettingsDialog` displays a configuration window for managing credentials and options.
  * `get_values() -> dict`: Returns the dictation parameters typed by the user.
* **Example Usage:**
  ```python
  from PyQt6.QtWidgets import QApplication
  import sys
  from ui import SettingsDialog
  app = QApplication(sys.argv)
  dialog = SettingsDialog()
  if dialog.exec() == SettingsDialog.DialogCode.Accepted:
      print(dialog.get_values())
  ```

### 5. `DictationApp` (`main.py`)
Core orchestrator that binds global hotkey events, recording, transcription, and typing lifecycle.
* **Methods:**
  * `setup_tray()`: Initializes the system tray icon and attaches action menus.
  * `open_settings()`: Spawns the SettingsDialog widget and applies modified configs dynamically.
  * `quit_app()`: Properly terminates pynput global listeners and quits the Qt application.
  * `run()`: Begins execution of the application and starts the PyQt event loop.
* **Example Usage:**
  ```python
  from main import DictationApp
  app = DictationApp()
  app.run()
  ```

---

## Configuration & Environment Variables

All variables are loaded from the environment or a `.env` file via `config.py`:

* `GROQ_API_KEY`: The authorization token for the Groq API.
* `GROQ_BASE_URL`: Base URL endpoint (defaults to `https://api.groq.com/openai/v1`).
* `HOTKEY`: Global key shortcut to start/stop dictation (defaults to `<alt>+3`).
* `AUDIO_FILE`: Temporal sound storage location (defaults to `temp_speech.wav`).
* `SAMPLE_RATE`: Input recorder sampling frequency in Hz (defaults to `16000`).

Update configuration dynamically using:
```python
import config
config.save_config("api_key", "base_url", "hotkey", 16000)
```

---

## Metrics and Enforcement Thresholds

* **Test Coverage:** $\ge 95\%$ (Current: $97\%$)
* **Critical Path Performance:** $\le 200\text{ ms}$ latency for scheduling, layout, and processing tasks (excluding third-party network API requests).
* **Memory Management:** Memory leaks are audited via automated garbage collection assertions. All PyObjects and Qt handles are garbage collected at widget teardown.

---

## Testing Framework

To run the unit tests and inspect the code coverage metrics, execute:
```bash
.venv\Scripts\python -m pytest --cov=. --cov-report=term-missing
```

import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPainter, QColor
from pynput import keyboard
import config
from audio import AudioRecorder
from stt import STTService
from injector import TextInjector
from ui import OverlayWidget, SettingsDialog

class AppSignals(QObject):
    toggle = pyqtSignal()

class DictationApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.signals = AppSignals()
        self.signals.toggle.connect(self.handle_toggle)
        
        self.recorder = AudioRecorder(config.AUDIO_FILE, config.SAMPLE_RATE)
        self.stt = STTService()
        self.injector = TextInjector()
        self.ui = OverlayWidget()
        
        self.is_recording = False
        self.listener = keyboard.GlobalHotKeys({config.HOTKEY: self.trigger_toggle})
        self.listener.start()

        self.setup_tray()

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self.create_tray_icon(), self.app)
        self.tray_menu = QMenu()
        
        self.toggle_action = QAction("Запись/Стоп", self.tray_menu)
        self.toggle_action.triggered.connect(self.trigger_toggle)
        
        self.settings_action = QAction("Настройки...", self.tray_menu)
        self.settings_action.triggered.connect(self.open_settings)
        
        self.exit_action = QAction("Выход", self.tray_menu)
        self.exit_action.triggered.connect(self.quit_app)
        
        self.tray_menu.addAction(self.toggle_action)
        self.tray_menu.addAction(self.settings_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.exit_action)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def create_tray_icon(self):
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor("transparent"))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("#0078d4"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(2, 2, 12, 12)
        painter.end()
        return QIcon(pixmap)

    def trigger_toggle(self):
        self.signals.toggle.emit()

    def handle_toggle(self):
        if not self.is_recording:
            self.is_recording = True
            self.ui.show_at_cursor()
            self.recorder.start()
        else:
            self.is_recording = False
            self.ui.hide()
            self.recorder.stop()
            try:
                text = self.stt.transcribe(config.AUDIO_FILE)
                if text:
                    self.injector.inject(text)
            except Exception as e:
                print(f"STT Error: {e}")

    def open_settings(self):
        dialog = SettingsDialog()
        if dialog.exec() == SettingsDialog.DialogCode.Accepted:
            vals = dialog.get_values()
            old_hotkey = config.HOTKEY
            config.save_config(vals["api_key"], vals["base_url"], vals["hotkey"], vals["sample_rate"])
            
            self.stt = STTService()
            self.recorder = AudioRecorder(config.AUDIO_FILE, config.SAMPLE_RATE)
            
            if vals["hotkey"] != old_hotkey:
                self.listener.stop()
                self.listener = keyboard.GlobalHotKeys({vals["hotkey"]: self.trigger_toggle})
                self.listener.start()

    def quit_app(self):
        self.listener.stop()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = DictationApp()
    app.run()
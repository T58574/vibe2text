from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDialog, QLineEdit, QPushButton, QFormLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon, QPixmap, QPainter, QColor
import config

class OverlayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.state = "recording"
        self.recorder = None
        self.anim_angle = 0
        self.timer = None
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(16, 12, 16, 24)
        
        self.label = QLabel("🎤 Запись... Нажмите Alt+3 для отправки")
        self.label.setStyleSheet("color: #ffffff; font-family: 'Segoe UI', sans-serif; font-size: 13px; font-weight: 500;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.adjustSize()
        
        from PyQt6.QtCore import QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_tick)

    def set_state(self, state, extra_text=""):
        self.state = state
        hotkey_str = config.HOTKEY.upper()
        if state == "recording":
            self.label.setText(f"🎤 Запись... Нажмите {hotkey_str} для отправки")
            self.layout.setContentsMargins(16, 12, 16, 24)
            self.timer.start(33)
        elif state == "transcribing":
            self.label.setText("⚡ Распознавание...")
            self.layout.setContentsMargins(16, 12, 16, 24)
            self.timer.start(33)
        elif state == "success":
            self.label.setText("✅ Готово!")
            self.layout.setContentsMargins(16, 12, 16, 12)
            self.timer.stop()
        elif state == "error":
            err_msg = extra_text if extra_text else "ошибка"
            self.label.setText(f"❌ Ошибка: {err_msg}")
            self.layout.setContentsMargins(16, 12, 16, 12)
            self.timer.stop()
        
        self.adjustSize()
        self.update()

    def on_timer_tick(self):
        if self.state == "transcribing":
            self.anim_angle = (self.anim_angle + 12) % 360
        self.update()

    def show_at_cursor(self):
        pos = QCursor.pos()
        self.move(pos.x() + 15, pos.y() + 15)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(QColor(18, 18, 18, 230))
        
        if self.state == "recording":
            border_color = QColor(0, 120, 212, 220)
        elif self.state == "transcribing":
            border_color = QColor(255, 185, 0, 220)
        elif self.state == "success":
            border_color = QColor(16, 124, 65, 220)
        else:
            border_color = QColor(232, 17, 35, 220)
            
        painter.setPen(border_color)
        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 10, 10)
        
        if self.state == "recording":
            rms = self.recorder.last_rms if self.recorder else 0.0
            level = min(max(rms * 150.0, 1.0), 16.0)
            center_x = rect.width() / 2.0
            base_y = rect.height() - 10.0
            bar_width = 3.0
            bar_gap = 4.0
            
            heights = [level * 0.4, level * 0.7, level * 1.0, level * 0.7, level * 0.4]
            heights = [max(h, 2.0) for h in heights]
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(0, 150, 255, 255))
            
            for i, h in enumerate(heights):
                offset = (i - 2) * (bar_width + bar_gap)
                x = int(center_x + offset - bar_width / 2.0)
                y = int(base_y - h)
                painter.drawRoundedRect(x, y, int(bar_width), int(h), 1.5, 1.5)
                
        elif self.state == "transcribing":
            center_x = rect.width() / 2.0
            center_y = rect.height() - 10.0
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.save()
            painter.translate(center_x, center_y)
            painter.rotate(self.anim_angle)
            for i in range(8):
                opacity = int(255 * (i + 1) / 8)
                painter.setBrush(QColor(255, 185, 0, opacity))
                painter.drawEllipse(0, -6, 2, 2)
                painter.rotate(45)
            painter.restore()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Настройки STT Vidjet")
        self.setFixedSize(450, 340)
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 13px;
            }
            QLineEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 6px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
            QPushButton {
                font-size: 13px;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton#saveBtn {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
            }
            QPushButton#saveBtn:hover {
                background-color: #005a9e;
            }
            QPushButton#cancelBtn {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #444444;
            }
            QPushButton#cancelBtn:hover {
                background-color: #3d3d3d;
            }
        """)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setText(config.GROQ_API_KEY)

        self.base_url_input = QLineEdit()
        self.base_url_input.setText(config.GROQ_BASE_URL)

        self.hotkey_input = QLineEdit()
        self.hotkey_input.setText(config.HOTKEY)

        self.sample_rate_input = QLineEdit()
        self.sample_rate_input.setText(str(config.SAMPLE_RATE))

        self.model_input = QLineEdit()
        self.model_input.setText(config.STT_MODEL)

        self.language_input = QLineEdit()
        self.language_input.setText(config.STT_LANGUAGE)

        form_layout.addRow(QLabel("API Ключ Groq:"), self.api_key_input)
        form_layout.addRow(QLabel("Base URL:"), self.base_url_input)
        form_layout.addRow(QLabel("Горячая клавиша:"), self.hotkey_input)
        form_layout.addRow(QLabel("Sample Rate (Гц):"), self.sample_rate_input)
        form_layout.addRow(QLabel("Модель STT:"), self.model_input)
        form_layout.addRow(QLabel("Язык (ru/en/...):"), self.language_input)

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def get_values(self):
        try:
            sr = int(self.sample_rate_input.text())
        except ValueError:
            sr = 16000
        return {
            "api_key": self.api_key_input.text(),
            "base_url": self.base_url_input.text(),
            "hotkey": self.hotkey_input.text(),
            "sample_rate": sr,
            "stt_model": self.model_input.text(),
            "stt_language": self.language_input.text()
        }
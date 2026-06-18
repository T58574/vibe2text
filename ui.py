from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDialog, QLineEdit, QPushButton, QFormLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon, QPixmap, QPainter, QColor
import config

class OverlayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        self.label = QLabel("🎤 Запись... Нажмите Alt+3 для отправки")
        self.label.setStyleSheet("""
            background-color: #1e1e1e;
            color: #ffffff;
            border: 2px solid #0078d4;
            border-radius: 6px;
            padding: 8px 12px;
            font-family: 'Segoe UI', sans-serif;
            font-size: 12px;
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.adjustSize()

    def show_at_cursor(self):
        pos = QCursor.pos()
        self.move(pos.x() + 15, pos.y() + 15)
        self.show()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Настройки STT Vidjet")
        self.setFixedSize(450, 280)
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

        form_layout.addRow(QLabel("API Ключ Groq:"), self.api_key_input)
        form_layout.addRow(QLabel("Base URL:"), self.base_url_input)
        form_layout.addRow(QLabel("Горячая клавиша:"), self.hotkey_input)
        form_layout.addRow(QLabel("Sample Rate (Гц):"), self.sample_rate_input)

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
            "sample_rate": sr
        }
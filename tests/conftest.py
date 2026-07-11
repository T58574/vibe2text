import sys
from unittest import mock

class MockModule:
    def __init__(self, name, custom_attrs=None):
        self.__name__ = name
        if custom_attrs:
            for k, v in custom_attrs.items():
                setattr(self, k, v)
    def __getattr__(self, item):
        m = mock.MagicMock()
        m.DialogCode.Accepted = 1
        m.DialogCode.Rejected = 0
        return m

class MockQWidget:
    def __init__(self, *args, **kwargs):
        self.visible = False
        self.x = 0
        self.y = 0
    def setWindowFlags(self, flags):
        self.flags = flags
    def setAttribute(self, attr):
        self.attr = attr
    def setLayout(self, layout):
        self.layout = layout
    def adjustSize(self):
        pass
    def move(self, x, y):
        self.x = x
        self.y = y
    def show(self):
        self.visible = True
    def hide(self):
        self.visible = False
    def setWindowTitle(self, title):
        pass
    def setFixedSize(self, w, h):
        pass
    def setStyleSheet(self, style):
        pass
    def update(self):
        pass
    def rect(self):
        m = mock.MagicMock()
        m.width.return_value = 100
        m.height.return_value = 50
        m.adjusted.return_value = m
        return m

class MockQApplication:
    def __init__(self, argv):
        pass
    def exec(self):
        return 0
    def quit(self):
        pass

class MockQObject:
    def __init__(self, *args, **kwargs):
        pass

class MockSignal:
    def __init__(self):
        self.slots = []
    def connect(self, slot):
        self.slots.append(slot)
    def emit(self, *args, **kwargs):
        for slot in self.slots:
            try:
                slot(*args, **kwargs)
            except TypeError:
                slot()

def mock_pyqt_signal(*args, **kwargs):
    return MockSignal()

class MockQt:
    class WindowType:
        FramelessWindowHint = 1
        WindowStaysOnTopHint = 2
        Tool = 4
    class WidgetAttribute:
        WA_TranslucentBackground = 8
    class PenStyle:
        NoPen = 0
    class GlobalColor:
        transparent = 0
    class AlignmentFlag:
        AlignCenter = 132

class MockQThread(MockQObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def start(self):
        self.run()
    def run(self):
        pass
    def deleteLater(self, *args, **kwargs):
        pass

class MockQTimer(MockQObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timeout = MockSignal()
    def start(self, msec=None):
        self.timeout.emit()
    def stop(self):
        pass
    @staticmethod
    def singleShot(msec, slot):
        slot()

class MockDialog(MockQWidget):
    class DialogCode:
        Accepted = 1
        Rejected = 0
    def __init__(self, parent=None):
        super().__init__(parent)
    def exec(self):
        return 1
    def get_values(self):
        return {
            "api_key": "test_key",
            "base_url": "test_url",
            "hotkey": "<alt>+3",
            "sample_rate": 16000,
            "stt_model": "whisper-large-v3-turbo",
            "stt_language": "ru"
        }
    def accept(self):
        pass
    def reject(self):
        pass

class MockQLineEdit:
    class EchoMode:
        Password = 1
    def __init__(self, *args, **kwargs):
        self._text = ""
    def setEchoMode(self, mode):
        pass
    def setText(self, text):
        self._text = str(text)
    def text(self):
        return self._text

class MockQPushButton:
    def __init__(self, *args, **kwargs):
        self.clicked = mock.MagicMock()
    def setObjectName(self, name):
        pass

widgets_attrs = {
    "QWidget": MockQWidget,
    "QApplication": MockQApplication,
    "QDialog": MockDialog,
    "QLineEdit": MockQLineEdit,
    "QPushButton": MockQPushButton,
}

core_attrs = {
    "QObject": MockQObject,
    "pyqtSignal": mock_pyqt_signal,
    "Qt": MockQt,
    "QThread": MockQThread,
    "QTimer": MockQTimer,
}

mock_pos = mock.MagicMock()
mock_pos.x.return_value = 100
mock_pos.y.return_value = 200
mock_qcursor = mock.MagicMock()
mock_qcursor.pos.return_value = mock_pos

gui_attrs = {
    "QCursor": mock_qcursor
}

sys.modules["PyQt6"] = MockModule("PyQt6")
sys.modules["PyQt6.QtWidgets"] = MockModule("PyQt6.QtWidgets", widgets_attrs)
sys.modules["PyQt6.QtCore"] = MockModule("PyQt6.QtCore", core_attrs)
sys.modules["PyQt6.QtGui"] = MockModule("PyQt6.QtGui", gui_attrs)

class MockGlobalHotKeys:
    def __init__(self, hotkeys):
        self.hotkeys = hotkeys
    def start(self):
        pass
    def stop(self):
        pass

pynput_kbd_attrs = {
    "GlobalHotKeys": MockGlobalHotKeys,
    "Controller": mock.MagicMock
}

sys.modules["pynput"] = MockModule("pynput")
sys.modules["pynput.keyboard"] = MockModule("pynput.keyboard", pynput_kbd_attrs)

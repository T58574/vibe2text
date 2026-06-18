from pynput.keyboard import Controller
import time

class TextInjector:
    def __init__(self):
        self.keyboard = Controller()

    def inject(self, text):
        time.sleep(0.1)
        self.keyboard.type(text)
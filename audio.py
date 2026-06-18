import sounddevice as sd
import soundfile as sf
import queue

class AudioRecorder:
    def __init__(self, filename, samplerate=16000):
        self.filename = filename
        self.samplerate = samplerate
        self.q = queue.Queue()
        self.stream = None

    def callback(self, indata, frames, time, status):
        self.q.put(indata.copy())

    def start(self):
        self.q = queue.Queue()
        self.stream = sd.InputStream(samplerate=self.samplerate, channels=1, callback=self.callback)
        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
        
        with sf.SoundFile(self.filename, mode='w', samplerate=self.samplerate, channels=1) as f:
            while not self.q.empty():
                f.write(self.q.get())
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
import pyaudio
from threading import Thread
import requests


class VideoScreen(Screen):
    icon = StringProperty('volume-off')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
        self.audio_streaming = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.audio_thread = None

    def toggle_icon(self):
        if not self.audio_streaming:
            self.start_audio_stream()
            self.icon = 'volume-off'
        else:
            self.stop_audio_stream()
            self.icon = 'volume-high'
        self.audio_streaming = not self.audio_streaming

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def start_audio_stream(self):
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      output=True,
                                      frames_per_buffer=1024)
        self.audio_thread = Thread(target=self.stream_audio)
        self.audio_thread.start()

    def stop_audio_stream(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

        self.audio.terminate()
        if self.audio_thread is not None:
            self.audio_thread.join()

    def stream_audio(self):
        with requests.get("http://192.168.0.122:5000/audio_feed", stream=True) as r:
            for block in r.iter_content(1024):
                if block:
                    self.stream.write(block)

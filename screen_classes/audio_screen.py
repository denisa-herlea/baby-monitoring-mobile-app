from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from plyer import audio

class AudioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.record_button = Button(text='Start Recording')
        self.record_button.bind(on_press=self.start_recording)
        self.stop_button = Button(text='Stop and Send', on_press=self.stop_recording)
        layout.add_widget(self.record_button)
        layout.add_widget(self.stop_button)
        return layout

    def start_recording(self, instance):
        self.record_button.text = 'Recording...'
        audio.start()

    def stop_recording(self, instance):
        audio.stop()
        self.send_audio_to_server()

    def send_audio_to_server(self):
        url = 'http://192.168.0.122:5000/upload_audio'
        files = {'audio': open('your_audio_file.wav', 'rb')}
        response = requests.post(url, files=files)
        print(response.text)

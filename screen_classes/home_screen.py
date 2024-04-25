from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.material_resources import dp


class HomeScreen(Screen):
    icon_audio = StringProperty('microphone')
    icon_lights = StringProperty('string-lights-off')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def toggle_icon_audio(self):
        if self.icon_audio == 'microphone':
            self.icon_audio = 'microphone-off'
        else:
            self.icon_audio = 'microphone'


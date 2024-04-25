from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class VideoScreen(Screen):
    icon = StringProperty('volume-high')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def toggle_icon(self):
        if self.icon == 'volume-high':
            self.icon = 'volume-off'
        else:
            self.icon = 'volume-high'

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

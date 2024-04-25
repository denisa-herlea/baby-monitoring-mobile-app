from kivy.uix.boxlayout import BoxLayout
from kivymd.material_resources import dp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.core.audio import SoundLoader
from kivy.properties import BooleanProperty, ObjectProperty

from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen


def play_audio(screen, var, btn):
    if screen.currently_playing:
        screen.currently_playing.stop()

    audio_paths = {
        1: 'lullabies/Lullaby1.mp3',
        2: 'lullabies/Lullaby2.mp3',
        3: 'lullabies/Lullaby3.mp3',
        4: 'lullabies/Lullaby4.mp3',
        5: 'lullabies/Lullaby5.mp3',
        6: 'lullabies/Lullaby6.mp3',
        7: 'lullabies/Lullaby7.mp3',
        8: 'lullabies/Lullaby8.mp3',
        9: 'lullabies/Lullaby9.mp3',
        10: 'lullabies/Lullaby10.mp3',
    }
    audio_path = audio_paths.get(var, 'lullabies/Default.mp3')

    screen.currently_playing = SoundLoader.load(audio_path)
    if screen.currently_playing:
        screen.currently_playing.play()
        btn.icon = "pause-circle-outline"
    else:
        print(f"Could not load the sound from {audio_path}")


class LullabiesScreen(Screen):
    currently_playing = ObjectProperty(None)
    items_added = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        if not hasattr(self, 'rect'):
            self.rect = Rectangle(size=self.size, pos=self.pos)
            with self.canvas.before:
                Color(1, 1, 1, 1)
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self, *args):
        super(LullabiesScreen, self).on_enter(*args)
        if not self.items_added:
            self.populate_lullabies()
            self.items_added = True

    def populate_lullabies(self):
        lullabies = [("Audio 1", 1),
                     ("Audio 2", 2),
                     ("Audio 3", 3),
                     ("Audio 4", 4),
                     ("Audio 5", 5),
                     ("Audio 6", 6),
                     ("Audio 7", 7),
                     ("Audio 8", 8),
                     ("Audio 9", 9),
                     ("Audio 10", 10),
                     ("Audio 11", 11),
                     ("Audio 12", 12),
                     ("Audio 13", 13),
                     ("Audio 14", 14)]
        for name, var in lullabies:
            self.ids.content.add_widget(self.create_lullaby_item(name, var))

    def create_lullaby_item(self, name, var):
        container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(48))
        btn = MDFloatingActionButton(
            icon="play-circle-outline",
            pos_hint={'center_x': 0.3, 'center_y': 0.5},
            on_release=lambda x, var=var: play_audio(self, var, btn)
        )
        label = MDLabel(text=name, halign="center", size_hint_x=None, width=dp(100))
        container.add_widget(btn)
        container.add_widget(label)
        return container

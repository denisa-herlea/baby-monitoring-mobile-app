import websockets
from kivy.uix.boxlayout import BoxLayout
from kivymd.material_resources import dp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.core.audio import SoundLoader
from kivy.properties import BooleanProperty, ObjectProperty

from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen

from kivy.network.urlrequest import UrlRequest
import asyncio

class LullabiesScreen(Screen):
    currently_playing = ObjectProperty(None)
    items_added = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
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
        lullabies = [("Brahms' Lullaby", 1),
                     ("Lullaby For A Frantic World", 2),
                     ("Twinkle Twinkle Little Star", 3),
                     ("Lullaby Goodnight", 4),
                     ("Rock a Bye Baby", 5),
                     ("Good Night Baby", 6),
                     ("Old Elder's Farm", 7),
                     ("Moonlight", 8),
                     ("Magical stories with a twist", 9),
                     ("Greensleeves", 10)]
        for name, var in lullabies:
            self.ids.content.add_widget(self.create_lullaby_item(name, var))

    def play_audio(self, var, btn):
        if self.currently_playing:
            self.currently_playing.stop()

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

        self.currently_playing = SoundLoader.load(audio_path)
        if self.currently_playing:
            self.currently_playing.play()
        else:
            print(f"Could not load the sound from {audio_path}")

    def create_lullaby_item(self, name, var):
        container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(48))
        btn = MDFloatingActionButton(
            icon="music",
            pos_hint={'center_x': 0.2, 'center_y': 0.5},
            on_release=lambda x, var=var: self.play_audio(var, btn)
        )
        label = MDLabel(text=name, halign="center", size_hint_x=None, width=dp(100))
        container.add_widget(btn)
        container.add_widget(label)
        return container

    def pause_audio(self):
        if self.currently_playing:
            self.currently_playing.stop()

    async def send_lullaby_command(self):
        uri = "ws://192.168.195.187:5679"
        async with websockets.connect(uri) as websocket:
            await websocket.send("PLAY_LULLABY")
            response = await websocket.recv()
            print(response)

    def play(self):
        asyncio.run(self.send_lullaby_command())


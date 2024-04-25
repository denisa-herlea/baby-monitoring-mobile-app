import sqlite3

from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


class HomeScreen(Screen):
    icon_audio = StringProperty('microphone-off')
    first_name = StringProperty('John')
    last_name = StringProperty('Doe')
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

    def on_enter(self):
        self.first_name, self.last_name = self.load_user_data()

    def get_user_id(self):
        app = MDApp.get_running_app()
        return app.current_user_id

    def load_user_data(self):
        first_name=''
        last_name=''
        user_id = self.get_user_id()
        conn = sqlite3.connect('baby-v.db')
        c = conn.cursor()

        try:
            c.execute('''
                        SELECT first_name, last_name FROM users WHERE id = ?
                    ''', (user_id,))
            user_data = c.fetchone()
            if user_data:
                first_name, last_name = user_data
        except Exception as e:
            print("An error occurred:", e)
        finally:
            conn.close()
        return first_name,last_name






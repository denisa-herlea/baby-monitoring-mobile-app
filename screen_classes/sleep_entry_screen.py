import sqlite3
from kivymd.app import MDApp

from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class SleepEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def get_user_id(self):
        app = MDApp.get_running_app()
        return app.current_user_id

    def add_sleep_entry(self, baby_id, start_hour, end_hour, sleep_date, notes):
        user_id = self.current_user_id

        if start_hour and end_hour and sleep_date:
            conn = sqlite3.connect('baby-v.db')
            cursor = conn.cursor()

            cursor.execute('''SELECT id FROM babies WHERE user_id = ? LIMIT 1''', (user_id,))
            baby = cursor.fetchone()

            if baby is not None:
                baby_id = baby[0]

            cursor.execute('''INSERT INTO sleep_entries (baby_id, start_hour, end_hour, sleep_date, notes) VALUES (?, ?, ?, 
            ?, ?)''',
                       (baby_id, start_hour, end_hour, sleep_date, notes))
            conn.commit()
            conn.close()

        if not start_hour:
            self.manager.get_screen('SleepEntry').ids.start_hour.line_color_normal = self.theme_cls.error_color
            self.manager.get_screen('SleepEntry').ids.start_hour.helper_text = "Start hour cannot be empty."
        if not end_hour:
            self.manager.get_screen('SleepEntry').ids.end_hour.line_color_normal = self.theme_cls.error_color
            self.manager.get_screen('SleepEntry').ids.end_hour.helper_text = "End hour cannot be empty."
        if not sleep_date:
            self.manager.get_screen('SleepEntry').ids.sleep_date.line_color_normal = self.theme_cls.error_color
            self.manager.get_screen('SleepEntry').ids.sleep_date.helper_text = "Date cannot be empty."

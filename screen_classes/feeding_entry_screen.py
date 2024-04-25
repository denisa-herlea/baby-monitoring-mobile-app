import sqlite3
from kivymd.app import MDApp

from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen

class FeedingEntryScreen(Screen):
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

    def add_food_entry(self, baby_id, feed_hour, feed_date, ml, notes):
        user_id = self.get_user_id()
        app = MDApp.get_running_app()

        if feed_hour and feed_date:
            conn = sqlite3.connect('baby-v.db')
            cursor = conn.cursor()

            cursor.execute('''SELECT id FROM babies WHERE user_id = ? LIMIT 1''', (user_id,))
            baby = cursor.fetchone()

            if baby is not None:
                baby_id = baby[0]

            cursor.execute('''INSERT INTO food_entries (baby_id, feed_hour, feed_date, ml, notes) VALUES (?, ?, ?, 
            ?, ?)''',
                       (baby_id, feed_hour, feed_date, ml, notes))
            conn.commit()
            conn.close()

        if not feed_hour:
            self.manager.get_screen('FeedingEntry').ids.feed_hour.line_color_normal = app.theme_cls.error_color
        if not feed_date:
            self.manager.get_screen('FeedingEntry').ids.feed_date.line_color_normal = app.theme_cls.error_color

import sqlite3
from kivymd.app import MDApp

from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu


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

    def clear_fields(self):
        self.manager.get_screen('SleepEntry').ids.baby_selector.text = ''
        self.manager.get_screen('SleepEntry').ids.start_hour.text = ''
        self.manager.get_screen('SleepEntry').ids.end_hour.text = ''
        self.manager.get_screen('SleepEntry').ids.sleep_date.text = ''
        self.manager.get_screen('SleepEntry').ids.sleep_notes.text = ''

    def show_baby_selector(self):
        menu_items = [{'text': f"{baby['baby_name']}", 'viewclass': 'OneLineListItem',
                       'on_release': lambda x=f"{baby['baby_name']}": self.set_baby(x)}
                      for baby in self.fetch_babies()]
        self.menu = MDDropdownMenu(
            caller=self.manager.get_screen('SleepEntry').ids.baby_selector,
            items=menu_items,
            position="auto",
        )
        self.menu.open()

    def set_baby(self, baby_name):
        self.manager.get_screen('SleepEntry').ids.baby_selector.text = baby_name
        self.menu.dismiss()

    def fetch_babies(self):
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()
        user_id = self.get_user_id()

        query = "SELECT id, baby_name FROM babies WHERE user_id = ?"

        try:
            cursor.execute(query, (user_id,))
            babies = cursor.fetchall()
            return [{'id': baby[0], 'baby_name': baby[1]} for baby in babies]
        except sqlite3.Error as e:
            print(f"An error occurred while fetching babies: {e}")
            return []
        finally:
            conn.close()

    def add_sleep_entry(self, baby_id, baby_name, start_hour, end_hour, sleep_date, notes):
        user_id = self.get_user_id()
        app = MDApp.get_running_app()

        if baby_name and start_hour and end_hour and sleep_date:
            conn = sqlite3.connect('baby-v.db')
            cursor = conn.cursor()

            cursor.execute('''SELECT id FROM babies WHERE user_id = ? AND baby_name = ? LIMIT 1''', (user_id, baby_name,))
            baby = cursor.fetchone()

            if baby is not None:
                baby_id = baby[0]

            cursor.execute('''INSERT INTO sleep_entries (baby_id, start_hour, end_hour, sleep_date, notes) VALUES (?, ?, ?, 
            ?, ?)''',
                       (baby_id, start_hour, end_hour, sleep_date, notes))
            conn.commit()

            self.manager.get_screen('SleepEntry').ids.baby_selector.line_color_normal = app.theme_cls.primary_color
            self.manager.get_screen('SleepEntry').ids.start_hour.line_color_normal = app.theme_cls.primary_color
            self.manager.get_screen('SleepEntry').ids.end_hour.line_color_normal = app.theme_cls.primary_color
            self.manager.get_screen('SleepEntry').ids.sleep_date.line_color_normal = app.theme_cls.primary_color

            conn.close()
        if not baby_name:
            self.manager.get_screen('SleepEntry').ids.baby_selector.line_color_normal = app.theme_cls.error_color
        if not start_hour:
            self.manager.get_screen('SleepEntry').ids.start_hour.line_color_normal = app.theme_cls.error_color
        if not end_hour:
            self.manager.get_screen('SleepEntry').ids.end_hour.line_color_normal = app.theme_cls.error_color
        if not sleep_date:
            self.manager.get_screen('SleepEntry').ids.sleep_date.line_color_normal = app.theme_cls.error_color
        self.clear_fields()
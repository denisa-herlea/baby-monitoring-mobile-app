import sqlite3

from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp


class WelcomeScreen(Screen):
    baby_name = StringProperty('')
    date_of_birth = StringProperty('')
    hour_of_birth = StringProperty('')
    birth_weight = StringProperty('')
    birth_height = StringProperty('')

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

    def clear_baby_fields(self):
        self.ids.baby_name_input.text = ''
        self.ids.date_of_birth_input.text = ''
        self.ids.hour_of_birth_input.text = ''
        self.ids.birth_weight_input.text = ''
        self.ids.birth_height_input.text = ''

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def save_baby_details(self, baby_name, date_of_birth, hour_of_birth, birth_weight, birth_height):
        if baby_name:
            user_id = self.get_user_id()
            conn = sqlite3.connect('baby-v.db')
            c = conn.cursor()
            c.execute('''
                    INSERT INTO babies (user_id, baby_name, date_of_birth, hour_of_birth, birth_weight, birth_height)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, baby_name, date_of_birth, hour_of_birth, birth_weight, birth_height))
            conn.commit()
            conn.close()
            self.show_success_dialog_add_baby()
        else:
            self.manager.get_screen('Welcome').ids.baby_name.line_color_normal = self.theme_cls.error_color
            self.manager.get_screen('Welcome').ids.baby_name.helper_text = "Baby name cannot be empty."

    def show_success_dialog_add_baby(self):
        dialog = MDDialog(
            text="Baby was successfully added!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: (self.dismiss_dialog(dialog), self.redirect_home())
                ),
                MDFlatButton(
                    text="ADD ANOTHER BABY",
                    on_release=lambda x: (self.add_another_baby(dialog))
                )
            ]
        )
        dialog.open()

    def redirect_home(self):
        self.manager.current = 'Home'

    def add_another_baby(self, dialog):
        self.dismiss_dialog(dialog)
        # self.clear_baby_fields()
        self.manager.current  = 'Welcome'

    def dismiss_dialog(self, dialog):
        dialog.dismiss()

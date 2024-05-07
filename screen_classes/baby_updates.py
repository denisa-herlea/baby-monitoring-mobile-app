import sqlite3

from kivymd.app import MDApp
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem


class ChooseBabyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self):
        self.populate_babies_list()

    def get_user_id(self):
        app = MDApp.get_running_app()
        return app.current_user_id

    def fetch_babies(self):
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()
        user_id = self.get_user_id()

        query = ("SELECT id, baby_name, date_of_birth, hour_of_birth, birth_weight, birth_height  FROM babies WHERE user_id = ?")

        try:
            cursor.execute(query, (user_id,))
            babies = cursor.fetchall()
            return [{'id': baby[0], 'baby_name': baby[1], 'date_of_birth': baby[2], 'hour_of_birth': baby[3],
                     'birth_weight': baby[4], 'birth_height': baby[5]} for baby in babies]
        except sqlite3.Error as e:
            print(f"Error fetching babies: {e}")
            return []
        finally:
            conn.close()

    def populate_babies_list(self):
        babies = self.fetch_babies()
        babies_list = self.ids.babies_list

        babies_list.clear_widgets()

        for baby in babies:
            list_item = OneLineListItem(
                text=baby['baby_name'],
                on_release=lambda x, b=baby: self.select_baby(b)
            )
            babies_list.add_widget(list_item)

    def select_baby(self, baby):
        self.manager.current = 'UpdateBaby'
        self.manager.get_screen('UpdateBaby').set_baby_data(baby)


class UpdateBabyScreen(Screen):
    baby_id = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def set_baby_data(self, baby):
        self.baby_id = baby['id']
        self.ids.baby_name.text = baby['baby_name']
        self.ids.date_of_birth.text = baby['date_of_birth']
        self.ids.hour_of_birth.text = baby['hour_of_birth']
        self.ids.birth_weight.text = str(baby['birth_weight'])
        self.ids.birth_height.text = str(baby['birth_height'])

    def return_baby_id(self):
        return self.baby_id

    def update_baby_name(self, new_name):
        baby_id = self.return_baby_id()
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE babies SET baby_name = ? WHERE id = ?
            ''', (new_name, baby_id))

            conn.commit()
            self.show_success_dialog("Baby's name successfully updated!")
        except sqlite3.Error as e:
            self.show_error_dialog(f"Database error: {e}")
        finally:
            conn.close()

    def update_date_of_birth(self, date_of_birth):
        baby_id = self.return_baby_id()
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE babies SET date_of_birth = ? WHERE id = ?
                    ''', (date_of_birth, baby_id))

            conn.commit()
            self.show_success_dialog("Baby's date of birth successfully updated!")
        except sqlite3.Error as e:
            self.show_error_dialog(f"Database error: {e}")
        finally:
            conn.close()

    def update_hour_of_birth(self, hour_of_birth):
        baby_id = self.return_baby_id()
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                    UPDATE babies SET hour_of_birth = ? WHERE id = ?
                            ''', (hour_of_birth, baby_id))

            conn.commit()
            self.show_success_dialog("Baby's hour of birth successfully updated!")
        except sqlite3.Error as e:
            self.show_error_dialog(f"Database error: {e}")
        finally:
            conn.close()

    def update_birth_weight(self, birth_weight):
        baby_id = self.return_baby_id()
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE babies SET birth_weight = ? WHERE id = ?
                    ''', (birth_weight, baby_id))

            conn.commit()
            self.show_success_dialog("Baby's birth weight successfully updated!")
        except sqlite3.Error as e:
            self.show_error_dialog(f"Database error: {e}")
        finally:
            conn.close()

    def update_birth_height(self, birth_height):
        baby_id = self.return_baby_id()
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE babies SET birth_height = ? WHERE id = ?
                    ''', (birth_height, baby_id))

            conn.commit()
            self.show_success_dialog("Baby's birth height successfully updated!")
        except sqlite3.Error as e:
            self.show_error_dialog(f"Database error: {e}")
        finally:
            conn.close()

    def show_success_dialog(self, text):
        dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dismiss_dialog(dialog)
                )
            ]
        )
        dialog.open()

    def dismiss_dialog(self, dialog):
        dialog.dismiss()


class AddNewBabyScreen(Screen):
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
        self.manager.get_screen('AddNewBaby').ids.baby_name.text = ''
        self.manager.get_screen('AddNewBaby').ids.date_of_birth.text = ''
        self.manager.get_screen('AddNewBaby').ids.hour_of_birth.text = ''
        self.manager.get_screen('AddNewBaby').ids.birth_weight.text = ''
        self.manager.get_screen('AddNewBaby').ids.birth_height.text = ''

    def save_baby_details(self, baby_name, date_of_birth, hour_of_birth, birth_weight, birth_height):
        app = MDApp.get_running_app()
        if baby_name:
            user_id = self.get_user_id()
            conn = sqlite3.connect('baby-v.db')
            c = conn.cursor()

            try:
                c.execute('SELECT id FROM babies WHERE baby_name = ? AND user_id = ?', (baby_name, user_id))
                existing_baby = c.fetchone()

                if existing_baby:
                    self.manager.get_screen('AddNewBaby').ids.baby_name.line_color_normal = app.theme_cls.error_color
                    self.manager.get_screen('AddNewBaby').ids.baby_name.helper_text = "Baby was already registered"
                    return
                c.execute('''
                    INSERT INTO babies (user_id, baby_name, date_of_birth, hour_of_birth, birth_weight, birth_height)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, baby_name, date_of_birth, hour_of_birth, birth_weight, birth_height))
                conn.commit()
                self.manager.get_screen('AddNewBaby').ids.baby_name.line_color_normal = app.theme_cls.primary_color
                self.manager.get_screen('AddNewBaby').ids.baby_name.helper_text = ''
                self.show_success_dialog_add_baby()
            finally:
                conn.close()
        else:
            self.manager.get_screen('AddNewBaby').ids.baby_name.line_color_normal = app.theme_cls.error_color

    def show_success_dialog_add_baby(self):
        dialog = MDDialog(
            text="Baby was successfully added!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: (self.dismiss_dialog(dialog))
                )
            ]
        )
        dialog.open()

    def dismiss_dialog(self, dialog):
        self.clear_baby_fields()
        dialog.dismiss()

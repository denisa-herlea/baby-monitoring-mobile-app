import sqlite3

from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class AccountScreen(Screen):
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

    def toggle_icon_lights(self):
        app = MDApp.get_running_app()
        if self.icon_lights == 'string-lights-off':
            self.icon_lights = 'string-lights'
            app.theme_cls.theme_style = "Dark"
        else:
            self.icon_lights = 'string-lights-off'
            app.theme_cls.theme_style = "Light"

    def get_user_id(self):
        app = MDApp.get_running_app()
        return app.current_user_id

    def update_last_name(self):
        user_id = self.get_user_id()
        last_name = self.ids.last_name.text
        self.update_user_last_name(user_id, last_name)

    def update_first_name(self):
        user_id = self.get_user_id()
        first_name = self.ids.first_name.text
        self.update_user_first_name(user_id, first_name)

    def update_password(self):
        user_id = self.get_user_id()
        password = self.ids.password.text
        self.update_user_password(user_id, password)

    def update_user_last_name(self, user_id, last_name):
        conn = sqlite3.connect('baby-v.db')
        c = conn.cursor()

        try:
            c.execute('''
                UPDATE users SET last_name = ? WHERE id = ?
            ''', (last_name, user_id))
            conn.commit()
            self.show_success_dialog_last_name()
        except Exception as e:
            print("An error occurred:", e)
        finally:
            conn.close()

        self.manager.current = 'Account'

    def update_user_first_name(self, user_id, first_name):
        conn = sqlite3.connect('baby-v.db')
        c = conn.cursor()
        try:
            c.execute('''
                UPDATE users SET first_name = ? WHERE id = ?
            ''', ( first_name, user_id))
            conn.commit()
            self.show_success_dialog_first_name()
        except Exception as e:
            print("An error occurred:", e)
        finally:
            conn.close()

        self.manager.current = 'Account'

    def update_user_password(self, user_id, password):
        conn = sqlite3.connect('baby-v.db')
        c = conn.cursor()
        try:
            c.execute('''
                UPDATE users SET password = ? WHERE id = ?
            ''', ( password, user_id))
            conn.commit()
            self.show_success_dialog_password()
        except Exception as e:
            print("An error occurred:", e)
        finally:
            conn.close()
        self.manager.current = 'Account'

    def show_success_dialog_first_name(self):
        dialog = MDDialog(
            text="First name was successfully updated!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dismiss_dialog(dialog)
                )
            ]
        )
        dialog.open()

    def show_success_dialog_last_name(self):
        dialog = MDDialog(
            text="Last name was successfully updated!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dismiss_dialog(dialog)
                )
            ]
        )
        dialog.open()

    def show_success_dialog_password(self):
        dialog = MDDialog(
            text="Password was successfully updated!",
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

    def show_delete_confirmation(self):
        dialog = MDDialog(
            title="Confirm Deletion",
            text="Are you sure you want to delete your account?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dismiss_dialog(dialog)
                ),
                MDFlatButton(
                    text="DELETE",
                    on_release=lambda x: (self.delete_account(), self.dialog.dismiss(dialog))
                )
            ]
        )
        dialog.open()

    def delete_account(self):
        user_id = self.get_user_id()
        conn = sqlite3.connect('baby-v.db')
        c = conn.cursor()
        try:
            c.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            self.show_success_delete()
        except sqlite3.Error as e:
            print(f"An error occurred while trying to delete the account: {e}")
        finally:
            conn.close()
        self.manager.current = 'Login'

    def show_success_delete(self):
        dialog = MDDialog(
            text="Account was successfully deleted!",
            buttons=[
                MDFlatButton(
                    text="BACK TO LOGIN",
                    on_release=lambda x: self.dismiss_dialog(dialog)
                )
            ]
        )
        dialog.open()

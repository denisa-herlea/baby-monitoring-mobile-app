import sqlite3

from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu


class GrowthHealthTrackingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos


class LogMeasurementScreen(Screen):
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
        self.manager.get_screen('LogMeasurement').ids.baby_selector.text = ''
        self.manager.get_screen('LogMeasurement').ids.height_field.text = ''
        self.manager.get_screen('LogMeasurement').ids.weight_field.text = ''
        self.manager.get_screen('LogMeasurement').ids.head_circ_field.text = ''
        self.manager.get_screen('LogMeasurement').ids.measurement_date.text = ''


    def show_baby_selector(self):
        menu_items = [{'text': f"{baby['baby_name']}", 'viewclass': 'OneLineListItem',
                       'on_release': lambda x=f"{baby['baby_name']}": self.set_baby(x)}
                      for baby in self.fetch_babies()]
        self.menu = MDDropdownMenu(
            caller=self.manager.get_screen('LogMeasurement').ids.baby_selector,
            items=menu_items,
            position="auto",
        )
        self.menu.open()

    def set_baby(self, baby_name):
        self.manager.get_screen('LogMeasurement').ids.baby_selector.text = baby_name
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

    def save_measurement(self, baby_id, baby_name, measurement_date, height_field, weight_field, head_circ_field):
        user_id = self.get_user_id()
        app = MDApp.get_running_app()

        if baby_name and measurement_date and height_field and weight_field and head_circ_field:
            conn = sqlite3.connect('baby-v.db')
            cursor = conn.cursor()

            cursor.execute('''SELECT id FROM babies WHERE user_id = ? AND baby_name = ? LIMIT 1''', (user_id, baby_name,))
            baby = cursor.fetchone()

            if baby is not None:
                baby_id = baby[0]

            cursor.execute('''INSERT INTO measurement_entries (baby_id, measurement_date, height, weight, head_circ) VALUES (?, ?, ?, 
            ?, ?)''',
                       (baby_id, measurement_date, height_field, weight_field, head_circ_field))
            conn.commit()

            self.manager.get_screen('LogMeasurement').ids.baby_selector.line_color_normal = app.theme_cls.primary_color
            self.manager.get_screen('LogMeasurement').ids.height_field.line_color_normal = app.theme_cls.primary_color
            self.manager.get_screen('LogMeasurement').ids.weight_field.line_color_normal = app.theme_cls.primary_color
            self.manager.get_screen('LogMeasurement').ids.head_circ_field.line_color_normal = app.theme_cls.primary_color
            self.manager.get_screen('LogMeasurement').ids.measurement_date.line_color_normal = app.theme_cls.primary_color

            conn.close()
        if not baby_name:
            self.manager.get_screen('LogMeasurement').ids.baby_selector.line_color_normal = app.theme_cls.error_color
        if not height_field:
            self.manager.get_screen('LogMeasurement').ids.height_field.line_color_normal = app.theme_cls.error_color
        if not weight_field:
            self.manager.get_screen('LogMeasurement').ids.weight_field.line_color_normal = app.theme_cls.error_color
        if not head_circ_field:
            self.manager.get_screen('LogMeasurement').ids.head_circ_field.line_color_normal = app.theme_cls.error_color
        if not measurement_date:
            self.manager.get_screen('LogMeasurement').ids.measurement_date.line_color_normal = app.theme_cls.error_color
        self.clear_fields()


class VaccinesScreen(Screen):
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
        self.data_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            size_hint=(0.9, 0.8),
            rows_num=27,
            column_data=[
                ("Age", dp(20)),
                ("Recommended Vaccines", dp(25)),
                ("Dose No.",dp(10))
            ],
            row_data=[
                ("After Birth", "HepB","1"),
                ("1-2 months", "HepB", "2"),
                ("2 months", "DTaP", "1"),
                ("2 months", "Hib", "1"),
                ("2 months", "IPV", "1"),
                ("2 months", "RV", "1"),
                ("2 months", "PCV13", "1"),
                ("4 months", "DTaP", "2"),
                ("4 months", "Hib", "2"),
                ("4 months", "IPV", "2"),
                ("4 months", "RV", "2"),
                ("4 months", "PCV13", "2"),
                ("6-15 months", "Hib", "3/4"),
                ("6-15 months", "MMR", "1"),
                ("6-18 months", "HepB","3"),
                ("6-18 months", "IPV", "3"),
                ("6 months", "DTaP", "3"),
                ("6 months", "PCV13", "3"),
                ("6 months-6 yrs", "Flu", "Yearly"),
                ("12-15 months", "PCV13", "4"),
                ("12-15 months", "Varicella", "1"),
                ("12-18 months", "HepA", "1 & 2"),
                ("15-18 months", "DTaP", "4"),
                ("4-6 years", "DTaP", "5"),
                ("4-6 years", "IPV", "4"),
                ("4-6 years", "MMR", "2"),
                ("4-6 years", "Varicella", "2"),
            ]
        )

        self.add_widget(self.data_table)

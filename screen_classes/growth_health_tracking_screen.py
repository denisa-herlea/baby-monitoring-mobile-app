import sqlite3

from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from matplotlib import pyplot as plt
from datetime import datetime, timedelta


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


class MeasurementReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self, *args):
        self.load_data()

    def get_user_id(self):
        app = MDApp.get_running_app()
        return app.current_user_id

    def load_data(self):
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()
        user_id = self.get_user_id()


        query = """
        SELECT b.id, b.baby_name
        FROM babies b
        WHERE b.user_id = ?
        """
        cursor.execute(query, (user_id,))
        babies = cursor.fetchall()

        self.ids.cards_container.clear_widgets()
        for baby_id, baby_name in babies:
            card = self.create_card(baby_id, baby_name)
            self.ids.cards_container.add_widget(card)

        conn.close()

    def create_card(self, baby_id, baby_name):
        card = MDCard(size_hint=(None, None), size=("280dp", "100dp"),
                      md_bg_color=[185 / 255, 220 / 255, 170 / 255, 1],
                      orientation='vertical',
                      padding=20)

        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=40)

        growth_chart_button = MDRaisedButton(text="Growth Chart", text_color=[0, 0.2, 0.2, 1], size_hint=(None, None), size=(250, 50),
                                             md_bg_color=[235 / 255, 230 / 255, 210 / 255, 1])
        growth_chart_button.bind(on_press=lambda x: self.show_growth_chart(baby_id))

        measurement_table_button = MDRaisedButton(text="Measurement Table", text_color=[0.2, 0.2, 0.2, 1], size_hint=(None, None), size=(250, 50), md_bg_color=[125 / 255, 205 / 255, 230 / 255, 1])
        measurement_table_button.bind(on_press=lambda x: self.show_measurement_table(baby_id))

        button_layout.add_widget(growth_chart_button)
        button_layout.add_widget(measurement_table_button)

        label_layout = BoxLayout(orientation='vertical', padding=(20, 20, 20, 20), size_hint_y=None, height=40)
        label = MDLabel(text=f"{baby_name}", halign='right', theme_text_color='Custom',
                        text_color=[0.2, 0.2, 0.2, 1])
        label_layout.add_widget(label)

        card.add_widget(label_layout)
        card.add_widget(button_layout)

        return card

    def show_growth_chart(self, baby_id):
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()

        query = """
        SELECT measurement_date, height, weight, head_circ
        FROM measurement_entries
        WHERE baby_id = ?
        ORDER BY measurement_date
        """
        cursor.execute(query, (baby_id,))
        measurements = cursor.fetchall()

        dates = [datetime.strptime(entry[0], '%Y-%m-%d').date() for entry in measurements]
        heights = [entry[1] for entry in measurements]
        weights = [entry[2] for entry in measurements]
        head_circs = [entry[3] for entry in measurements]

        fig, ax = plt.subplots(3, 1, figsize=(5, 12), sharex=True)

        ax[0].plot(dates, heights, marker='o', linestyle='-', color='lightblue')
        ax[0].set_ylabel('Height (cm)')
        ax[0].set_title('Growth Over Time', fontsize=14)

        ax[1].plot(dates, weights, marker='o', linestyle='-', color='green')
        ax[1].set_ylabel('Weight (kg)')

        ax[2].plot(dates, head_circs, marker='o', linestyle='-', color='pink')
        ax[2].set_ylabel('Head Circumference (cm)')
        ax[2].set_xlabel('Date')

        for ax_ in ax:
            for label in ax_.get_xticklabels():
                label.set_rotation(45)
                label.set_ha('right')

        plt.tight_layout()

        chart_container = self.ids.chart_container
        chart_container.clear_widgets()

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        scroll_view.add_widget(FigureCanvasKivyAgg(fig))

        chart_container.add_widget(scroll_view)

        close_button = self.ids.close_button
        close_button.opacity = 1
        close_button.disabled = False

        conn.close()

    def show_measurement_table(self, baby_id):
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()

        query = """
        SELECT measurement_date, height, weight, head_circ
        FROM measurement_entries
        WHERE baby_id = ?
        ORDER BY measurement_date
        """
        cursor.execute(query, (baby_id,))
        measurements = cursor.fetchall()

        table_data = []
        for entry in measurements:
            measurement_date, height, weight, head_circ = entry
            height_m = height / 100
            bmi = weight / (height_m ** 2) if height_m > 0 else 0
            table_data.append((round(bmi, 2), height, weight, head_circ, measurement_date))

        data_table = MDDataTable(
            size_hint=(1, 1),
            pos_hint=(0.5, 0.5),
            column_data=[
                ("BMI", dp(15)),
                ("Height (cm)", dp(20)),
                ("Weight (kg)", dp(20)),
                ("Head Circumference (cm)", dp(30)),
                ("Date", dp(30)),
            ],
            row_data=table_data
        )

        chart_container = self.ids.chart_container
        chart_container.clear_widgets()

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        scroll_view.add_widget(data_table)

        chart_container.add_widget(scroll_view)

        close_button = self.ids.close_button
        close_button.opacity = 1
        close_button.disabled = False

        conn.close()

    def hide_chart(self):
        chart_container = self.ids.chart_container
        chart_container.clear_widgets()

        close_button = self.ids.close_button
        close_button.opacity = 0
        close_button.disabled = True



import sqlite3

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from datetime import datetime, timedelta
from matplotlib import pyplot as plt


class FeedingTrackingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos


class FeedingReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def on_enter(self, *args):
        self.load_data()

    def get_user_id(self):
        app = MDApp.get_running_app()
        return app.current_user_id

    def load_data(self):
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()
        user_id = self.get_user_id()
        today = datetime.now().date()

        query = """
        SELECT b.id, b.baby_name, IFNULL(SUM(fe.ml), 0)
        FROM babies b
        LEFT JOIN food_entries fe ON b.id = fe.baby_id AND DATE(fe.feed_date) = ?
        WHERE b.user_id = ?
        GROUP BY b.id, b.baby_name
        """
        cursor.execute(query, (today, user_id))
        babies = cursor.fetchall()

        self.ids.cards_container.clear_widgets()
        for baby_id, baby_name, total_milk in babies:
            card = self.create_card(baby_id, baby_name, total_milk)
            self.ids.cards_container.add_widget(card)

        conn.close()

    def create_card(self, baby_id, baby_name, total_milk):
        card = MDCard(size_hint=(None, None), size=("280dp", "100dp"),
                      md_bg_color=[225 / 255, 220 / 255, 205 / 255, 1],
                      orientation='vertical',
                      padding=20)

        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=40)

        milk_ratio_button = MDRaisedButton(text="Milk Ratio", size_hint=(None, None), size=(250, 50),
                                           md_bg_color=[235 / 255, 190 / 255, 230 / 255, 1])
        milk_ratio_button.bind(on_press=lambda x: self.show_feeding_chart(baby_id))

        other_food_button = MDRaisedButton(text="Other Food", size_hint=(None, None), size=(250, 50),
                                           md_bg_color=[195 / 255, 100 / 255, 185 / 255, 1])
        other_food_button.bind(on_press=lambda x: self.show_other_food(baby_id))

        button_layout.add_widget(milk_ratio_button)
        button_layout.add_widget(other_food_button)

        label_layout = BoxLayout(orientation='vertical',spacing=30, padding=(20, 20, 20, 20), size_hint_y=None, height=40)
        label = MDLabel(text=f"{baby_name}", halign='right', theme_text_color='Custom', text_color=[0.2, 0.2, 0.2, 1])
        milk_label = MDLabel(text=f"Total Milk: {total_milk} ml", halign='right', theme_text_color='Custom',
                             text_color=[0.2, 0.2, 0.2, 1])
        label_layout.add_widget(label)
        label_layout.add_widget(milk_label)

        card.add_widget(label_layout)
        card.add_widget(button_layout)

        return card

    def show_feeding_chart(self, baby_id, selected_date=None):
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()

        if selected_date is None:
            selected_date = datetime.now().date()

        query = """
        SELECT feed_hour, ml
        FROM food_entries
        WHERE baby_id = ? AND feed_date = ?
        """
        cursor.execute(query, (baby_id, selected_date))
        food_entries = cursor.fetchall()

        hours = list(range(24))
        ml_per_hour = [0] * 24

        for entry in food_entries:
            feed_hour, ml = entry
            hour = datetime.strptime(feed_hour, '%H:%M').hour
            ml_per_hour[hour] += ml

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(hours, ml_per_hour, color='pink')
        ax.set_yticks(hours)
        ax.set_yticklabels([f"{h}:00" for h in hours])
        ax.set_xlabel('Milliliters (ml)')
        ax.set_title(f'Distribution of Feedings on {selected_date.strftime("%Y-%m-%d")}')
        ax.set_xlim(0, 300)

        chart_container = self.ids.chart_container
        chart_container.clear_widgets()

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        scroll_view.add_widget(FigureCanvasKivyAgg(fig))

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50),
                                  padding=(10, 10, 10, 10), spacing=10)

        with button_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=button_layout.size, pos=button_layout.pos)

        button_layout.bind(size=self._update_rect, pos=self._update_rect)

        left_arrow = MDIconButton(icon="arrow-left", size_hint=(None, None), size=(40, 40))
        right_arrow = MDIconButton(icon="arrow-right", size_hint=(None, None), size=(40, 40))

        left_arrow.bind(on_release=lambda x: self.show_feeding_chart(baby_id, selected_date - timedelta(days=1)))
        right_arrow.bind(on_release=lambda x: self.show_feeding_chart(baby_id, selected_date + timedelta(
            days=1) if selected_date < datetime.now().date() else selected_date))

        button_layout.add_widget(left_arrow)
        button_layout.add_widget(right_arrow)

        chart_container.add_widget(button_layout)
        chart_container.add_widget(scroll_view)

        close_button = self.ids.close_button
        close_button.opacity = 1
        close_button.disabled = False

        conn.close()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def hide_chart(self):
        chart_container = self.ids.chart_container
        chart_container.clear_widgets()

        close_button = self.ids.close_button
        close_button.opacity = 0
        close_button.disabled = True

    def show_other_food(self, baby_id):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=lambda instance, value, date_range: self.show_food_for_date(baby_id, value))
        date_dialog.open()

    def show_food_for_date(self, baby_id, selected_date):
        try:
            print(f"Showing food for date: {selected_date} for baby_id: {baby_id}")
            conn = sqlite3.connect('baby-v.db')
            cursor = conn.cursor()

            query = """
            SELECT feed_hour, notes
            FROM food_entries
            WHERE baby_id = ? AND feed_date = ? AND notes IS NOT NULL AND notes != ''
            """
            cursor.execute(query, (baby_id, selected_date.strftime('%Y-%m-%d')))
            food_entries = cursor.fetchall()

            table_data = []
            if food_entries:
                for entry in food_entries:
                    feed_hour, notes = entry
                    table_data.append((feed_hour, notes))
            else:
                table_data.append(("No entries", "No entries"))

            data_table = MDDataTable(
                size_hint=(1, 0.75),
                column_data=[
                    ("Feed Hour", dp(20)),
                    ("Notes", dp(80)),
                ],
                row_data=table_data)

            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            close_button = MDRaisedButton(text='Close', size_hint=(None, None), size=(100, 40))
            food_popup = Popup(title=f"Food Entries for {selected_date.strftime('%Y-%m-%d')}", content=layout,
                               size_hint=(0.9, 0.9))

            close_button.bind(on_release=food_popup.dismiss)
            layout.add_widget(data_table)
            layout.add_widget(close_button)

            food_popup.open()

            conn.close()
        except Exception as e:
            print(f"Error showing food for date: {e}")

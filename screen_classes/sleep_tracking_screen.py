import calendar

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import sqlite3
from datetime import datetime, timedelta, time

from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from matplotlib import pyplot as plt


class SleepTrackingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos


class SleepRecScreen(Screen):
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
            rows_num=9,
            column_data=[
                ("Age Group", dp(30)),
                ("Recommended Sleep", dp(30))
            ],
            row_data=[
                ("Babies (<4 months)", "16+ hours"),
                ("Infants (4-12 months)", "12-16 hours"),
                ("Toddlers (1-2 years)", "11-14 hours"),
                ("Children (3-5 years)", "10-13 hours"),
                ("Children (6-13 years)", "9-11 hours"),
                ("Teenagers (14-17 years)", "8-10 hours"),
                ("Young Adults (18-25 years)", "7-9 hours"),
                ("Adults (26-64 years)", "7-9 hours"),
                ("Seniors (65+ years)", "7-8 hours")
            ]
        )

        self.add_widget(self.data_table)


class SleepReportScreen(Screen):
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
        SELECT b.id, b.baby_name, b.date_of_birth, IFNULL(SUM(strftime('%s', se.end_hour) - strftime('%s', se.start_hour)), 0)
        FROM babies b
        LEFT JOIN sleep_entries se ON b.id = se.baby_id AND se.sleep_date = ?
        WHERE b.user_id = ?
        GROUP BY b.id, b.baby_name
        """
        cursor.execute(query, (today, user_id))
        babies = cursor.fetchall()

        self.ids.cards_container.clear_widgets()
        for baby_id, baby_name, dob, total_seconds in babies:
            recommended_sleep = 0
            age_months = -1
            if dob is not '':
                age_months = (today - datetime.strptime(dob, '%Y-%m-%d').date()).days / 30

            if age_months <= 4 and age_months != -1:
                recommended_sleep = 16
            elif 4 < age_months < 12:
                recommended_sleep = 14
            elif 12 <= age_months < 36:
                recommended_sleep = 12.5
            elif 36 <= age_months < 60:
                recommended_sleep = 12
            elif age_months == -1:
                recommended_sleep = 0

            hours_slept = total_seconds / 3600
            card = self.create_card(baby_id, baby_name, hours_slept, recommended_sleep)
            self.ids.cards_container.add_widget(card)

        conn.close()

    def create_card(self, baby_id, baby_name, hours_slept, recommended_sleep):
        card = MDCard(size_hint=(None, None), size=("280dp", "100dp"),
                      md_bg_color=[0.68, 0.85, 0.9, 1],
                      orientation='horizontal')

        icon_layout = BoxLayout(size_hint=(None, 1), width=card.height)
        sleep_icon = MDIconButton(icon='weather-night', size_hint=(None, None), size=(50, 50))
        icon_layout.add_widget(sleep_icon)

        label_layout = BoxLayout(orientation='vertical', padding=(10, 0, 0, 0))
        if recommended_sleep != 0:
            label = MDLabel(text=f"{baby_name}: {hours_slept:.1f}/{recommended_sleep} hours",
                            halign='center', theme_text_color='Custom', text_color=[0.2, 0.2, 0.2, 1])
        else:
            label = MDLabel(text=f"{baby_name}: {hours_slept:.1f} hours",
                            halign='center', theme_text_color='Custom', text_color=[0.2, 0.2, 0.2, 1])
        label_layout.add_widget(label)

        card.add_widget(icon_layout)
        card.add_widget(label_layout)
        card.bind(on_release=lambda x: self.show_sleep_chart(baby_id, recommended_sleep))

        return card

    def show_sleep_chart(self, baby_id, recommended_sleep):
        conn = sqlite3.connect('baby-v.db')
        cursor = conn.cursor()

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=6)

        query = """
        SELECT sleep_date, start_hour, end_hour 
        FROM sleep_entries 
        WHERE baby_id = ? AND sleep_date BETWEEN ? AND ?
        """
        cursor.execute(query, (baby_id, start_date, end_date))
        sleep_entries = cursor.fetchall()

        days = []
        day_sleep = []
        night_sleep = []

        for i in range(7):
            date = start_date + timedelta(days=i)
            days.append(calendar.day_name[date.weekday()])
            day_total = 0
            night_total = 0
            for entry in sleep_entries:
                sleep_date, start_hour, end_hour = entry
                if sleep_date == date.strftime('%Y-%m-%d'):
                    start = datetime.strptime(start_hour, '%H:%M').time()
                    end = datetime.strptime(end_hour, '%H:%M').time()
                    if start >= time(7, 0) and end <= time(20, 0):
                        day_total += (datetime.combine(date, end) - datetime.combine(date, start)).seconds
                    else:
                        night_total += (datetime.combine(date, end) - datetime.combine(date, start)).seconds
            day_sleep.append(day_total / 3600)
            night_sleep.append(night_total / 3600)

        fig, ax = plt.subplots(figsize=(3.6, 6.4))
        ax.barh(days, day_sleep, label='Day Sleep', color='pink')
        ax.barh(days, night_sleep, left=day_sleep, label='Night Sleep', color='lightblue')
        ax.set_ylabel('Day of the Week')
        ax.set_xlabel('Hours of Sleep')
        ax.set_title('Sleep Duration over the Last Week')
        if recommended_sleep == 0:
            recommended_sleep = 16
        ax.set_xlim(0, recommended_sleep)
        ax.legend()

        for label in ax.get_yticklabels():
            label.set_rotation(45)
            label.set_ha('right')

        chart_container = self.ids.chart_container
        chart_container.clear_widgets()

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        scroll_view.add_widget(FigureCanvasKivyAgg(fig))

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

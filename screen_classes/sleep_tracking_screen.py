from kivy_garden.graph import Graph, MeshLinePlot
import sqlite3
from datetime import datetime, timedelta

from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen


def calculate_sleep_durations(baby_id, week_start_date):
    conn = sqlite3.connect('baby-v.db')
    cursor = conn.cursor()

    week_end_date = week_start_date + timedelta(days=7)

    cursor.execute('''
        SELECT sleep_date, start_hour, end_hour FROM sleep_entries
        WHERE baby_id = ? AND sleep_date BETWEEN ? AND ?
    ''', (baby_id, week_start_date.strftime('%Y-%m-%d'), week_end_date.strftime('%Y-%m-%d')))

    sleep_entries = cursor.fetchall()
    conn.close()

    day_sleep = {i: 0 for i in range(7)}
    night_sleep = {i: 0 for i in range(7)}

    for sleep_date, start, end in sleep_entries:
        start_dt = datetime.strptime(f"{sleep_date} {start}", "%Y-%m-%d %H:%M")

        if start > end:
            end_dt = datetime.strptime(f"{sleep_date} {end}", "%Y-%m-%d %H:%M") + timedelta(days=1)
        else:
            end_dt = datetime.strptime(f"{sleep_date} {end}", "%Y-%m-%d %H:%M")

        duration = (end_dt - start_dt).total_seconds() / 3600

        if (start_dt.hour >= 20 or start_dt.hour < 7) and (end_dt.hour >= 20 or end_dt.hour < 7):
            night_sleep[start_dt.weekday()] += duration
        else:
            day_sleep[start_dt.weekday()] += duration

    return day_sleep, night_sleep


class SleepTrackingScreen(Screen):
    baby_name = 'Anna'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(255 / 255.0, 255 / 255.0, 255 / 255.0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def add_sleep_chart(self, day_sleep, night_sleep):
        graph = Graph(xlabel='Date', ylabel='Y',
                      x_ticks_minor=5, x_ticks_major=1, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=0, xmax=7, ymin=0,
                      ymax=max(max(day_sleep.values()), max(night_sleep.values())) + 1)

        day_plot = MeshLinePlot(color=[1, 0.5, 0, 1])
        night_plot = MeshLinePlot(color=[0, 0, 1, 1])

        day_plot.points = [(i, day_sleep[i]) for i in range(7)]
        night_plot.points = [(i, night_sleep[i]) for i in range(7)]

        graph.add_plot(day_plot)
        graph.add_plot(night_plot)
        graph.size_hint = (1, 1)

        self.ids.sleep_graph.clear_widgets()
        self.ids.sleep_graph.add_widget(graph)

    def create_sleep_chart(self):
        day_sleep, night_sleep = calculate_sleep_durations(1, datetime(2024, 4, 1))
        self.add_sleep_chart(day_sleep, night_sleep)

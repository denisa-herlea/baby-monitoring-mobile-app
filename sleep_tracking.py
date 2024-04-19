import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


import numpy as np


def calculate_sleep_durations(baby_id, week_start_date):
    conn = sqlite3.connect('baby-v.db')
    cursor = conn.cursor()

    week_end_date = week_start_date + timedelta(days=7)

    cursor.execute('''
        SELECT sleep_date, start_hour, end_hour FROM sleep_entries
        WHERE baby_id = ? AND sleep_date BETWEEN ? AND ?
    ''', (baby_id, week_start_date.strftime('%Y-%m-%d'), week_end_date.strftime('%Y-%m-%d')))

    sleep_entries = cursor.fetchall()
    print(sleep_entries)
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


def plot_sleep_chart(baby_id, week_start_date):
    day_sleep, night_sleep = calculate_sleep_durations(baby_id, week_start_date)
    days_of_week = np.arange(7)
    bar_width = 0.35

    day_hours = [day_sleep[day] for day in days_of_week]
    night_hours = [night_sleep[day] for day in days_of_week]

    plt.figure(figsize=(10, 6))

    plt.bar(days_of_week - bar_width / 2, day_hours, width=bar_width, color='orange', label='Day Sleep')
    plt.bar(days_of_week + bar_width / 2, night_hours, width=bar_width, color='blue', label='Night Sleep')

    plt.xlabel('Day of the Week')
    plt.ylabel('Hours Slept')
    plt.title('Sleep Duration by Day and Night')
    plt.xticks(days_of_week, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.legend()

    plt.show()


def plot_sleep_chart_call():
    plot_sleep_chart(1, datetime(2024, 4, 1))



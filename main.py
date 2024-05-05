from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

import sqlite3
from datetime import datetime

from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder

from helper import screen_helper
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.button import MDFlatButton
from sleep_tracking import plot_sleep_chart_call

import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from screen_classes.lullabies_screen import LullabiesScreen
from screen_classes.login_screen import LoginScreen
from screen_classes.register_screen import RegisterScreen
from screen_classes.welcome_screen import WelcomeScreen
from screen_classes.home_screen import HomeScreen
from screen_classes.sleep_tracking_screen import SleepTrackingScreen
from screen_classes.feeding_tracking_screen import FeedingTrackingScreen
from screen_classes.growth_health_tracking_screen import GrowthHealthTrackingScreen
from screen_classes.video_screen import VideoScreen
from screen_classes.sleep_entry_screen import SleepEntryScreen
from screen_classes.feeding_entry_screen import FeedingEntryScreen
from screen_classes.account_screen import AccountScreen
from screen_classes.baby_updates import UpdateBabyScreen,ChooseBabyScreen

sm = ScreenManager()
sm.add_widget(LoginScreen(name='Login'))
sm.add_widget(RegisterScreen(name='Register'))
sm.add_widget(WelcomeScreen(name='Welcome'))
sm.add_widget(HomeScreen(name='Home'))
sm.add_widget(FeedingTrackingScreen(name='FeedingTracking'))
sm.add_widget(SleepTrackingScreen(name='SleepTracking'))
sm.add_widget(GrowthHealthTrackingScreen(name='GrowthHealthTracking'))
sm.add_widget(LullabiesScreen(name='Lullabies'))
sm.add_widget(VideoScreen(name='Video'))
sm.add_widget(SleepEntryScreen(name='SleepEntry'))
sm.add_widget(FeedingEntryScreen(name='FeedingEntry'))
sm.add_widget(AccountScreen(name='Account'))
sm.add_widget(UpdateBabyScreen(name='UpdateBaby'))
sm.add_widget(ChooseBabyScreen(name='ChooseBaby'))

class VideoStreamWidget(Image):
    def start_stream(self, url):
        self.capture = cv2.VideoCapture(url)
        Clock.schedule_interval(self.update, 1.0 / 33.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture


class DemoApp(MDApp):
    current_user_id = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        screen = Builder.load_string(screen_helper)
        return screen

    def on_start(self):
        sleep_screen = self.root.get_screen('SleepTracking')
        video_screen = self.root.get_screen('Video')

        video_widget = video_screen.ids.video_stream
        video_widget.start_stream('http://192.168.0.122:5000/video_feed')

        sleep_screen.plot_sleep_chart_call = plot_sleep_chart_call

    # -----------------  DIALOGS  ---------------------
    def back_to_login(self):
        self.root.current = 'Login'
        self.root.get_screen('Login').ids.login_username.text = ""
        self.root.get_screen('Login').ids.login_password.text = ""

    def close_dialog_to_login(self, obj):
        self.dialog.dismiss()
        self.root.current = 'Login'

    def close_dialog_to_welcome(self, obj):
        self.dialog.dismiss()
        self.root.current = 'Welcome'

    def close_dialog(self, obj):
        self.dialog.dismiss()

    # ------------------- DATE PICKER -----------------------
    def show_date_picker(self, var):
        date_dialog = MDDatePicker()
        if var == 1:
            date_dialog.bind(on_save=self.on_date_save_welcome, on_cancel=self.on_date_cancel)
        elif var == 2:
            date_dialog.bind(on_save=self.on_date_save_sleep, on_cancel=self.on_date_cancel)
        elif var == 3:
            date_dialog.bind(on_save=self.on_date_save_feed, on_cancel=self.on_date_cancel)
        date_dialog.open()

    def on_date_save_welcome(self, instance, value, date_range):
        formatted_date = value.strftime('%Y-%m-%d')
        self.root.get_screen('Welcome').ids.date_of_birth.text = formatted_date

    def on_date_save_sleep(self, instance, value, date_range):
        formatted_date = value.strftime('%Y-%m-%d')
        self.root.get_screen('SleepEntry').ids.sleep_date.text = formatted_date

    def on_date_save_feed(self, instance, value, date_range):
        formatted_date = value.strftime('%Y-%m-%d')
        self.root.get_screen('FeedingEntry').ids.feed_date.text = formatted_date

    def on_date_cancel(self, instance, value):
        pass

    # -------------------- TIME PICKER ---------------------
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.set_time(datetime.now())
        time_dialog.bind(time=self.on_time_save)
        time_dialog.open()

    def on_time_save(self, instance, time):
        formatted_time = time.strftime('%H:%M')
        self.root.get_screen('Welcome').ids.hour_of_birth.text = formatted_time

    def show_time_picker_for_sleep_entry(self, start):
        time_dialog = MDTimePicker()
        time_dialog.set_time(datetime.now())
        if start:
            time_dialog.bind(time=self.on_time_save_start_hour)
        else:
            time_dialog.bind(time=self.on_time_save_end_hour)
        time_dialog.open()

    def on_time_save_start_hour(self, instance, time):
        formatted_time = time.strftime('%H:%M')
        self.root.get_screen('SleepEntry').ids.start_hour.text = formatted_time

    def on_time_save_end_hour(self, instance, time):
        formatted_time = time.strftime('%H:%M')
        self.root.get_screen('SleepEntry').ids.end_hour.text = formatted_time

    def show_time_picker_for_feed(self):
        time_dialog = MDTimePicker()
        time_dialog.set_time(datetime.now())
        time_dialog.bind(time=self.on_time_save_feed)
        time_dialog.open()

    def on_time_save_feed(self, instance, time):
        formatted_time = time.strftime('%H:%M')
        self.root.get_screen('FeedingEntry').ids.feed_hour.text = formatted_time

    # ---------------------- LOGIN/REGISTER -----------------
    def create_account(self, username, password, first_name, last_name):
        conn = sqlite3.connect('baby-v.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            self.root.get_screen('Register').ids.username.line_color_normal = self.theme_cls.error_color
            self.root.get_screen('Register').ids.username.helper_text = "This username already exists"
            conn.close()
            return

        if username and password:
            c.execute("INSERT INTO users (username, password, first_name, last_name) VALUES (?, ?, ?, ?)",
                      (username, password, first_name, last_name))
            conn.commit()

            c.execute("SELECT id FROM users WHERE username=?", (username,))
            result = c.fetchone()
            self.current_user_id = result[0]

            conn.commit()
            conn.close()

            self.dialog = MDDialog(
                title="Success",
                text="Account created successfully!",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog_to_welcome
                    )
                ]
            )
            self.dialog.open()
        else:
            self.dialog = MDDialog(
                title="Error",
                text="Username or password cannot be empty",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        conn.close()

    def login(self, username, password):
        err = False
        conn = sqlite3.connect('baby-v.db')
        c = conn.cursor()

        c.execute("SELECT id, password FROM users WHERE username=?", (username,))
        result = c.fetchone()

        if result:
            user_id, stored_password = result
            if password == stored_password:
                self.root.get_screen('Login').ids.login_username.line_color_normal = self.theme_cls.primary_color
                self.root.get_screen('Login').ids.login_password.line_color_normal = self.theme_cls.primary_color
                self.current_user_id = user_id
                self.root.current = 'Home'
            else:
                err = True
        else:
            err = True

        if err:
            if username and password:
                self.root.get_screen('Login').ids.login_username.line_color_normal = self.theme_cls.error_color
                self.root.get_screen('Login').ids.login_password.line_color_normal = self.theme_cls.error_color
                self.dialog = MDDialog(
                    title="Error",
                    text="Incorect username or password!",
                    buttons=[
                        MDFlatButton(
                            text="Try again",
                            on_release=self.close_dialog_to_login
                        )
                    ]
                )
                self.dialog.open()
            elif not username and not password:
                self.root.get_screen('Login').ids.login_username.line_color_normal = self.theme_cls.error_color
                self.root.get_screen('Login').ids.login_password.line_color_normal = self.theme_cls.error_color
            elif not username:
                self.root.get_screen('Login').ids.login_username.line_color_normal = self.theme_cls.error_color
                self.root.get_screen('Login').ids.login_password.line_color_normal = self.theme_cls.primary_color
            elif not password:
                self.root.get_screen('Login').ids.login_password.line_color_normal = self.theme_cls.error_color
                self.root.get_screen('Login').ids.login_username.line_color_normal = self.theme_cls.primary_color

        conn.close()

DemoApp().run()

"""
import sounddevice as sd
import websocket
import _thread as thread
import numpy as np
import time

ws = None

def audio_callback(indata, frames, time, status):
    global ws
    if ws and ws.sock and ws.sock.connected:
        ws.send(indata.tobytes(), opcode=websocket.ABNF.OPCODE_BINARY)

def on_message(ws, message):
    print("Received message:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("### WebSocket Closed ###")

def on_open(ws):
    print("WebSocket opened")
    stream = sd.InputStream(callback=audio_callback)
    stream.start()
    print("Audio stream started")

def ensure_websocket():
    global ws
    if not ws or not ws.sock or not ws.sock.connected:
        ws = websocket.WebSocketApp("wss://192.168.0.122:5000/audio_stream",
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()

if __name__ == "__main__":
    websocket.enableTrace(True)
    thread.start_new_thread(ensure_websocket, ())
    while True:
        time.sleep(1)
"""

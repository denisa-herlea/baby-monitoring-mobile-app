from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

import sqlite3
from datetime import datetime
import asyncio
import websockets

from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder

from helper import screen_helper
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.button import MDFlatButton
import threading

import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from screen_classes.lullabies_screen import LullabiesScreen
from screen_classes.login_screen import LoginScreen
from screen_classes.register_screen import RegisterScreen
from screen_classes.welcome_screen import WelcomeScreen
from screen_classes.home_screen import HomeScreen
from screen_classes.sleep_tracking_screen import SleepTrackingScreen, SleepRecScreen, SleepReportScreen
from screen_classes.feeding_tracking_screen import FeedingTrackingScreen, FeedingReportScreen
from screen_classes.growth_health_tracking_screen import GrowthHealthTrackingScreen, LogMeasurementScreen, \
    VaccinesScreen, MeasurementReportScreen
from screen_classes.video_screen import VideoScreen
from screen_classes.sleep_entry_screen import SleepEntryScreen
from screen_classes.feeding_entry_screen import FeedingEntryScreen
from screen_classes.account_screen import AccountScreen
from screen_classes.baby_updates import UpdateBabyScreen, ChooseBabyScreen, AddNewBabyScreen

sm = ScreenManager()
sm.add_widget(LoginScreen(name='Login'))
sm.add_widget(RegisterScreen(name='Register'))
sm.add_widget(WelcomeScreen(name='Welcome'))
sm.add_widget(HomeScreen(name='Home'))
sm.add_widget(FeedingTrackingScreen(name='FeedingTracking'))
sm.add_widget(FeedingReportScreen(name='FeedingReport'))
sm.add_widget(SleepTrackingScreen(name='SleepTracking'))
sm.add_widget(SleepRecScreen(name='SleepRec'))
sm.add_widget(GrowthHealthTrackingScreen(name='GrowthHealthTracking'))
sm.add_widget(LogMeasurementScreen(name='LogMeasurement'))
sm.add_widget(VaccinesScreen(name='Vaccines'))
sm.add_widget(LullabiesScreen(name='Lullabies'))
sm.add_widget(VideoScreen(name='Video'))
sm.add_widget(SleepEntryScreen(name='SleepEntry'))
sm.add_widget(FeedingEntryScreen(name='FeedingEntry'))
sm.add_widget(AccountScreen(name='Account'))
sm.add_widget(UpdateBabyScreen(name='UpdateBaby'))
sm.add_widget(ChooseBabyScreen(name='ChooseBaby'))
sm.add_widget(AddNewBabyScreen(name='AddNewBaby'))
sm.add_widget(SleepReportScreen(name='SleepReport'))
sm.add_widget(MeasurementReportScreen(name='MeasurementReport'))

class NotificationListener:
    def __init__(self, app):
        self.app = app
        self.keep_running = False
        self.loop = None
        self.websocket_task = None

    async def connect_websocket(self):
        uri = "ws://192.168.90.187:5678"
        try:
            async with websockets.connect(uri) as websocket:
                while self.keep_running:
                    message = await websocket.recv()
                    self.app.send_notification(message)
        except Exception as e:
            print(f"WebSocket connection failed: {e}")

    def start(self):
        self.keep_running = True
        self.loop = asyncio.new_event_loop()
        self.websocket_task = threading.Thread(target=self.run_loop)
        self.websocket_task.start()

    def run_loop(self):
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self.connect_websocket())
        except Exception as e:
            print(f"Error in run_loop: {e}")
        finally:
            self.loop.close()

    def stop(self):
        self.keep_running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        if self.websocket_task:
            self.websocket_task.join()



class VideoStreamWidget(Image):
    def __init__(self, **kwargs):
        super(VideoStreamWidget, self).__init__(**kwargs)
        self.capture = None

    def start_stream(self, url):
        if self.capture is not None:
            self.capture.release()
        self.capture = cv2.VideoCapture(url)
        if not self.capture.isOpened():
            print(f"Error: Unable to open video stream from {url}")
        Clock.schedule_interval(self.update, 1.0 / 33.0)

    def stop_stream(self):
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        Clock.unschedule(self.update)

    def update(self, dt):
        if self.capture is None:
            return
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture
        else:
            print("Error: Failed to read frame from video stream")


class DemoApp(MDApp):
    current_user_id = None
    notifications_enabled = False
    notification = ""
    camera_on = False

    def build(self):
        self.theme_cls.theme_style = "Light"
        screen = Builder.load_string(screen_helper)
        self.notification_listener = NotificationListener(self)
        return screen

    def on_start(self):
        pass

    def on_stop(self):
        video_screen = self.root.get_screen('Video')
        video_widget = video_screen.ids.video_stream
        video_widget.stop_stream()

    def toggle_camera(self, is_active):
        video_screen = self.root.get_screen('Video')
        video_widget = video_screen.ids.video_stream
        if is_active:
            video_widget.start_stream('http://192.168.90.187:5000/video_feed')
            self.camera_on = True
        else:
            video_widget.stop_stream()
            self.camera_on = False

    def send_notification(self, message):
        print(f"Received notification: {message}")
        self.notification = message

        notification_bar = self.root.get_screen('Home').ids.notification_bar
        if message == "X" and self.notifications_enabled:
            notification_bar.height = 100
        else:
            notification_bar.height = 0

    def toggle_notifications(self, value):
        self.notifications_enabled = value
        if self.notifications_enabled:
            self.notification_listener.start()
        else:
            self.notification_listener.stop()
        self.update_notification_bar()

    def update_notification_bar(self):
        notification_bar = self.root.get_screen('Home').ids.notification_bar
        if self.notifications_enabled and self.notification == "X":
            notification_bar.height = 100
        else:
            notification_bar.height = 0

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
        elif var == 4:
            date_dialog.bind(on_save=self.on_date_save_update_baby, on_cancel=self.on_date_cancel)
        elif var == 5:
            date_dialog.bind(on_save=self.on_date_add_baby, on_cancel=self.on_date_cancel)
        elif var == 6:
            date_dialog.bind(on_save=self.on_date_add_measurement, on_cancel=self.on_date_cancel)
        date_dialog.open()

    def on_date_save_welcome(self, instance, value, date_range):
        formatted_date = value.strftime('%Y-%m-%d')
        self.root.get_screen('Welcome').ids.date_of_birth.text = formatted_date

    def on_date_add_measurement(self, instance, value, date_range):
        formatted_date = value.strftime('%Y-%m-%d')
        self.root.get_screen('LogMeasurement').ids.measurement_date.text = formatted_date

    def on_date_add_baby(self, instance, value, date_range):
        formatted_date = value.strftime('%Y-%m-%d')
        self.root.get_screen('AddNewBaby').ids.date_of_birth.text = formatted_date

    def on_date_save_sleep(self, instance, value, date_range):
        formatted_date = value.strftime('%Y-%m-%d')
        self.root.get_screen('SleepEntry').ids.sleep_date.text = formatted_date

    def on_date_save_feed(self, instance, value, date_range):
        formatted_date = value.strftime('%Y-%m-%d')
        self.root.get_screen('FeedingEntry').ids.feed_date.text = formatted_date

    def on_date_save_update_baby(self, instance, value, date_range):
        formatted_date = value.strftime('%Y-%m-%d')
        self.root.get_screen('UpdateBaby').ids.date_of_birth.text = formatted_date

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

    def show_time_picker_for_update_baby(self):
        time_dialog = MDTimePicker()
        time_dialog.set_time(datetime.now())
        time_dialog.bind(time=self.on_time_save_update_baby)
        time_dialog.open()

    def show_time_picker_add_baby(self):
        time_dialog = MDTimePicker()
        time_dialog.set_time(datetime.now())
        time_dialog.bind(time=self.on_time_add_baby)
        time_dialog.open()

    def on_time_save_update_baby(self, instance, time):
        formatted_time = time.strftime('%H:%M')
        self.root.get_screen('UpdateBaby').ids.hour_of_birth.text = formatted_time

    def on_time_add_baby(self, instance, time):
        formatted_time = time.strftime('%H:%M')
        self.root.get_screen('AddNewBaby').ids.hour_of_birth.text = formatted_time

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

import asyncio
import websockets
import numpy as np
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle
import sounddevice as sd
import threading

class VideoScreen(Screen):
    icon_speaker = StringProperty("volume-off")
    icon_audio = StringProperty("microphone-off")
    speaker_on = False
    audio_on = False
    ws_send_audio = None
    ws_receive_audio = None
    loop = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        threading.Thread(target=self.loop.run_forever).start()

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    async def connect_to_server_for_audio(self):
        uri = "ws://192.168.90.187:5679"

        try:
            async with websockets.connect(uri) as websocket:
                self.ws_receive_audio = websocket
                print("Connected to server for audio")
                while self.speaker_on and self.ws_receive_audio.open:
                    try:
                        message = await self.ws_receive_audio.recv()
                        print("Audio received")
                        audio_data = np.frombuffer(message, dtype=np.float32)
                        print("Playing audio")
                        sd.play(audio_data, samplerate=16000)
                        sd.wait()
                    except websockets.ConnectionClosed:
                        print("WebSocket connection closed by server")
                        break
                    except Exception as e:
                        print(f"An error occurred while receiving audio: {e}")
                        break
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
        finally:
            print("WebSocket connection closed")
            self.ws_receive_audio = None

    async def connect_to_server_for_sending_audio(self):
        uri = "ws://192.168.90.187:5680"

        try:
            async with websockets.connect(uri) as websocket:
                self.ws_send_audio = websocket
                print("Connected to server for sending audio")
                while self.audio_on and self.ws_send_audio.open:
                    try:
                        print("Recording audio...")
                        audio_data = sd.rec(int(1.5 * 16000), samplerate=16000, channels=1, dtype="float32")
                        sd.wait()
                        audio_bytes = audio_data.tobytes()
                        print("Sending audio...")
                        await self.ws_send_audio.send(audio_bytes)
                        print("Audio sent")
                    except websockets.ConnectionClosed:
                        print("WebSocket connection closed by server")
                        break
                    except Exception as e:
                        print(f"An error occurred while sending audio: {e}")
                        break
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
        finally:
            print("WebSocket connection closed")
            self.ws_send_audio = None

    def toggle_icon_speaker(self):
        self.speaker_on = not self.speaker_on
        self.icon_speaker = "volume" if self.speaker_on else "volume-off"
        if self.speaker_on:
            asyncio.run_coroutine_threadsafe(self.connect_to_server_for_audio(), self.loop)
        else:
            if self.ws_receive_audio:
                asyncio.run_coroutine_threadsafe(self.ws_receive_audio.close(), self.loop)

    def toggle_icon_audio(self):
        self.audio_on = not self.audio_on
        self.icon_audio = "microphone" if self.audio_on else "microphone-off"
        if self.audio_on:
            asyncio.run_coroutine_threadsafe(self.connect_to_server_for_sending_audio(), self.loop)
        else:
            if self.ws_send_audio:
                asyncio.run_coroutine_threadsafe(self.ws_send_audio.close(), self.loop)

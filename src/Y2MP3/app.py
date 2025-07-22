from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import yt_dlp, pathlib, threading, os

class Y2MP3App(App):
    def build(self):
        box = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.url = TextInput(hint_text='ألصق الرابط', multiline=False)
        btn_mp3 = Button(text='حوّل إلى MP3', on_release=self.download_mp3)
        btn_mp4 = Button(text='حمّل MP4', on_release=self.download_mp4)
        self.label = Label(text='جاهز')

        box.add_widget(self.url)
        box.add_widget(btn_mp3)
        box.add_widget(btn_mp4)
        box.add_widget(self.label)
        return box

    def download_mp3(self, _):
        self.download("mp3")

    def download_mp4(self, _):
        self.download("mp4")

    def download(self, mode):
        url = self.url.text.strip()
        if not url:
            self.label.text = "ألصق رابطاً"
            return
        threading.Thread(target=self._dl, args=(url, mode)).start()

    def _dl(self, mode):
        storage = pathlib.Path("/sdcard/Download")
        storage.mkdir(exist_ok=True)
        ydl_opts = {
            "outtmpl": str(storage / f"%(title)s.{mode}"),
            "format": "bestaudio/best" if mode == "mp3" else "bestvideo+bestaudio",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}] if mode == "mp3" else [],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.label.text = "تم الحفظ!"
        except Exception as e:
            self.label.text = str(e)

if __name__ == "__main__":
    Y2MP3App().run()
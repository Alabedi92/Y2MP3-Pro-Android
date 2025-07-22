import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import yt_dlp, pathlib, threading

class Y2MP3App(toga.App):
    def startup(self):
        box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        self.url = toga.TextInput(placeholder="ألصق الرابط")
        btn = toga.Button("حمل MP3", on_press=self.download)
        box.add(self.url)
        box.add(btn)
        self.main_window = toga.MainWindow(title="Y2MP3-Pro")
        self.main_window.content = box
        self.main_window.show()

    def download(self, widget):
        url = self.url.value.strip()
        if not url:
            return
        threading.Thread(target=self._dl, args=(url,)).start()

    def _dl(self, url):
        storage = pathlib.Path.home() / "Download"
        ydl_opts = {
            "outtmpl": str(storage / "%(title)s.mp3"),
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            pass

def main():
    return Y2MP3App()
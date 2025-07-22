import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import yt_dlp, pathlib, threading, os

APP_NAME = "Y2MP3-Pro"
DESIGNER = "د. علي العابدي"

class Y2MP3Pro(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        self.url_input = toga.TextInput(placeholder="ألصق الرابط")
        self.status = toga.Label("جاهز")

        mp3_btn = toga.Button("حوّل إلى MP3", on_press=self.download_mp3)
        mp4_btn = toga.Button("حمّل MP4", on_press=self.download_mp4)

        main_box.add(self.url_input)
        main_box.add(mp3_btn)
        main_box.add(mp4_btn)
        main_box.add(self.status)

        self.main_window = toga.MainWindow(title=APP_NAME)
        self.main_window.content = main_box
        self.main_window.show()

    def download_mp3(self, widget):
        self.download("mp3")

    def download_mp4(self, widget):
        self.download("mp4")

    def download(self, mode):
        url = self.url_input.value.strip()
        if not url:
            self.status.text = "ألصق رابطاً"
            return
        threading.Thread(target=self._download, args=(url, mode)).start()

    def _download(self, url, mode):
        storage = pathlib.Path.home() / "Download"
        storage.mkdir(exist_ok=True)
        ydl_opts = {
            "outtmpl": str(storage / f"%(title)s.{mode}"),
            "format": "bestaudio/best" if mode == "mp3" else "bestvideo+bestaudio/best[height<=720]",
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "320"}
            ] if mode == "mp3" else [],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.main_window.info_dialog("انتهى", f"تم الحفظ إلى {storage}")
        except Exception as e:
            self.main_window.info_dialog("خطأ", str(e))

def main():
    return Y2MP3Pro()
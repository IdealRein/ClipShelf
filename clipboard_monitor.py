import pyperclip
import time

class ClipboardMonitor:
    def __init__(self, on_new_clip_callback):
        self.last_clip = ""
        self.on_new_clip = on_new_clip_callback

    def run(self):
        while True:
            try:
                clip = pyperclip.paste()
                if clip != self.last_clip:
                    self.last_clip = clip
                    self.on_new_clip(clip)
                time.sleep(1)
            except:
                continue


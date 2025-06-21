import threading
import os
from ui import ClipUI
from clipboard_monitor import ClipboardMonitor

if __name__ == '__main__':
    STORAGE_PATH = os.path.join(os.path.dirname(__file__), 'storage.json')
    ui = ClipUI(STORAGE_PATH)
    monitor = ClipboardMonitor(ui.add_clip)

    monitor_thread = threading.Thread(target=monitor.run, daemon=True)
    monitor_thread.start()

    ui.run()
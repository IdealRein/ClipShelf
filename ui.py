import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import json
import os

class ClipUI:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.clip_list = self.load_history()

        self.root = tk.Tk()
        self.root.title("ClipShelf - 剪贴板历史")
        self.root.geometry("600x500")

        self.display = ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 11))
        self.display.pack(fill=tk.BOTH, expand=True)
        self.display.bind('<Double-1>', self.on_select)

        self.refresh_display()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_clip(self, text):
        if not text.strip():
            return
        if not any(clip['text'] == text for clip in self.clip_list):
            self.clip_list.insert(0, {"time": self.timestamp(), "text": text})
            self.refresh_display()
            self.save_history()

    def refresh_display(self):
        self.display.delete(1.0, tk.END)
        for clip in self.clip_list:
            self.display.insert(tk.END, "-" * 40 + "\n")
            self.display.insert(tk.END, f"[{clip['time']}]\n")
            self.display.insert(tk.END, clip['text'] + "\n\n")
        self.display.see(tk.END)

    def on_select(self, event):
        index = self.display.index(tk.CURRENT)
        line = self.display.get(f"{index} linestart", f"{index} lineend").strip()
        # 从当前位置向上查找最近的内容段落
        lines = self.display.get("1.0", tk.END).split("\n")
        current_line_num = int(index.split('.')[0])
        selected_text = ""
        for i in range(current_line_num - 1, -1, -1):
            if lines[i].startswith("----------------------------------------"):
                break
            selected_text = lines[i] + "\n" + selected_text
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text.strip())

    def timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def load_history(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.clip_list, f, ensure_ascii=False, indent=2)
        except:
            pass

    def on_close(self):
        self.save_history()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
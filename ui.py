import tkinter as tk
import json
import os

class ClipUI:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.clip_list = self.load_history()

        self.root = tk.Tk()
        self.root.title("ClipShelf - 剪贴板历史")
        self.root.geometry("500x400")

        self.listbox = tk.Listbox(self.root, width=60, height=20)
        self.listbox.pack(pady=10)
        self.listbox.bind('<Double-1>', self.on_select)

        self.refresh_list()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_clip(self, text):
        if text not in self.clip_list:
            self.clip_list.insert(0, text)
            self.refresh_list()
            self.save_history()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for item in self.clip_list:
            self.listbox.insert(tk.END, item[:60])

    def on_select(self, event):
        index = self.listbox.curselection()
        if index:
            selected = self.clip_list[index[0]]
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)

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
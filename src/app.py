import tkinter as tk
from src.config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # In a message to confirm it's running
        label = tk.Label(self, text="KaGo đã sẵn sàng!", font=("Arial", 18))
        label.pack(pady=100)
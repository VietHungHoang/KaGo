import tkinter as tk
from src.config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        
        self.center_window()

        # In a message to confirm it's running
        label = tk.Label(self, text="Cửa sổ chính của KaGo đã sẵn sàng!", font=("Arial", 18))
        label.pack(pady=100)

    """Caculate and set position to make the window appear centered on the screen"""
    def center_window(self):
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate x, y coordinates
        x_coordinate = int((screen_width / 2) - (WINDOW_WIDTH / 2))
        y_coordinate = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

        # Set the window geometry with the new position
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_coordinate}+{y_coordinate}")
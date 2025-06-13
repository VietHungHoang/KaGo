import tkinter as tk
from src.config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from src.views.home_frame import HomeFrame

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.center_window()

        # Create a main content where all the other frames (screens) will be stacked
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store the frames
        self.frames = {}

        # Create and add HomeFrame to the dictionary
        frame = HomeFrame(container, self)
        self.frames[HomeFrame] = frame
        frame.grid(row=0, column=0, sticky="nsew") # nsew = north, south, east, west

        # Show the first frame
        self.show_frame(HomeFrame)

    def show_frame(self, frame_class):
        """Show a created frame"""
        frame = self.frames[frame_class]
        frame.tkraise() # Raise the selected frame to the top.

    def center_window(self):
        """Caculate and set the position to make the window in the center of the screen"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (WINDOW_WIDTH / 2))
        y_coordinate = int((screen_height / 2) - (WINDOW_HEIGHT / 2))
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_coordinate}+{y_coordinate}")
import tkinter as tk
from tkinter import messagebox
from src.config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from src.views.home_frame import HomeFrame
from src.views.lesson_list_frame import LessonListFrame
from src.views.practice_frame import PracticeFrame
from src.services.lesson_service import LessonService

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.center_window()

        self.lesson_service = LessonService()

        # Create a main content where all the other frames (screens) will be stacked
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=(12, 2), pady=(0, 16))
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store the frames
        self.frames = {}

        # Create and add all frames to the dictionary
        for F in (HomeFrame, LessonListFrame, PracticeFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame # Use the Class name as the key
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame_by_class_name("HomeFrame")

    def start_practice_session(self, lesson_id):
        """Coordinator method to start a practice session"""
        lesson = self.lesson_service.get_lesson_by_id(lesson_id)
        if lesson and lesson.cards:
            practice_frame = self.frames["PracticeFrame"]
            practice_frame.start_session(lesson)
            self.show_frame_by_class_name("PracticeFrame")
        else:
            messagebox.showerror("Lỗi!", f"Không thể tải bài học {lesson_id} hoặc bài học không có câu hỏi nào.")


    def show_frame_by_class_name(self, class_name):
        """Show a created frame based on its class name"""
        frame = self.frames[class_name]
        frame.tkraise() # Raise the selected frame to the top.

    def center_window(self):
        """Caculate and set the position to make the window in the center of the screen"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (WINDOW_WIDTH / 2))
        y_coordinate = int((screen_height / 2) - (WINDOW_HEIGHT / 2))
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_coordinate}+{y_coordinate}")


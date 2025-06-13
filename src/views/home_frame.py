import tkinter as tk
from tkinter import ttk, messagebox

class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        """Initialize the HomeFrame"""
        # :param parent: The parent widget (the container in the main app)
        # :param controller: The main Application object to call its methods (e.g., switching frames)
        super().__init__(parent)
        self.controller = controller

        """--- Interface ---"""

        # Create a content frame for easy centering
        content_frame = ttk.Frame(self)
        # Allows this frame take up exra space
        content_frame.pack(expand=True) 

        # Create styles for widgets
        style = ttk.Style(self)
        style.configure("TButton", font=("Arial", 14), padding=10, width=20)
        style.configure("Header.TLabel", font=("Arial", 32, "bold"))

        # App header
        header_label = ttk.Label(content_frame, text="KaGo", style="Header.TLabel")
        header_label.pack(pady=(20, 40)) # (khoảng cách trên, khoảng cách dưới)

        # Function buttons
        practice_button = ttk.Button(
            content_frame,
            text="Luyện tập",
            command=lambda: print("Go to the practice screen"),
            style="TButton"
        )
        practice_button.pack(pady=10)

        ai_practice_button = ttk.Button(
            content_frame,
            text="Luyện tập với AI",
            command=lambda: messagebox.showinfo("Thông báo", "Tính năng sẽ sớm ra mắt!"),
            style="TButton"
        )
        ai_practice_button.pack(pady=10)

        settings_button = ttk.Button(
            content_frame,
            text="Cài đặt",
            command=lambda: messagebox.showinfo("Thông báo", "Tính năng sẽ sớm ra mắt!"),
            style="TButton"
        )
        settings_button.pack(pady=10)
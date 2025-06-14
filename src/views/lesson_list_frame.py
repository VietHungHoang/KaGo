import tkinter as tk
from tkinter import ttk, messagebox
from src.services.lesson_service import LessonService

class LessonListFrame(tk.Frame):
    def __init__(self, parent, controller):
        """Initalize the frame"""
        super().__init__(parent)
        self.controller = controller

        # Initialize lesson service
        self.lesson_service = LessonService()

        """--- Config layout with grid ---"""
        # Column 1 (the list) will take up all extra horizontal space
        self.grid_columnconfigure(1, weight=1) 
        # Row 2 (the list) will take up all extra vertical space
        self.grid_rowconfigure(2, weight=1) 

        # --- Widgets ---   

        # Back button and Header
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        top_frame.config(height=80)
        top_frame.grid_propagate(False)
        
        back_button = ttk.Button(top_frame, text="Quay lại", width=7, command=lambda: self.controller.show_frame_by_class_name("HomeFrame"))
        back_button.place(relx=0.0, rely=0.5, anchor="w")

        header_label = ttk.Label(top_frame, text="Các bài luyện tập", font=("Arial", 28, "bold"))
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        # Search bar and Add new button
        search_frame = ttk.Frame(self)
        search_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 10))
        search_frame.grid_columnconfigure(0, weight=1)

        search_entry = ttk.Entry(search_frame, font=("Arial", 16))
        search_entry.grid(row=0, column=0, sticky="ew", ipady=8)

        add_new_button = ttk.Button(search_frame, text="Thêm mới", width=8, command=self.add_new_lesson)
        add_new_button.grid(row=0, column=1, padx=(10, 12))
        
        # Frame to contain the list of lessons (using a Treeview)
        # Set custom style for Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=30, padding=[10, 0])
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

        columns = ('lesson_name', 'progress')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        
        # Define the columns
        self.tree.heading('lesson_name', text='Tên bài học')
        self.tree.heading('progress', text='Tiến độ')
        self.tree.column('progress', width=100, anchor=tk.CENTER)

        # Add sample data
        sample_lessons = [
            ("Từ vựng N5 - Bài 1", "25%"),
            ("Kanji sơ cấp", "78%"),
            ("Ngữ pháp Minna no Nihongo - Bài 10", "0%"),
            ("Từ vựng N4 - Động từ", "100%")
        ]

        for lesson in sample_lessons:
            self.tree.insert('', tk.END, values=lesson)
        
        self.tree.grid(row=2, column=0, columnspan=3, sticky='nsew', padx=10)
        # Register listening event
        self.tree.bind('<<TreeviewSelect>>', self.on_lesson_select)

        # Add scroll bar for list
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=2, sticky='ns', padx=(0,10))
        
        # Load intital data
        self.load_lessons()

    def add_new_lesson(self):
        """Even handler method for 'Thêm mới' buttonn click"""
        new_lesson, message = self.lesson_service.import_lesson_from_csv()
        
        if new_lesson:
            # If success, add to the Treeview and show a success message
            self.tree.insert('', tk.END, values=(new_lesson.name, f"{new_lesson.progress_percent}%"))
            messagebox.showinfo("Thành công", message)
        elif message:
            # If failed, show an error message
            messagebox.showerror("Lỗi", message)

    def load_lessons(self):
        """Load all lessons from the service"""

        # Delete existing item to refresh
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get the list of lessons from service
        all_lessons = self.lesson_service.get_all_lessons()
        
        # Iterate through each lesson and add it to the Treeview
        if not all_lessons:
            # Display a message if there are no lessons yet
            self.tree.insert('', tk.END, values=("Chưa có bài học nào. Hãy thêm một bài mới!", ""), tags=('placeholder',))
            self.tree.tag_configure('placeholder', foreground='grey')
        else:
            for lesson in all_lessons:
                self.tree.insert('', tk.END, iid=lesson.id, values=(lesson.name, f"{lesson.progress_percent}%"))

    def on_lesson_select(self, event):
        """"Event handler for when a lesson is selected """
        selected_items = self.tree.selection()
        if not selected_items: 
            return

        lesson_id = selected_items[0]
        self.controller.start_practice_session(lesson_id)





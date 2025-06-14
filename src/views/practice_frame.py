import tkinter as tk
from tkinter import ttk

class PracticeFrame(tk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller
		self.current_lesson = None
		self.current_card_index = 0

		""" --- Layout config --- """

		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)

		""" --- Widgets --- """

		# Back button
		top_bar = ttk.Frame(self)
		top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(24, 24))
		quit_button = ttk.Button(top_bar, text="Thoát", width=5, command=lambda: self.controller.show_frame_by_class_name("LessonListFrame"))
		quit_button.pack(side="left")

		# Main frame contain question
		main_content_frame = ttk.Frame(self)
		main_content_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 20), pady=30)
		main_content_frame.grid_columnconfigure(0, weight=1)

		# Question label
		question_frame = ttk.Frame(main_content_frame)
		question_frame.pack(fill="x", pady=(20, 20))

		self.question_label = ttk.Label(question_frame, text="Question", font=("Arial", 36, "bold"), anchor="center")
		self.question_label.pack(expand=True, fill="x")

		# Input field
		self.answer_entry = ttk.Entry(main_content_frame, font=("Arial", 20))
		self.answer_entry.pack(fill="x", ipady=10)

		# Result 
		self.result_label = ttk.Label(main_content_frame, text="", font=("Arial", 20), anchor="center")
		self.result_label.pack(pady=10)

		# Explanation
		self.explanation_label = ttk.Label(main_content_frame, text="", font=("Arial", 20, "italic"), anchor="center", wraplength=500)
		self.explanation_label.pack(pady=10)

		# Show romaji button
		self.romaji_button = ttk.Button(main_content_frame, text="Romaji")

	def start_session(self, lesson):
		"""Start learning sesson"""
		self.current_lesson = lesson
		self.show_next_card()

	def show_next_card(self):
		"""Show the next question"""
		# For now, display the first card
		if self.current_lesson and self.current_lesson.cards:
			card = self.current_lesson.cards[self.current_card_index]
			self.question_label.config(text=card.question)
		else:
			self.question_label.config(text="Không có câu hỏi nào trong bài học này.")


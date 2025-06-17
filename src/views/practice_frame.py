import tkinter as tk
from tkinter import ttk, messagebox
import random
from src.services.text_service import TextService

class PracticeFrame(tk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller
		self.init_variables()
		self.init_ui()

	def init_ui(self):
		"""Initialize the UI components"""
		""" --- Layout config --- """

		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)

		""" --- Widgets --- """

		# Back button
		top_bar = ttk.Frame(self)
		top_bar.grid(row=0, column=0, sticky="ew", padx=200, pady=(48, 0))
		quit_button = ttk.Button(top_bar, text="Thoát", width=5, command=self.quit_session)
		quit_button.pack(side="left")

		# Main frame contain question
		main_content_frame = ttk.Frame(self)
		main_content_frame.grid(row=1, column=0, sticky="nsew", padx=200, pady= (100, 20))
		main_content_frame.grid_columnconfigure(0, weight=1)

		# Question label
		question_frame = ttk.Frame(main_content_frame)
		question_frame.pack(fill="x", pady=(20, 10))

		self.question_label = ttk.Label(question_frame, text="...", font=("Arial", 36, "bold"), anchor="center", wraplength=1200)
		self.question_label.pack(pady=(20, 10), fill="x")

		# Input field
		self.answer_entry = ttk.Entry(main_content_frame, font=("Arial", 32))
		self.answer_entry.pack(fill="x", ipady=10, pady=16, padx=8)
		self.answer_entry.bind("<Return>", self.check_answer_or_continue)

		# Result 
		self.result_label = ttk.Label(main_content_frame, text="", font=("Arial", 28, "bold"), anchor="center", justify="center")
		self.result_label.pack(pady=(20, 10))
		self.result_label.bind("<Button-1>", self.convert_answer)

		# Explanation
		self.explanation_label = ttk.Label(main_content_frame, text="", font=("Arial", 20, "italic"), anchor="center", wraplength=1000)

		# Show romaji button
		self.explanation_button = ttk.Button(main_content_frame, text="Giải thích", command=self.show_explanation)
  
	def init_variables(self):
		"""Initialize variables for the learning session"""
		self.current_lesson = None
		self.current_card = None
		self.waiting_for_next_card = False
  
		self.text_service = TextService()
		self.practice_service = self.controller.practice_service
  
	def start_session(self, lesson, streak_of_cards):
		"""Start learning sesson"""
		self.current_lesson = lesson
		self.streak_of_cards = streak_of_cards
		self.show_next_card()
  
	def show_next_card(self):
		"""Show the next question"""
		self.reset_ui_for_new_card()
		self.streak_of_cards = {k:v for k, v in self.streak_of_cards.items() if v < self.practice_service.required_streak_for_mastery}

		if not self.streak_of_cards:
			self.quit_session(completed=True) # Exit when completed
			return

		key = random.choice(list(self.streak_of_cards.keys()))
		self.current_card = self.current_lesson.get_card_by_hash(key)
		self.question_label.config(text=self.current_card.question)

	def check_answer_or_continue(self, event=None):
		# Check the answer or continue after a wrong answer
		if self.waiting_for_next_card:
			self.show_next_card()
			return

		user_answer = self.answer_entry.get().strip()
		if not user_answer:
			return

		self.answer_entry.config(state="readonly")  # Disable input while checking

		# Normalize the user's answer and the correct answers
		normalized_user_answer = self.text_service.normalize_japanese_text(user_answer)
		correct_answers = [self.text_service.normalize_japanese_text(ans) for ans in self.current_card.answer.split(';')]

		is_correct = normalized_user_answer in correct_answers

		# Display result
		if is_correct:
			self.result_label.config(text="Đúng!", foreground="green")
			self.streak_of_cards[self.current_card.get_hash()] += 1
			
			# Automatically move to the next card after 2 seconds
			self.after(2000, self.show_next_card)
		else:
			self.result_label.config(text=f"Sai!\n {self.current_card.answer}", foreground="red")
			# Set the waiting flag, requiring the user to press Enter to continue.
			self.waiting_for_next_card = True
		if self.current_card.explanation:
			self.explanation_button.pack()

	def show_explanation(self):
		# Show the explanation for the current card
		self.explanation_button.pack_forget()
		self.explanation_label.config(text=self.current_card.explanation)
		self.explanation_label.pack(pady=10)

	def reset_ui_for_new_card(self):
		# Clean up the UI for the new question
		self.waiting_for_next_card = False
		self.result_label.config(text="")
		self.explanation_label.pack_forget() # Hide explanation label
		self.explanation_button.pack_forget() # Hidden explanation button
		self.answer_entry.config(state="normal")
		self.answer_entry.delete(0, tk.END)
		self.answer_entry.focus_set() # Automatically focus to entry

	def quit_session(self, completed=False):
		self.practice_service.update_lesson_progress(self.current_lesson.id, self.streak_of_cards)
		if completed:
			messagebox.showinfo("Hoàn thành", "Chúc mừng! Bạn đã hoàn thành tất cả các thẻ trong bài học này!")

		self.controller.frames["LessonListFrame"].load_lessons()
		self.controller.show_frame_by_class_name("LessonListFrame")
  
	def convert_answer(self, event=None):
		# Translate the user's answer using the text service
		try:
			answer = self.result_label["text"][6::]
			if answer == self.current_card.answer:
				answer = self.text_service.normalize_japanese_text(self.current_card.answer)
			else:
				answer = self.current_card.answer
			self.result_label.config(text=f"Sai!\n {answer}", foreground="red")
		except Exception:
			print("Error: ", Exception)
		
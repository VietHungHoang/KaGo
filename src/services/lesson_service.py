import csv
import os
import shutil
import json
from pathlib import Path
from tkinter import filedialog
from src.models.lesson import Lesson
from src.models.card import Card

class LessonService:
    def __init__(self):
        # Define important paths
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.lessons_dir = self.base_dir / "data" / "lessons"
        self.progress_dir = self.base_dir / "data" / "progress"
        # Ensure these directories exist
        self.lessons_dir.mkdir(parents=True, exist_ok=True)
        self.progress_dir.mkdir(parents=True, exist_ok=True)

    def import_lesson_from_csv(self):
        # Open select file dialog
        filepath = filedialog.askopenfilename(
            title="Chọn file CSV bài học",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filepath:
            return None, "Không có file nào được chọn."

        try:
            # Create new filename and destination path
            original_filename = Path(filepath).name
            new_csv_path = self.lessons_dir / original_filename
            
            if new_csv_path.exists():
                return None, f"Lỗi: Bài học '{original_filename}' đã tồn tại."

            # Read csv file to validate and get card data
            cards = self._read_cards_from_csv(filepath)
            if not cards:
                return None, "Lỗi: File CSV trống hoặc sai định dạng (cần cột 'question' và 'answer')."

            # If valid, copy CSV file to the data directory
            shutil.copy(filepath, new_csv_path)

            # Create the JSON progress file
            lesson_id = new_csv_path.stem
            self._create_progress_file(lesson_id, cards)

            # Create a new Lesson object to return
            lesson_name = lesson_id.replace("_", " ").title()
            new_lesson = Lesson(lesson_id, lesson_name, str(new_csv_path))
            new_lesson.cards = cards
            
            return new_lesson, "Thêm bài học thành công!"

        except Exception as e:
            return None, f"Đã xảy ra lỗi: {e}"


    def get_all_lessons(self):
        """Get a list of all existing lessons"""
        lessons = []
        # Scan all CSV files in the lessons directory
        for csv_path in self.lessons_dir.glob("*.csv"):
            lesson_id = csv_path.stem
            
            # Create a simple Lesson object
            lesson_name = lesson_id.replace("_", " ").title()
            lesson = Lesson(lesson_id, lesson_name, str(csv_path))
            
            # Read the corresponding file progress to update progress
            progress_data = self._read_progress_file(lesson_id)
            if progress_data:
                lesson.progress_percent = self._calculate_completion_percent(progress_data)
            
            lessons.append(lesson)
        
        return lessons

    def _read_progress_file(self, lesson_id):
        # Read the content from the JSON progress file
        progress_path = self.progress_dir / f"progress_{lesson_id}.json"
        if not progress_path.exists():
            return None
        
        try:
            with open(progress_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def _calculate_completion_percent(self, progress_data):
        # Caculates the completion percentage
        # This feature will be improved later
        # For now, mock with 1
        required_streak = 1
        
        progress_map = progress_data.get("current_progress", {})
        if not progress_map:
            return 0

        completed_cards = 0
        for card_hash, card_data in progress_map.items():
            if card_data.get("correct_streak", 0) >= required_streak:
                completed_cards += 1
        
        total_cards = len(progress_map)
        if total_cards == 0:
            return 0
        
        return int((completed_cards / total_cards) * 100)

    def _read_cards_from_csv(self, filepath):
        cards = []
        with open(filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Convert header names to lowercase for flexibility
            reader.fieldnames = [field.lower() for field in reader.fieldnames]
            
            if 'question' not in reader.fieldnames or 'answer' not in reader.fieldnames:
                return []

            for i, row in enumerate(reader):
                card = Card(
                    id_in_lesson=i,
                    question=row.get('question', ''),
                    answer=row.get('answer', ''),
                    explanation=row.get('explanation', '')
                )
                cards.append(card)
        return cards

    def _create_progress_file(self, lesson_id, cards):
        progress_path = self.progress_dir / f"progress_{lesson_id}.json"
        
        progress_data = {
            "lesson_id": lesson_id,
            "total_cards": len(cards),
            "current_progress": {
                card.get_hash(): {"correct_streak": 0} for card in cards
            },
            "session_history": []
        }
        
        with open(progress_path, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
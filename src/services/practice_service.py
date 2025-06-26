import json
from pathlib import Path

class PracticeService:
    def __init__(self):
        # Determine the paths
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.progress_dir = self.base_dir / "data" / "progress"
        
        # UPDATE: Get setup from config
        self.required_streak_for_mastery = 3 # Mock data 

    def get_streak_of_cards(self, lesson_id, all_cards, start_over=False):
        """"Get the list of cards to practice for a lesson"""
        progress_data = self._read_progress_file(lesson_id)
        if not progress_data or start_over:
            return {card.get_hash(): 0 for card in all_cards}  # Reset progress if no data or start_over

        # Fiter incompleted cards (active c)
        cards_streaks = {}
        progress_map = progress_data.get("current_progress", {})
        
        for card in all_cards:
            card_hash = card.get_hash()
            card_progress = progress_map.get(card_hash, {"correct_streak": 0})
            if card_progress["correct_streak"] < self.required_streak_for_mastery:
                cards_streaks[card_hash] = card_progress["correct_streak"]
        
        return cards_streaks 

    def update_lesson_progress(self, lesson, streak_of_cards):
        # Update progress for a specific card in a lesson
        progress_data = self._read_progress_file(lesson.id)
        if not progress_data:
            return

        progress_map = progress_data.get("current_progress", {})
        for card_hash in progress_map:
            streak = streak_of_cards.get(card_hash, 3)
            progress_map[card_hash]["correct_streak"] = streak
            progress_map[card_hash]["correct"] = lesson.get_card_by_hash(card_hash).correct
            progress_map[card_hash]["incorrect"] = lesson.get_card_by_hash(card_hash).incorrect

        self._save_progress_file(lesson.id, progress_data)

    def reset_lesson_progress(self, lesson_id):
        # Reset the progress for a lesson
        progress_data = self._read_progress_file(lesson_id)
        if not progress_data:
            return
        
        progress_map = progress_data.get("current_progress", {})
        for card_hash in progress_map:
            progress_map[card_hash]["correct_streak"] = 0
            
        # UPDATE: Save history of progress
        self._save_progress_file(lesson_id, progress_data)

    def _read_progress_file(self, lesson_id):
        progress_path = self.progress_dir / f"progress_{lesson_id}.json"
        if not progress_path.exists():
            return None
        try:
            with open(progress_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def _save_progress_file(self, lesson_id, data):
        progress_path = self.progress_dir / f"progress_{lesson_id}.json"
        try:
            with open(progress_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Lỗi khi lưu file progress: {e}")
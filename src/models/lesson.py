class Lesson:
    def __init__(self, lesson_id, name, csv_path):
        """Initialize a lesson"""
        self.id = lesson_id # Unique identifier
        self.name = name
        self.csv_path = csv_path
        self.cards = []
        self.progress_percent = 0

    def __repr__(self):
        return f"Lesson(ID: {self.id}, Name: {self.name}, Cards: {len(self.cards)})"
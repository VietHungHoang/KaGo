import hashlib

class Card:
    def __init__(self, question, answer, explanation, id_in_lesson=0):
        # Initialize a learning card 
        self.id_in_lesson = id_in_lesson # The sequence number of the card within the lesson
        self.question = str(question).strip()
        self.answer = str(answer).strip()
        self.explanation = str(explanation).strip()
    
    def get_hash(self):
        """Create a unique identifier for this card based on its content to track 
        the card's progress even if the sequence number changes"""
        unique_string = f"{self.question}|{self.answer}"
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()

    def __repr__(self):
        # For debugging
        return f"Card(Q: {self.question}, A: {self.answer})"
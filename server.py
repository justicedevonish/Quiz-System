from pymongo import MongoClient

class User:
    def __init__(self):
        self.correct_answers = 0

    def increment_correct_answers(self):
        self.correct_answers += 1

client = MongoClient('mongodb://localhost:27017')
db = client['QuizQuestions']  
collection = db['Questions']  
user_info = db['Users']

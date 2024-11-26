from server import user_info, collection, User
import time
# import variables from server.py file

username = ' '
password = ' '


new_user = str(input("New or Previous User? (New/Previous): "))
new_user.lower()

while new_user == 'new':
    username = str(input("Enter Username: "))
    existing_user = user_info.find_one({"username": username})
    if existing_user:
        print("Username already exists. Please choose a different username.")
    else:
        password = str(input("Enter Password: "))
        print("New User Created ", end=' ')
        print(f"Welcome to the quiz {username}")
        user_info.insert_one({"username": username, "password": password})
        new_user = None
        pass
        
if new_user == 'previous':
    username = str(input("Enter Username: "))
    password = str(input("Enter Password: "))
    existing_user = user_info.find_one({"username": username, "password": password})
    if existing_user:
        print(f"Welcome back {username} !!!!")
    else:
        print("Invalid username and password")
        exit()


    
previous_scores = str(input("Would you like to take a new quiz or see previous scores? (New/Previous Scores)"))
previous_scores.lower()

if previous_scores == 'new':
    pass
elif previous_scores == 'previous scores' or previous_scores == 'previous':
    user_data = user_info.find_one({"username": username})
    if user_data and "scores" in user_data:
        print("Previous Scores:")
        print(user_data["scores"])
    else:
        print("No previous scores found.")
        print("\n")
        print("\n")
num_questions = int(input("How many questions would you like to answer? "))
print("\n")
if num_questions > 10:
    print("Number has to be lower than 10.")

timer_count = num_questions * .25

#countdown(timer_count)


questions = collection.find({}, {'_id': 0, 'question': 1, 'options': 1}).limit(num_questions)

user = User()

for question_data in questions:
    correct_answer = None

    if question_data:
        print("Question:", question_data['question'])
        for index, option in enumerate(question_data['options'], start=1):
            print(f"{index}. {option['option']}")
            if option['isCorrect']:
                correct_answer = index

    user_answer = int(input("Enter Answer: "))

    if user_answer == correct_answer:
        print("Correct answer")
        print("\n")
        user.increment_correct_answers()
        print(f"You have {timer_count} time left")
    else:
        print("Incorrect answer")
        print("\n")

final_score = (user.correct_answers / num_questions) * 100
user_info.update_one(
    {"username": username},
    {"$push": {"scores": final_score}}
)
print("\n")
print(f"You answered {user.correct_answers} out of {num_questions} questions correctly.")
print("\n")
print(f"Your final score was {final_score:.2f}%")
from server import user_info, collection, User
import random

# Initialize username and password variables
username = ' '
password = ' '

print('\n')
# Prompt user to choose between new or previous user
new_user = input("New or Previous User? (New/Previous): ").strip().lower()
print('\n')

def admin_panel():
    while True:
        # Display admin panel options
        print("\nAdmin Panel")
        print("1. Create a new question")
        print("2. Modify an existing question")
        print("3. Delete a question")
        print("4. View all questions")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            # Create a new question
            question = input("Enter the question: ").strip()
            options = []
            for i in range(4):
                option_text = input(f"Enter option {i + 1}: ").strip()
                is_correct = input(f"Is option {i + 1} correct? (yes/no): ").strip().lower() == 'yes'
                options.append({"option": option_text, "isCorrect": is_correct})
            collection.insert_one({"question": question, "options": options})
            print("Question added successfully.")

        elif choice == '2':
            # Modify an existing question
            question_id = input("Enter the question ID to modify: ").strip()
            question = input("Enter the new question text: ").strip()
            options = []
            for i in range(4):
                option_text = input(f"Enter new option {i + 1}: ").strip()
                is_correct = input(f"Is option {i + 1} correct? (yes/no): ").strip().lower() == 'yes'
                options.append({"option": option_text, "isCorrect": is_correct})
            collection.update_one({"_id": question_id}, {"$set": {"question": question, "options": options}})
            print("Question updated successfully.")

        elif choice == '3':
            # Delete a question
            question_id = input("Enter the question ID to delete: ").strip()
            collection.delete_one({"_id": question_id})
            print("Question deleted successfully.")

        elif choice == '4':
            # View all questions
            all_questions = list(collection.find({}, {'question': 1, 'options': 1}))
            for question_data in all_questions:
                print("Question ID:", question_data['_id'])
                print("Question:", question_data['question'])
                for index, option in enumerate(question_data['options'], start=1):
                    print(f"{index}. {option['option']} (Correct: {option['isCorrect']})")
                print("\n")

        elif choice == '5':
            # Exit admin panel
            exit()

        else:
            print("Invalid choice. Please try again.")



# New User Registration
while new_user == 'new':
    username = input("Enter Username: ").strip()
    existing_user = user_info.find_one({"username": username})
    if existing_user:
        print("Username already exists. Please choose a different username.")
    else:
        password = input("Enter Password: ").strip()
        print("New User Created ")
        print(f"Welcome to the quiz {username}")
        user_info.insert_one({"username": username, "password": password})
        new_user = None

# Previous User Login
while new_user == 'previous':
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()
    if username == 'admin' and password == 'admin':
        print("Welcome to the Admin Panel")
        admin_panel()
    else:
        existing_user = user_info.find_one({"username": username, "password": password})
        if existing_user:
            print(f"Welcome back {username} !!!!")
            previous_scores = input("Would you like to take a new quiz or see previous scores? (New/Previous Scores)").strip().lower()
            if previous_scores == 'previous scores' or previous_scores == 'previous':
                user_data = user_info.find_one({"username": username})
                if user_data and "scores" in user_data:
                    print("Previous Scores:")
                    print(user_data["scores"])
                else:
                    print("No previous scores found.")
                    print("\n")
            new_user = None
        else:
            print("Invalid username and password. Please try again.")



# Prompt user for the number of questions they want to answer
num_questions = int(input("How many questions would you like to answer? ").strip())
print("\n")

# Fetch all questions from the database
all_questions = list(collection.find({}, {'_id': 0, 'question': 1, 'options': 1}))

# Randomly select the specified number of questions
questions = random.sample(all_questions, num_questions)

# Create a new user object to track correct answers
user = User()

# Loop through each question and prompt the user for an answer
for question_data in questions:
    correct_answer = None

    if question_data:
        print("Question:", question_data['question'])
        for index, option in enumerate(question_data['options'], start=1):
            print(f"{index}. {option['option']}")
            if option['isCorrect']:
                correct_answer = index

    user_answer = int(input("Enter Answer: ").strip())

    if user_answer == correct_answer:
        print("Correct answer")
        print("\n")
        user.increment_correct_answers()
    else:
        print("Incorrect answer")
        print("\n")

# Calculate the final score
final_score = (user.correct_answers / num_questions) * 100

# Update the user's scores in the database
user_info.update_one(
    {"username": username},
    {"$push": {"scores": final_score}}
)

print("\n")
print(f"You answered {user.correct_answers} out of {num_questions} questions correctly.")
print("\n")
print(f"Your final score was {final_score:.2f}%")
exit()

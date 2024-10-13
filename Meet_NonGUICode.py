import os
import shutil
import random
import time

class QuizCentre:
    quiz_state = False
    quiz_file = None
    num_questions = 0
    total_quiz_time_in_seconds = 0
    num_users = 0
    file_path = None
    file_choice = 0

    @staticmethod
    def main():
        print("---------------\"WELCOME TO THE QUIZ_QUIZ\"---------------")
        print("----------USE '3' FOR EXIT-----------")

        while True:
            print("\nAs what ROLE, you want to continue ?(ADMIN OR CANDIDATE)\n" +
                  "[TYPE '1' FOR \"ADMIN\" AND '2' FOR ALL \"CANDIDATES\"]")
            choice = 0
            try:
                choice = int(input())
            except ValueError:
                print("Invalid input. Please enter a valid integer choice.")

            if choice == 1:
                QuizCentre.admin_menu()
            elif choice == 2:
                if QuizCentre.quiz_state:
                    print("Quiz is started for Candidates !!")
                    QuizCentre.start_quiz()
                    exit(0)
                else:
                    print("Quiz is not created yet, Sorry !")
            elif choice == 3:
                exit(0)
            else:
                print("Invalid I/P, Try again.")

    @staticmethod
    def admin_menu():
        while True:
            print("Enter ADMIN password:")
            password = input()
            print()
            if password.upper() == "IAMADMIN":
                break
            elif password == "3":
                exit(0)
            else:
                print("Wrong password or role.")

        flag = True
        while flag:
            print("Choose an option for \"QUIZ-TYPE\":")
            print("1. Take a quiz from the inbuilt quizzes.")
            print("2. Take a quiz from your own file.(By entering 'FILE-PATH')")
            choice2 = 0

            try:
                choice2 = int(input())
            except ValueError:
                print("Invalid input. Please enter a valid integer choice.")

            if choice2 == 1:
                QuizCentre.take_inbuilt_quiz()
                if QuizCentre.quiz_file is None:
                    print("Try again.")
                else:
                    QuizCentre.file_choice = 1
                    flag = False
            elif choice2 == 2:
                QuizCentre.take_custom_quiz()
                if QuizCentre.quiz_file is None:
                    print("Try again.")
                else:
                    QuizCentre.file_choice = 2
                    flag = False
            elif choice2 == 3:
                exit(0)
            else:
                print("Invalid choice. Please try again.")

        print("Enter the total time for the quiz (in seconds): ")
        QuizCentre.total_quiz_time_in_seconds = int(input())

        print("Enter the number of users you want to give the quiz: ")
        try:
          QuizCentre.num_users = int(input())
        except ValueError:
                print("Invalid input. Please enter a valid integer choice.")
        QuizCentre.quiz_state = True

    @staticmethod
    def start_quiz():
        users = []
        user_details = {}
        total_time_taken=[]

        for i in range(1, QuizCentre.num_users + 1):
            print("User:", i)
            
            while True:
                flg = 0
                try:
                    ID = (input("Enter your ID number: "))
                    id2 = int(ID)
                    flg = 1
                except ValueError:
                    print("Invalid input. Please enter a valid integer for the ID.")
                if flg == 1 :
                    if ID in user_details.keys() :
                            print("ID already exists. Please enter a unique ID.")
                    else:
                        name = input("Enter your name: ")
                        user_details[i] = name
                        user_details[ID] = name
                        
                        break
            score = 0
            total_elapsed_time = 0

            try:
                with open(name + ".txt", "a") as file_writer:
                    file_writer.write("\nName: \n" + name)
                    file_writer.write("ID Number: {}\n\n" + ID)

                    available_questions = QuizCentre.read_available_questions(QuizCentre.quiz_file)
                    selected_questions = QuizCentre.select_random_questions(available_questions, QuizCentre.num_questions)

                    question_number = 0
                    for qa in selected_questions:
                        print("[Total time remaining {} seconds]".format(QuizCentre.total_quiz_time_in_seconds - (total_elapsed_time // 1000)))
                        question_number += 1
                        file_writer.write("Question {}: {}\n".format(question_number, qa["question"]))
                        print("Question {}: {}".format(question_number, qa["question"]))

                        start_time = QuizCentre.get_current_time_in_milliseconds()
                        user_answer = input()  # Read the entire line for the user's answer
                        end_time = QuizCentre.get_current_time_in_milliseconds()
 
                        elapsed_time = end_time - start_time
                        total_elapsed_time += elapsed_time

                        file_writer.write("Your Answer for Question {}: {}\n".format(question_number, user_answer))

                        correct_answer = str(qa["answer"]).upper()
                        if user_answer.strip().lower() == correct_answer.strip().lower():
                            file_writer.write("Correct: Yes\n")
                            score += 1
                        else:
                            file_writer.write("Correct: No (Correct Ans : {})\n".format(correct_answer))

                        if total_elapsed_time / 1000 > QuizCentre.total_quiz_time_in_seconds:
                            print("TIME's UP FOR QUIZ ")
                            break

                    file_writer.write("Total Time: {} sec\n".format(total_elapsed_time / 1000))
                    file_writer.write("Score: {}\n".format(score))
                    if score > 0:
                        users.append({"name": name, "score": score})

                    print("Quiz for {} has been done. Your score: {}".format(name, score))
                    total_time_taken.append(total_elapsed_time // 1000)
                    print("Total Time Taken: {} sec".format(total_elapsed_time//1000))

            except Exception as e:
                print("Error while running quiz:", e)

        if users:
            users.sort(key=lambda x: x["score"], reverse=True)
            win_index = 0
            winner = users[win_index]
            decision = min(total_time_taken)
            index = total_time_taken.index(decision)
            
            if len(users)>1 and users[win_index]["score"] == users[win_index - 1]["score"]:
                winner = users[index]
                print("Winner: {} with a score of {} out of {}.".format(winner["name"], winner["score"], QuizCentre.num_questions))
            else:
                winner = users[win_index]
                print("Winner: {} with a score of {} out of {}.".format(winner["name"], winner["score"], QuizCentre.num_questions))
        else:
            print("No one has scored more than 0.")

    @staticmethod
    def count_questions(filename):
        que_counter = 0
        qa = 0

        with open(filename, "r") as file:
            for line in file:
                if qa == 0 and line.startswith("Q: "):
                    if len(line) > 3:
                        que_counter += 1
                        qa = 1
                    else:
                        return -1
                elif qa == 1 and line.startswith("A: "):
                    if len(line) > 3:
                        qa = 0
                    else:
                        return -1
                else:
                    return -1

        return que_counter

    @staticmethod
    def take_inbuilt_quiz():
        quiz_files = [file for file in os.listdir(".") if file.startswith("GK_quiz")]
        if quiz_files:
            random_quiz_file = random.choice(quiz_files)
            print("Taking quiz from: ",random_quiz_file)
            QuizCentre.num_questions = QuizCentre.count_questions(random_quiz_file)
            QuizCentre.quiz_file = random_quiz_file
        else:
            print("At this moment there is no inbuilt quiz for users.")

    @staticmethod
    def take_custom_quiz():
        print("Enter the file path of the quiz:")
        QuizCentre.file_path = input()

        custom_quiz_file = os.path.basename(QuizCentre.file_path)
        if not os.path.exists(custom_quiz_file):
            print("File not found. Please check the file path and try again.")
            return
        QuizCentre.num_questions = QuizCentre.count_questions(QuizCentre.file_path)

        if QuizCentre.num_questions == -1:
            print("Found Wrong Format.")
            return
        else:
            print("Total Questions are {}.".format(QuizCentre.num_questions))

        print("Taking quiz from: {}".format(custom_quiz_file))
        QuizCentre.quiz_file = custom_quiz_file

        # Copying the file to the current directory
        shutil.copyfile(QuizCentre.file_path, custom_quiz_file)

    @staticmethod
    def read_available_questions(filename):
        questions = []
        current_question = ""
        current_answer = None

        with open(filename, "r") as file:
            for line in file:
                if line.startswith("Q: "):
                    # Store the previous question and answer
                    if len(current_question) > 0 and current_answer is not None:
                        questions.append({"question": current_question, "answer": current_answer})
                    current_question = line[3:]
                elif line.startswith("A: "):
                    current_answer = line[3:]

        # Add the last question and answer
        if len(current_question) > 0 and current_answer is not None:
            questions.append({"question": current_question, "answer": current_answer})

        return questions

    @staticmethod
    def select_random_questions(questions, num_questions):
        selected_questions = random.sample(questions, min(num_questions, len(questions)))
        return selected_questions

    @staticmethod
    def get_current_time_in_milliseconds():
        return int(round(time.time() * 1000))


# if __name__ == "__main__":
QuizCentre.main()
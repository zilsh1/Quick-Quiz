import os
import shutil
import random
import time
from tkinter import *
import customtkinter as ctk

class QuizCentre:
    quiz_state = False
    quiz_file = None
    num_questions = 0
    num_answers = 0
    total_quiz_time_in_seconds = 0
    num_users = 0
    count_Can = 0
    file_path = None
    file_choice = 0
    customQFlg = False
    
    @staticmethod
    def main():
        
        #GUI
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        root = ctk.CTk()
        root.title('Quick Quiz!')
        root.geometry('1920x1080')

            
        def stQuizForCandidates() :
            users = []
            user_details = {}
            total_time_taken=[]
            
            def startQz() :
                    
                # QuizCentre.count_Can += 1
                # if QuizCentre.count_Can <= QuizCentre.num_users :
                    candiWindow = ctk.CTkToplevel(root, fg_color="white")
                    candiWindow.title("Candidate Window")
                    candiWindow.geometry('1920x1080')

                    def attemp_Quiz() :
                        psw = "0000"

                        warn = ctk.CTkLabel(candiWindow, text=f'{psw}',
                                        text_color="Red",
                                        font=("Helvetica", 12))
                        warn.place(relx=0.48, rely=0.07)

                        if cName.get() == "" or not(cId.get().isdigit()) or cPsw.get() != psw or cId.get() in user_details.keys() :

                            warn.configure(text="*Plese enter proper details!")
                        else :
                            
                            warn.configure(text="                                                                                  ")
                            
                            user_details[QuizCentre.count_Can] = cName.get()
                            user_details[cId.get()] = cName.get()

                            global score, total_elapsed_time, question_index
                            score = 0
                            question_index = 0
                            total_elapsed_time = 0
                            
                            file_writer = open(cName.get() + ".txt", "w+")
                            file_writer.write("\nName: " + cName.get() + " | ")
                            file_writer.write("ID Number: " + cId.get() + "\n\n")

                            available_questions = read_available_questions(QuizCentre.quiz_file)
                            selected_questions = select_random_questions(available_questions, QuizCentre.num_questions)
                            
                            Que_frame = ctk.CTkScrollableFrame(candiWindow,
                                                                height=600,
                                                                width=1515,
                                                                )
                            Que_frame.place(relx=0.0, rely=0.1)

                            def Display_Que() :
                                global question_index
                                question = selected_questions[question_index]

                                question_index += 1

                                def Sub_ans() :
                                    global question_index
                                    global score
                                    global total_elapsed_time
                                    ans = user_answer.get()

                                    file_writer.write("Your Answer for Question {}: {}\n".format(question_index, ans))
                                    correct_answer = str(question["answer"]).upper()

                                    if ans.strip().lower() == correct_answer.strip().lower():

                                        file_writer.write("Correct: Yes\n")
                                        score += 1
                                    else:
                                        file_writer.write("Correct: No ----> Correct Ans : " + correct_answer + "\n")
                                    end_time = get_current_time_in_milliseconds()
                                    elapsed_time = end_time - start_time
                                    total_elapsed_time += elapsed_time

                                    if question_index < QuizCentre.num_questions :
                                            Display_Que()
                                       
                                file_writer.write("Question {}: {}\n".format(question_index, question["question"]))
                                #Question
                                que = ctk.CTkLabel(Que_frame,
                                                    text=f'Q_{question_index} : {question["question"]}')
                                que.pack(pady=10, anchor = 'w')
                                
                                user_answer = ctk.CTkEntry(Que_frame,
                                                                    height=16,
                                                                    placeholder_text="Answer")
                                user_answer.pack(pady=10, anchor = 'w',)
                                global submit_ans
                                submit_ans = ctk.CTkButton(Que_frame, text="Submit_ans",
                                                                    height=16,
                                                                    command= Sub_ans)
                                submit_ans.pack(pady=10, anchor = 'w',)

                                    
                            #Noting Start time
                            global start_time
                            start_time = get_current_time_in_milliseconds()
                                       
                            Display_Que()
                                         
                            global timer_Flag
                            timer_Flag = True

                            def finish_Attemp() :
                                global timer_Flag
                                timer_Flag = False
                                global submit_ans
                                submit_ans.configure(fg_color="gray")
                                submit_ans.configure(state="disable")
                                end_time = get_current_time_in_milliseconds()
                                total_elapsed_time = end_time - start_time

                                def close_Window() :
                                    file_writer.close()

                                    candiWindow.destroy()
                                    candiWindow.update()
                                    
                                    if QuizCentre.count_Can < QuizCentre.num_users - 1 : 
                                        QuizCentre.count_Can += 1
                                        startQz()
                                    else :
                                        declare_Winner(users, total_time_taken)
                            

                                file_writer.write("\nTotal Time: {} sec\n".format(total_elapsed_time / 1000))
                                total_time_taken.append(total_elapsed_time // 1000)
                                file_writer.write("Score: {}\n".format(score))
                                
                                users.append({"name": cName.get(), "score": score})

                                finish_Lbl = ctk.CTkLabel(candiWindow,
                                                                text=f'Quiz for {cName.get()} has been done. Your score: {score}')
                                finish_Lbl.place(relx=0.5, rely=0.85, anchor=CENTER)

                                Close_Btn = ctk.CTkButton(candiWindow,
                                                                text=f'Close Window',
                                                                command=close_Window)
                                Close_Btn.place(relx=0.5, rely=0.9, anchor=CENTER)

                            qzInfo = ctk.CTkLabel(candiWindow,
                                            text=f'Total Que: {QuizCentre.num_questions} | Total Time: {QuizCentre.total_quiz_time_in_seconds//60} Min.',
                                            font=("Helvetica", 16)) 
                            qzInfo.place(relx=0.01, rely=0.85)

                            Finish_Attemp = ctk.CTkButton(candiWindow, text="Finish Attemp",
                                                                        command=finish_Attemp)
                            Finish_Attemp.place(relx=0.9, rely=0.85)

                            global timesUp
                            timesUp = ctk.CTkLabel(candiWindow, 
                                                    text=f'',
                                                    text_color='red',
                                                    font=("Helvetica", 16)) 
                            timesUp.place(relx=0.01, rely=0.93)

                            def countdown_timer(minutes):
                                global timer_Flag
                                total_seconds = minutes * 60
                                
                                #while total_seconds > 0:
                                mins = total_seconds // 60
                                secs = total_seconds % 60
                                
                                #f"{mins:02d}:{secs:02d}", end='\r')
                                timeLabel = ctk.CTkLabel(candiWindow, 
                                                text=f'*Time remaining: [{mins:02d}:{secs:02d}]',
                                                font=("Helvetica", 16)) 
                                timeLabel.place(relx=0.01, rely=0.9)

                                total_seconds -= 1

                                def recursive_timer(total_seconds):
                                    if timer_Flag :
                                        if total_seconds > 0 :
                                            #time.sleep(1)
                                            mins = total_seconds // 60
                                            secs = total_seconds % 60

                                            timeLabel.configure(text=f'*Time remaining: [{mins:02d}:{secs:02d}]') 
                                            total_seconds -= 1
                                            candiWindow.after(1000, recursive_timer, total_seconds)
                                        else :
                                            timeLabel.configure(text=f'*Time remaining: [00:00]')
                                            timesUp.configure(text=f'Time\'s up for Quiz!')
                                            Finish_Attemp.configure(fg_color="gray")
                                            Finish_Attemp.configure(state="disable")
                                            finish_Attemp()  
                                recursive_timer(total_seconds)
                            countdown_timer(QuizCentre.total_quiz_time_in_seconds // 60)

                    lbl1 = ctk.CTkLabel(candiWindow, text=f'Welcome to Quiz Candidate-{QuizCentre.count_Can+1}.',
                                        font=("Helvetica", 16))
                    lbl1.place(relx=0.02, rely=0.01, )

                    lbl2 = ctk.CTkLabel(candiWindow, text="Fill up your details here :",
                                                    font=("Helvetica", 16))
                    lbl2.place(relx=0.02, rely=0.04, )

                    cName = ctk.CTkEntry(candiWindow,
                                        placeholder_text="Name",
                                        height=16
                                        )
                    cName.place(relx=0.15, rely=0.045)

                    cId = ctk.CTkEntry(candiWindow,
                                        placeholder_text="ID",
                                        height=16
                                        )
                    cId.place(relx=0.25, rely=0.045)

                    cPsw = ctk.CTkEntry(candiWindow,
                                        placeholder_text="Password",
                                        height=16
                                        )
                    cPsw.place(relx=0.35, rely=0.045)

                    attempQz = ctk.CTkButton(candiWindow, text="Attemp Quiz",
                                                            height=16,
                                                            command=attemp_Quiz,
                                                            )
                    attempQz.place(relx=0.48, rely=0.045 )

            startQz()


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
        def select_random_questions(questions, num_questions):
            selected_questions = random.sample(questions, min(num_questions, len(questions)))
            return selected_questions
        
        def get_current_time_in_milliseconds():
            return int(round(time.time() * 1000))
        
    #------------------------------------------------------------------------------

        def declare_Winner(user, time_taken) :
            users = list(user)
            total_time_taken = list(time_taken)
            if users:
                users.sort(key=lambda x: x["score"], reverse=True)
                win_index = 0
                winner = users[win_index]
                decision = min(total_time_taken)
                index = total_time_taken.index(decision)
                
                if len(users)>1 and users[win_index]["score"] == users[win_index - 1]["score"]:
                    winner = users[index]
                    global stForCandidates
                    global stForCandidates2

                    stForCandidates.configure(text="Quiz's Completed")
                    stForCandidates.configure(state="disable")
                    stForCandidates2.configure(text="Quiz's Completed")
                    stForCandidates2.configure(state="disable")

                    winner_Lbl = ctk.CTkLabel(root,
                                                text=f'Winner: {winner["name"]} with a score of {winner["score"]} out of {QuizCentre.num_questions}.',
                                                 font=("Helvetica", 18))
                    winner_Lbl.place(relx=0.3,rely=0.9, anchor=CENTER)
                else:
                    winner = users[win_index]
                    winner_Lbl = ctk.CTkLabel(root,
                                                text=f'Winner: {winner["name"]} with a score of {winner["score"]} out of {QuizCentre.num_questions}.',
                                                 font=("Helvetica", 20))
                    winner_Lbl.place(relx=0.5,rely=0.9, anchor=CENTER)
            else:
                No_Winner_Lbl = ctk.CTkLabel(root,
                                                text=f'No one has scored more than 0.',
                                                 font=("Helvetica", 20))
                No_Winner_Lbl.place(relx=0.5,rely=0.9, anchor=CENTER)

    #------------------------------------------------------------------------------
        
        #Process for Admin to create quiz 
        def admin_menu() :

            def quetion_paper() :
                    
                    def create_Quiz() :
                        warn2 = ctk.CTkLabel(root, text="",
                                    text_color="Red",
                                    font=("Helvetica", 12))
                        warn2.place(relx=0.3,rely=0.71)
                        if radioVar.get() == "0" or not(candidates.get()).isdigit() or not(totalTime.get()).isdigit() or candidates.get() == "0" or totalTime.get() == "0": 

                            warn2.configure(text="*Please select/enter proper details !")

                        else :
                            
                            warn2.configure(text="                                                                                        ")
                            
                            QuizCentre.total_quiz_time_in_seconds = 60*(int(totalTime.get()))
                            QuizCentre.num_users = int(candidates.get())

                            if radioVar.get() == "1"  :

                                take_inbuilt_quiz()
                                        ###
                                inbuilt.configure(state="disable")
                                userDef.configure(state="disable")
                                candidates.configure(state="disable")
                                QuizCentre.quiz_state = True

                            else :
                                
                                take_custom_quiz()

                                inbuilt.configure(state="disable")
                                userDef.configure(state="disable")
                                candidates.configure(state="disable")
                                QuizCentre.quiz_state = True

                    def take_inbuilt_quiz():
                        quiz_files = [file for file in os.listdir(".") if file.startswith("GK_quiz")]
                        if quiz_files:
                            random_quiz_file = random.choice(quiz_files)

                            QuizCentre.num_questions = count_questions(random_quiz_file)
                            QuizCentre.quiz_file = random_quiz_file

                            ranQz = ctk.CTkLabel(root, text=f'Taking quiz from: {random_quiz_file} (TOTAL QUESTIONS={QuizCentre.num_questions})',
                                                        font=("Helvetica", 16))
                            ranQz.place(relx=0.3,rely=0.74)           

                            global stForCandidates
                            stForCandidates = ctk.CTkButton(root, text="Start Quiz for the candidates",
                                                fg_color="DarkOrange",
                                                hover_color="Olive",
                                                command=stQuizForCandidates
                                                )
                            stForCandidates.place(relx=0.3,rely=0.8)
                        else:
                            noFile = ctk.CTkLabel(root, text=f'*At this moment, no inbuilt quiz is available !',
                                                        text_color="red",
                                                        font=("Helvetica", 16))
                            noFile.place(relx=0.3,rely=0.74)

                    
                    def take_custom_quiz():   
                                                      #C:/Users/KISHAN/Desktop/GK_Q_Desk2.txt-----------------------------------------------
                        
                        def fatchFile() :
                            QuizCentre.file_path = custFilePath.get()

                            custom_quiz_file = os.path.basename(QuizCentre.file_path)
                            

                            notFound = ctk.CTkLabel(root, text="",
                                                            text_color="red",
                                                            font=("Helvica", 12))
                            notFound.place(relx=0.3, rely=0.87)

                            if not os.path.exists(custom_quiz_file):
                                notFound.configure(text="File not found. Please correct the file path !")
                            else :
                                notFound.configure("                                                                                                                                      ")
                                QuizCentre.num_questions = count_questions(QuizCentre.file_path)
                                
                                wrongFormat = ctk.CTkLabel(root,
                                        text=" ",
                                        text_color="red",
                                        font=("Helvica", 12))
                                wrongFormat.place(relx=0.3, rely=0.87,)

                                if QuizCentre.num_questions == -1:
                                    
                                    wrongFormat.configure(text="Found Wrong Format!")

                                else:
                                    wrongFormat.configure(text="                                                                      ")

                                    custFile = ctk.CTkLabel(root,
                                        text=f'[ Taking quiz from: {custom_quiz_file} (TOTAL QUESTIONS={QuizCentre.num_questions}) ]',
                                        font=("Helvica", 16))
                                    custFile.place(relx=0.4, rely=0.83,)
                                
                                    QuizCentre.quiz_file = custom_quiz_file

                                    # Copying the file to the current directory
                                    shutil.copyfile(QuizCentre.file_path, custom_quiz_file)

                                    custFilePath.configure(state="disable")
                                    enter.configure(state="disable")
                                    QuizCentre.file_choice = 2
                                    global stForCandidates2
                                    stForCandidates2 = ctk.CTkButton(root, text="Start Quiz for the candidates",
                                                    fg_color="DarkGoldenrod",
                                                    hover_color="Olive",
                                                    command=stQuizForCandidates
                                                    )
                                    stForCandidates2.place(relx=0.3,rely=0.9)

                        adlbl5 = ctk.CTkLabel(root, text="Enter your custom Quiz file Path below:",
                                                          font=("Helvetica", 16))
                        adlbl5.place(relx=0.3,rely=0.74) 

                        adlbl6 = ctk.CTkLabel(root, text=" (i,e: C:/Users/KISHAN/Desktop/GK_Q_Desk2.txt) ",   
                                                      font=("Helvetica", 16))
                        adlbl6.place(relx=0.4,rely=0.74) 

                        custFilePath = ctk.CTkEntry(root,
                                placeholder_text="File Path",
                                height=16,
                                width=400,
                                font=("Helvica", 16))
                        custFilePath.place(relx=0.3, rely=0.78,)
                        
                        enterPath = ctk.CTkButton(root, text="Enter",
                                                        height=16,
                                                        command=fatchFile)
                        enterPath.place(relx=0.3,rely=0.84)                   

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

                        #quetion paper portion
                    adlbl2 = ctk.CTkLabel(root, text="Let's prepare the QUIZ :",
                                        font=("Helvetica", 16))
                    adlbl2.place(relx=0.3, rely=0.38)

                    adlbl3 = ctk.CTkLabel(root, text="Select the mode of \"Quiz paper\" :",
                                        font=("Helvetica", 16))
                    adlbl3.place(relx=0.3, rely=0.42)

                    radioVar = ctk.StringVar(value="0")
                    inbuilt = ctk.CTkRadioButton(root, text="Inbuilt",
                                                 height=16,
                                                value="1",
                                                variable=radioVar)
                    inbuilt.place(relx=0.3, rely=0.47)

                    userDef = ctk.CTkRadioButton(root, text="User Defined",
                                                 height=16,
                                                value="2",
                                                variable=radioVar)
                    userDef.place(relx=0.4, rely=0.47)
                    
                    #No. of candidates
                    adlbl4 = ctk.CTkLabel(root, text="Enter the total number of Candidates :",
                                        font=("Helvetica", 16))
                    adlbl4.place(relx=0.3, rely=0.51)
                    
                    candidates = ctk.CTkEntry(root,
                                placeholder_text="Total Candidates",
                                height=16,
                                width=200,
                                font=("Helvica", 16))
                    candidates.place(relx=0.3, rely=0.55,)

                    tm = ctk.CTkLabel(root, text="Enter the total time of quiz in Minute :",
                                        font=("Helvetica", 16))
                    tm.place(relx=0.3, rely=0.59)
                    
                    totalTime = ctk.CTkEntry(root,
                                placeholder_text="Time in Minute",
                                height=16,
                                width=200,
                                font=("Helvica", 16))
                    totalTime.place(relx=0.3, rely=0.63,)

                    createQz = ctk.CTkButton(root, text="Create Quiz",
                                                    height=16,
                                                    command=create_Quiz,
                                                    )
                    createQz.place(relx=0.3, rely=0.68, )

            #wrong psw
            warn = ctk.CTkLabel(root, text="",
                                    text_color="Red",
                                    font=("Helvetica", 10))
            warn.place(relx=0.3,rely=0.28)

            #Admin password security
            def submit() :

                if((password.get()).upper() != "0000") :
                    warn.configure(text="*Wrong Password !!")

                elif((password.get()).upper() == "0000") :

                    warn.configure(text="")
                    password.configure(state="disable")
                    submit1.configure(state="disable")
                    clr.configure(state="disable")
                    
                    quetion_paper()
            
            def clear() :
                #password.configure(state="normal")
                password.delete(0, 100)   #deleting the data of entry box
                warn.configure(text="")

            #while True:
            adlbl1 = ctk.CTkLabel(root, text="Enter Admin password below :",
                                   font=("Helvetica", 16))
            adlbl1.place(relx=0.3, rely=0.22,)

            password = ctk.CTkEntry(root,
                                placeholder_text="Admin Password",
                                height=16,
                                width=200,
                                font=("Helvica", 16))
            password.place(relx=0.3, rely=0.26,)

            submit1 = ctk.CTkButton(root, text="Submit",
                                         height=16,
                                         command=submit)
            submit1.place(relx=0.3, rely=0.32, )

            clr = ctk.CTkButton(root, text="Clear",
                                      height=16,
                                     command=clear)
            clr.place(relx=0.4, rely=0.32, )


                                            #STRAT POINT#
            
        lbl1 = ctk.CTkLabel(root, text="Welcome to \"QUICK_QUIZ\" program",
                                 font=("Helvetica", 18))
        lbl1.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        enter = ctk.CTkButton(root, text = "Enter in the Program",
                                    height=20,
                                    command=admin_menu)
        enter.place(relx=0.5, rely=0.15, anchor=CENTER)

        root.mainloop()   
         
# if __name__ == "__main__":
QuizCentre.main()
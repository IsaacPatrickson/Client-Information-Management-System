from __future__ import print_function
import sys
import random
import mysql.connector
from mysql.connector import errorcode
from User import *
from Hashing_Algo import *
from Quiz import *
from Quiz_Question import *
from Quiz_Answer import *
from Take import *
from Take_Answer import *
from Select_Function import *

cnx = mysql.connector.connect(user='root', password='Isaac250mysql!', database='quiz')
cursor = cnx.cursor()


def login_menu():
    print()
    print("    ____        _          ______                    ")
    print("   / __ \__  __(_)___     / ____/___ _____ ___  ___  ")
    print("  / / / / / / / /_  /    / / __/ __ `/ __ `__ \/ _ \ ")
    print(" / /_/ / /_/ / / / /_   / /_/ / /_/ / / / / / /  __/ ")
    print(" \___\_\__,_/_/ /___/   \____/\__,_/_/ /_/ /_/\___/  ")
    print()
    print()
    print(" 1. Login")
    print(" 2. Sign Up")
    print(" 0. Quit")
    print()
    
    valid = False
    
    while valid == False:

        choice = input("Select 1, 2 or 0: ")
        
        if choice == "1":
            valid = True

            while True:

                try:
                    login = User()
                    print()
                    login.set_email(input("Email addresss: "))
                    login.selected_salt(login.get_email())
                    login.selected_password(login.get_email())
                    check = check_password(login.get_selected_salt(),
                                           login.get_selected_password(),
                                           input("Password: "))
                    break

                except:
                    print("An account with this email does not exist")
                    login_menu()
                    
            if check == True:
                name = login.return_name(login.get_email())
                print()
                print("Login Successful")
                print("Welcome,", name)
                login.set_selected_id(login.get_email())
                user_menu(login.get_email(), login.get_selected_id())
                
            else:
                print()
                print("Incorrect password")
                login_menu()
                
        elif choice == "2":
            valid = True

            while True:
            
                try:
                    print()
                    new = User()
                    new.set_first_name(input("First Name: "))
                    new.set_last_name(input("Last Name: "))
                    new.set_email(input("Email address: "))
                    new.set_salt()
                    new.set_password_hash(input("Password: "), new.get_salt())
                    new.set_profile()
                    new.add_user()
                    new.set_selected_id(new.get_email())
                    break
                    
                except:
                    print()
                    print("An account with that email already exists")
                    login_menu()

            user_menu(new.get_email(), new.get_selected_id())
                
            
        elif choice == "0":
            valid = True
            exit()
            
        else:
            pass
            
def user_menu(userEmail, id):
    print()
    print("     __  ___                 ")
    print("    /  |/  /__  ____  __  __ ")
    print("   / /|_/ / _ \/ __ \/ / / / ")
    print("  / /  / /  __/ / / / /_/ /  ")
    print(" /_/  /_/\___/_/ /_/\__,_/   ")
    print()
    print()
    print(" 1. Take a Quiz")
    print(" 2. Make a Quiz")
    print(" 3. View your created Quizzes")
    print(" 4. View Profile")
    print(" 5. View Leaderboads")
    print(" 0. Logout")
    print()
    
    valid = False
    
    while valid == False:

        choice = input("Select 1, 2, 3, 4 or 0: ")
        
        if choice == "1":
            valid = True
            print()
            quizTable = select_all_quizzes()
                
            valid = False
            
            while valid == False:
                
                while True:
                    
                    try:
                        print()
                        quizSelection = int(input("Select a quiz by entering it's ID: "))
                        break
                    
                    except:
                        print("That's not an ID")
                        
                if quizSelection > 0 and quizSelection < (len(quizTable) + 1):
                    valid = True
                    quizSelection = str(quizSelection)
                    scoreCount = 0
                    takeTitle = select_query_executor("SELECT title FROM quiz WHERE id = " + quizSelection)
                    valid = False
                    
                    while valid == False:
                        print()
                        print("Are you sure you want to take this quiz [Y/N]: ", takeTitle)
                        choice = input()
                        choice = choice.upper()
                        
                        if choice == "Y":
                            valid = True
                            takeQuiz = Take()
                            takeQuiz.set_quiz_id(quizSelection)
                            takeQuiz.set_user_id(id)
                            takeQuiz.set_quiz_id(quizSelection)
                            takeQuiz.set_score(0)
                            content = select_query_executor("SELECT content FROM quiz WHERE id = " + quizSelection)
                            takeQuiz.set_content(content)
                            takeQuiz.add_take()
                            takeQuiz.set_take_id()
                            scoreCount = 0
                            
                            print()
                            print(takeTitle)
                            print("Description:",content)

                            questions = []
                            questions = select_all_strings_query_executor("SELECT content FROM quiz_question WHERE quizId = " + quizSelection)
                            questionTypes = select_all_strings_query_executor("SELECT type FROM quiz_question WHERE quizId = " + quizSelection)
                            questionIds = select_all_integers_query_executor("SELECT id FROM quiz_question WHERE quizId = " + quizSelection)
                            
                            for i in range(len(questions)-1, 0, -1):
                                j = random.randint(0, i)
                                questions[i], questions[j] = questions[j], questions[i]
                                questionTypes[i], questionTypes[j] = questionTypes[j], questionTypes[i]
                                questionIds[i], questionIds[j] = questionIds[j], questionIds[i]

                            for i in range(len(questions)):
                                
                                if questionTypes[i] == "1":
                                    multipleOptions = []
                                    correctMCValues = []
                                    multipleOptions = select_all_strings_query_executor("SELECT content FROM quiz_answer WHERE questionId = " + questionIds[i])
                                    correctMCValues = select_all_integers_query_executor("SELECT correct FROM quiz_answer WHERE questionId = " + questionIds[i])
                                    
                                    for j in range(len(multipleOptions)-1, 0, -1):
                                        k = random.randint(0, j)
                                        multipleOptions[j], multipleOptions[k] = multipleOptions[k], multipleOptions[j]
                                        correctMCValues[j], correctMCValues[k] = correctMCValues[k], correctMCValues[j]
                                    
                                print()
                                print()    
                                print("Question", i+1)
                                print(questions[i])
                                print()     
                                
                                if questionTypes[i] == "1":
                                    
                                    for j in range(len(multipleOptions)):
                                        print(str(j+1) + ".", multipleOptions[j])
                                        
                                    while True:
                                        
                                        try:          
                                            print()
                                            takeOption = int(input())
                                            
                                            if takeOption > 0 and takeOption <= len(multipleOptions):
                                                takeAnswer = Take_Answer()
                                                takeAnswer.set_take_id(takeQuiz.get_take_id())
                                                takeAnswer.set_question_id(questionIds[i])
                                                quizId = takeQuiz.get_quiz_id()
                                                answerId = select_query_executor("SELECT id FROM quiz_answer WHERE quizId = " + quizId
                                                                                 + " AND questionId = " + questionIds[i]
                                                                                 + " AND correct = 1")
                                                takeAnswer.set_answer_id(answerId)
                                                takeAnswer.set_answer_content(multipleOptions[takeOption - 1])
                                                takeAnswer.add_take_answer()
                                                break
                                            
                                            else:
                                                print("Input must be an integer preceeding one of the options above")
                                                
                                        except:
                                            print("Input must be an integer preceeding one of the options above")

                                    if correctMCValues[takeOption - 1] == "1":
                                        scoreCount += 1
                                        print()
                                        print("Correct")
                                        
                                    else:
                                        print()
                                        print("Incorrect")
       
                                if questionTypes[i] == "2":
                                    openEndedOption = []
                                    openEndedOption = select_query_executor("SELECT content FROM quiz_answer WHERE questionId = " + questionIds[i])
                                    print()
                                    takeOption = input()
                                    takeAnswer = Take_Answer()
                                    takeAnswer.set_take_id(takeQuiz.get_take_id())
                                    takeAnswer.set_question_id(questionIds[i])
                                    quizId = takeQuiz.get_quiz_id()
                                    answerId = select_query_executor("SELECT id FROM quiz_answer WHERE quizId = " + quizId
                                                                     + " AND questionId = " + questionIds[i]
                                                                     + " AND correct = 1")
                                    takeAnswer.set_answer_id(answerId)
                                    takeAnswer.set_answer_content(takeOption)
                                    takeAnswer.add_take_answer()
                                    
                                    if takeOption.upper() == openEndedOption.upper():
                                        scoreCount += 1
                                        print()
                                        print("Correct")
                                        
                                    else:
                                        print()
                                        print("Incorrect")        
                            print()
                            print("Take Finished!")
                            takeId = str(takeQuiz.get_take_id())
                            update_query_executor("UPDATE take SET score = " + str(scoreCount) + " WHERE id = " + takeId)
                            profileScore = select_query_executor("SELECT profile FROM user WHERE id = " + str(id))
                            update_query_executor("UPDATE user SET profile = " + str(int(profileScore) + scoreCount) + " WHERE id = " + str(id))
                            maxPossibleScore = select_query_executor("SELECT maxScore FROM quiz WHERE id = " + quizSelection)
                            profileScore = select_query_executor("SELECT profile FROM user WHERE id = " + str(id))
                            
                            print("You scored", scoreCount, "out of", maxPossibleScore)
                            print()
                            print("Your total Quiz Points is now:", profileScore)
                            user_menu(userEmail, id)
                                
                        elif choice == "N":
                            valid = True
                            user_menu(userEmail, id)
                            
                        else:
                            print("Errror, please enter Y or N")
                            
                else:
                    print("Please select an existing ID")


        elif choice == "2":
            valid = True
            quiz = Quiz()
            quiz.set_host_id(id)
            print()
            quiz.set_title(input("Quiz title: "))
            quiz.set_quiz_type()
            quiz.set_max_score()
            print()
            quiz.set_content(input("Quiz description: "))
            quiz.add_quiz()
            quiz.set_quiz_id()
            
            for i in range(quiz.get_max_score()):
                print()
                print("Question", i+1)
                question = Question()
                question.set_quiz_id(quiz.get_quiz_id())
                question.set_question_type(quiz.get_quiz_type())
                question.set_level()
                question.set_score()
                print()
                question.set_question_content(input("Question content: "))
                question.add_question()
                question.set_question_id()
                
                if question.get_question_type() == "1":
                    multipleChoice = Answer()
                    multipleChoice.set_quiz_id(quiz.get_quiz_id())
                    multipleChoice.set_question_id(question.get_question_id())
                    multipleChoice.multiple_choice_handling()
                    
                elif question.get_question_type() == "2":
                    openEnded = Answer()
                    openEnded.set_correct()
                    openEnded.set_quiz_id(quiz.get_quiz_id())
                    openEnded.set_question_id(question.get_question_id())
                    openEnded.set_answer_content(input("Content: "))
                    openEnded.add_answer()
                    
                elif question.get_question_type() == "3":
                    valid = False
                    multipleOrOpen = input("Multiple choice question or Open ended [M/O]: ")
                    
                    while valid == False:
                        
                        if multipleOrOpen == "M":
                            valid = True
                            update_query_executor("UPDATE quiz_question SET type = 1 WHERE type = 3")
                            multipleChoice = Answer()
                            multipleChoice.set_quiz_id(quiz.get_quiz_id())
                            multipleChoice.set_question_id(question.get_question_id())
                            multipleChoice.multiple_choice_handling()
                            
                        elif multipleOrOpen == "O":
                            valid = True
                            update_query_executor("UPDATE quiz_question SET type = 2 WHERE type = 3")
                            openEnded = Answer()
                            openEnded.set_correct()
                            openEnded.set_quiz_id(quiz.get_quiz_id())
                            openEnded.set_question_id(question.get_question_id())
                            openEnded.set_answer_content(input("Content: "))
                            openEnded.add_answer()
                            
                        else:
                            multipleOrOpen = input("Multiple choice question or Open ended [M/O]: ")
            print()
            print("Quiz Complete")
            user_menu(userEmail, id)

        elif choice == "3":
            valid = True
            view_created_quizzes_menu(userEmail, id)


        elif choice == "4":
            valid = True
            userTotalScore = select_query_executor("SELECT profile FROM user WHERE id = " + id)
            print()
            print("Total Quiz Points Earned:", userTotalScore)
            user_menu(userEmail, id)

        elif choice == "5":
            valid = True
            leaderboard_menu(userEmail, id)
            
            
        elif choice == "0":
            valid = True
            login_menu()
            
        else:
            pass

def view_created_quizzes_menu(userEmail, id):
    print()
    print("Select a quiz you want to modify")
    print()
    valid = True
    print()
    quizTable = select_users_quizzes(id)

    modifySelection = None

    while modifySelection is None or modifySelection < 1 or modifySelection > (len(quizTable) + 1):

        try:
            modifySelection = int(input("Select a quiz by entering it's ID: "))

        except:
            pass
    



    

def leaderboard_menu(userEmail, id):
    print()
    print("     __                   __          __                         __     ")
    print("    / /   ___  ____ _____/ /__  _____/ /_  ____  ____ __________/ /____ ")
    print("   / /   / _ \/ __ `/ __  / _ \/ ___/ __ \/ __ \/ __ `/ ___/ __  / ___/ ")
    print("  / /___/  __/ /_/ / /_/ /  __/ /  / /_/ / /_/ / /_/ / /  / /_/ (__  )  ")
    print(" /_____/\___/\__,_/\__,_/\___/_/  /_.___/\____/\__,_/_/   \__,_/____/   ")
    print()
    print()
    print("1. View overall Leaderboard")
    print("2. View leaderboards per quiz")
    print("0. Go back")
    print()

    valid = False

    while valid == False:

        choice = input("Select 1, 2 or 0: ")

        if choice == "1":
            valid = True
            userIdList = select_all_integers_query_executor("SELECT id FROM user")
            userNameList = []
            scoreList = []
            userIdNameScoreList = []
            
            for userId in userIdList:
                userName = name_selector(userId)
                userNameList.append(userName)
                profileScore = select_query_executor("SELECT profile FROM user WHERE id = " + userId)
                scoreList.append(profileScore)
            
            for i in range(len(userIdList)):
                userIdNameScore = ("USER ID: " + userIdList[i] + "  " + "USERNAME: " + userNameList[i] + "  " + "SCORE: " + scoreList[i])
                userIdNameScoreList.append(userIdNameScore)

            scoreList, userIdNameScoreList = zip(*sorted(zip(scoreList, userIdNameScoreList)))
            scoreList = scoreList[::-1]
            userIdNameScoreList = userIdNameScoreList[::-1]

            print()
            print()
            print("TOP 50 PLAYERS")
            print()
            
            for i in range(len(scoreList[:50])):
                print(str(i+1) + ". " + str(userIdNameScoreList[i]))

            valid2 = False
            
            while valid2 == False:
                print()
                print("Enter the number '1' when you are ready to return to the Leaderboard menu")
                goBack = input()
                
                if goBack == "1":
                    valid2 = True
                    leaderboard_menu(userEmail, id)
                    
                else:
                    pass
            
        elif choice == "2":
            valid = True
            print()
            quizTable = select_all_quizzes()

            quizSelection = None

            while quizSelection is None or quizSelection < 1 or quizSelection > (len(quizTable) + 1):

                try:
                    quizSelection = int(input("Select a quiz by entering it's ID: "))

                except:
                    pass

            quizSelection = str(quizSelection)
            userIdsOfQuizTakers = select_all_integers_query_executor("SELECT userId FROM take WHERE quizId = " + quizSelection)
            scoreForEachTake = select_all_integers_query_executor("SELECT score FROM take WHERE quizId = " + quizSelection)
            userNameList = []
            userIdNameScoreList = []
            
            for userId in userIdsOfQuizTakers:
                userName = name_selector(userId)
                userNameList.append(userName)
                
            scoreForEachTake, userIdsOfQuizTakers, userNameList = zip(*sorted(zip(scoreForEachTake, userIdsOfQuizTakers, userNameList)))
            userIdsOfQuizTakers = userIdsOfQuizTakers[::-1]
            scoreForEachTake = scoreForEachTake[::-1]
            userNameList = userNameList[::-1]
            
            for i in range(len(userIdsOfQuizTakers)):
                userIdNameScore = ("USER ID: " + userIdsOfQuizTakers[i] + "  " + "USERNAME: " + userNameList[i] + "  " + "SCORE: " + scoreForEachTake[i])
                userIdNameScoreList.append(userIdNameScore)

            leaderBoardQuizTitle = select_query_executor("SELECT title FROM quiz WHERE id = " + quizSelection)
            
            print()
            print()
            print("TOP 50 PLAYERS WHO COMPLETED:", leaderBoardQuizTitle)
            print()
            
            for i in range(len(userIdsOfQuizTakers[:50])):
                print(str(i+1) + ". " + str(userIdNameScoreList[i]))

            valid2 = False
            
            while valid2 == False:
                print()
                print("Enter the number '1' when you are ready to return to the Leaderboard menu")
                goBack = input()
                
                if goBack == "1":
                    valid2 = True
                    leaderboard_menu(userEmail, id)
                    
                else:
                    pass
            

        elif choice == "0":
            user_menu(userEmail, id)

        else:
            pass
            
                
login_menu()



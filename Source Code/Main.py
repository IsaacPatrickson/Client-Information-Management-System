from __future__ import print_function
# Changes the behavior of the 'print' funnction for older versions of python

import mysql.connector
# Importing the MySQL python connector (must have MySQL downnloaded)
import random
import sys
import time
# Importing python's premade libraries

from Hashing_Algorithm import *
from mysql.connector import errorcode
from Quiz import *
from Quiz_Answer import *
from Quiz_Question import *
from SQL_Query_Executor import *
from Take import *
from Take_Answer import *
from User import *
# Importing each part of my program so it can be accessed in the 'main'

# All subroutines, functions and imported files are in Snake case (login_menu),
# whereas variable names are in Camel case (cnxPassword)
# This is to help differentiate between variables and processes

# This while loop will ask the user to enter their details of their MySQL user so they can connect to the database 'quiz'
while True:
    print()
    cnxUser = input("Enter your MySQL username: ")
    cnxPassword = input("Enter your MySQL password: ")
    try:
        cnx = mysql.connector.connect(user=cnxUser, password=cnxPassword, database='quiz')
        cursor = cnx.cursor()
        print()
        print("MySQL account has been accepted")
        quiz_connection(cnxUser, cnxPassword)
        quiz_answer_connection(cnxUser, cnxPassword)
        quiz_question_connection(cnxUser, cnxPassword)
        sql_executor_connection(cnxUser, cnxPassword)
        take_connection(cnxUser, cnxPassword)
        take_answer_connection(cnxUser, cnxPassword)
        user_connection(cnxUser, cnxPassword)
        break
    # If the user's details are incorrect the error will be handled with exception handling
    except mysql.connector.Error as err:
        print()
        print("Something went wrong: {}".format(err))
        

# This is a subroutine which loads the Login Menu for the system
def login_menu():
    # I have used time.sleep to create an animation for the title's appearancee.
    # This style choice mimmicks that of an old computer and gives my program more character
    print()
    time.sleep(0.4)
    print()
    print("    ____  __  ___________      _________    __  _________")
    time.sleep(0.4)
    print("   / __ \/ / / /  _/__  /     / ____/   |  /  |/  / ____/")
    time.sleep(0.4)
    print("  / / / / / / // /   / /     / / __/ /| | / /|_/ / __/   ")
    time.sleep(0.4)
    print(" / /_/ / /_/ // /   / /__   / /_/ / ___ |/ /  / / /___   ")
    time.sleep(0.4)
    print(" \___\_\____/___/  /____/   \____/_/  |_/_/  /_/_____/   ")
    time.sleep(0.4)
    print()
    print()
    print(" 1. Login")
    print(" 2. Sign Up")
    print(" 0. Quit")
    print()

    # This while loop will validate the user's choice of action at the Login Menu
    loginMenuValid = False
    while loginMenuValid is False:
        choice = input("Select 1, 2 or 0: ")
        
        if choice == "1":
            loginMenuValid = True

            # If the user has chosen to login, this while loop will check if the entered detials match an existing account
            while True:
                try:
                    login = User()
                    print()
                    login.set_email(input("Email address: "))
                    userEmail = login.get_email()
                    query = "SELECT salt FROM user WHERE email = %s"
                    cursor.execute(query, (userEmail,))
                    for salt in cursor:
                        userSalt = ("{}".format(salt))
                        userSalt = userSalt.replace("'","")
                        userSalt = userSalt.replace("(","")
                        userSalt = userSalt.replace(")","")
                        userSalt = userSalt.replace(",","")
                    query = "SELECT passwordHash FROM user WHERE email = %s"
                    cursor.execute(query, (userEmail,))
                    for passwordHash in cursor:
                        userHPassword = ("{}".format(passwordHash))
                        userHPassword = userHPassword.replace("'","")
                        userHPassword = userHPassword.replace("(","")
                        userHPassword = userHPassword.replace(")","")
                        userHPassword = userHPassword.replace(",","")
                    check = check_password(userSalt, userHPassword, input("Password: "))
                    break
                # If the email entered does not exist and a salt cannot be selected,
                # the error will be dealt with using exception handling
                except:
                    print("Error! An account with this email does not exist")
                    print()
                    login_menu()

            # If the email does exist in the database and the passwords match,
            # the user is sent to the User Menu        
            if check == True:
                email = login.get_email()
                login.set_user_id(email)
                name = name_selector(login.get_user_id())
                print()
                print("Login Successful")
                print("Welcome,", name)
                user_menu(login.get_email(), login.get_user_id())

            #If the password does not match, the user is sent back to the Login Menu    
            else:
                print("Error! Incorrect password")
                print()
                login_menu()

        # The user has chosen to create an account        
        elif choice == "2":
            loginMenuValid = True

            while True:
                # The program will go through each field required to create an account.
                # If one of the fields causes an error, the user is sent back to the Login Menu
                try:
                    print()
                    new = User()
                    new.set_first_name(input("First Name: "))
                    new.set_last_name(input("Last Name: "))
                    new.set_email(input("Email address: "))
                    new.set_salt()
                    new.set_password_hash(input("Password: "), new.get_salt())
                    new.set_profile(0)
                    new.add_user()
                    new.set_user_id(new.get_email())
                    break  
                except:
                    print()
                    print("Error! An account with that email already exists")
                    login_menu()

            user_menu(new.get_email(), new.get_user_id())
                
        # If the User has chosen to exit the program, the program will close    
        elif choice == "0":
            loginMenuValid = True
            exit()
            
        else:
            print("Error! Input must be an integer preceding one of the options above")
            
def user_menu(signedInUserEmail, signedInUserId):
    time.sleep(0.4)
    print()
    print("     __  ______    _____   __   __  __________   ____  __")
    print("    /  |/  /   |  /  _/ | / /  /  |/  / ____/ | / / / / /")
    print("   / /|_/ / /| |  / //  |/ /  / /|_/ / __/ /  |/ / / / / ")
    print("  / /  / / ___ |_/ // /|  /  / /  / / /___/ /|  / /_/ /  ")
    print(" /_/  /_/_/  |_/___/_/ |_/  /_/  /_/_____/_/ |_/\____/   ")
    print()
    print()
    time.sleep(0.4)
    print(" 1. Take A Quiz")
    print(" 2. Create A Quiz")
    print(" 3. Delete A Quiz")
    print(" 4. View Profile")
    print(" 5. View Leaderboards")
    print(" 0. Logout")
    print()

    # This while loop will validate the user's choice of action at the Main Menu
    mainMenuValid = False  
    while mainMenuValid is False:
        choice = input("Select 1, 2, 3, 4, 5 or 0: ")

        # This choice will take the user to the Take Menu
        if choice == "1":
            mainMenuValid = True
            take_quizzes_menu(signedInUserEmail, signedInUserId)

        # This choice will take the user to the Create Quiz Menu       
        elif choice == "2":
            mainMenuValid = True
            create_quiz_menu(signedInUserEmail, signedInUserId)

        # This choice will take the user to the Modify Menu
        elif choice == "3":
            mainMenuValid = True
            delete_menu(signedInUserEmail, signedInUserId)

        # This choice will retrieve the user's total accumulated quiz points and display them on screen
        elif choice == "4":
            mainMenuValid = True
            userTotalScore = select_query_executor("SELECT profile FROM user WHERE id = " + signedInUserId)
            print()
            print("Total Quiz Points Earned:", userTotalScore)
            print()
            
            # A while loop to check if the user wants to go back to the Main Menu
            goBackFromProfile = False
            while goBackFromProfile is False:
                print("0. Go Back")
                goBack = input()
                
                if goBack == "0":
                    goBackFromProfile = True
                    time.sleep(0.5)
                    user_menu(signedInUserEmail, signedInUserId)
                    
                else:
                    print("Error! Must type '0' to go back to the Menu")
                    print()


        # This choice will take the user to the Leader boards Menu
        elif choice == "5":
            mainMenuValid = True
            leaderboard_menu(signedInUserEmail, signedInUserId)
            
        # This choice will take the user back to the Login Menu by breaking the loop causing 'Login_menu()' to trigger
        elif choice == "0":
            mainMenuValid = True

        else:
            print("Error! Input must be an integer preceding one of the options above")
            print()
        
    login_menu()

def take_quizzes_menu(signedInUserEmail, signedInUserId):
    time.sleep(0.4)
    print()
    print("   _________    __ __ ______   ____  __  ___________")
    print("  /_  __/   |  / //_// ____/  / __ \/ / / /  _/__  /")
    print("   / / / /| | / ,<  / __/    / / / / / / // /   / / ")
    print("  / / / ___ |/ /| |/ /___   / /_/ / /_/ // /   / /__")
    print(" /_/ /_/  |_/_/ |_/_____/   \___\_\____/___/  /____/")
    print()
    print()

    # 'select_all_quizzes()' returns all the necessary information for printing all quizzes in the quiz table
    availableRecordIds, availableHostIds, availableTitles, availableTypes, availableMaxScores, availableContents = select_all_quizzes()

    # This for loop prints every quiz found with 'select_all_quizzes()'
    for i in range(len(availableRecordIds)):
        time.sleep(0.25)
        HostName = name_selector(availableHostIds[i])
        print("ID:", availableRecordIds[i], "\n"
              "Quiz Title:", availableTitles[i], "\n"
              "Created by:", HostName, "\n"
              "Question Type:", availableTypes[i], "\n"
              "Maximum Score:", availableMaxScores[i], "\n"
              "Description:", availableContents[i])
        print("\n")

    # This while loop will check if the user's quiz selection is in the list of quizzes displayed
    quizSelectionValid = False
    while quizSelectionValid is False:

        # This while loop makes sure that the ID entered is an integer
        while True:            
            try:
                quizSelection = int(input("Select a quiz ID or '0' to go back: "))
                break     
            except:
                print("Errror! That's not an ID")
                print()

        # This if statement checks that the integer is in the list of available Quiz IDs
        if quizSelection in availableRecordIds:
            quizSelectionValid = True
            quizSelection = str(quizSelection)
            scoreCount = 0
            takeTitle = select_query_executor("SELECT title FROM quiz WHERE id = " + quizSelection)

            # Here, the user has a chance to back out of taking the quiz.
            # Their answer to the [Y/N] question is then validated
            takeQuizYNvalid = False
            while takeQuizYNvalid is False:
                print()
                print("Are you sure you want to take this quiz? [Y/N]: ", takeTitle)
                choice = input()
                choice = choice.upper()

                # If they have entered 'Y' they will go on to take the quiz
                if choice == "Y":
                    takeQuizYNvalid = True

                    # The user is asked if they want the question order randomised.
                    # Their answer to the [Y/N] question is then validated 
                    validYNRandOrder = False
                    while validYNRandOrder is False:
                        print()
                        print("Would you like to randomise the question order? [Y/N]")
                        randOrderChoice = input()
                        randOrderChoice = randOrderChoice.upper()

                        if randOrderChoice == "Y":
                            validYNRandOrder = True
                            randOrder = True

                        elif randOrderChoice == "N":
                            validYNRandOrder = True
                            randOrder = False

                        else:
                            print("Error! Please enter Y or N")
                
                    # The object "takeQuiz" is created and its variables are set with the take setter subroutines
                    takeQuiz = Take()
                    takeQuiz.set_quiz_id(quizSelection)
                    takeQuiz.set_user_id(signedInUserId)
                    takeQuiz.set_quiz_id(quizSelection)
                    takeQuiz.set_score(0)
                    content = select_query_executor("SELECT content FROM quiz WHERE id = " + quizSelection)
                    takeQuiz.set_content(content)
                    takeQuiz.add_take()
                    takeQuiz.set_take_id()
                    scoreCount = 0

                    # The user is presented with the title and the description of the quiz they are about to take
                    print()
                    print(takeTitle)
                    print("Description:", content)

                    # All question IDs, types and contents are retrieved from the table (in order) and saved to lists
                    questions = []
                    questionTypes = []
                    questionIds = []
                    questions = select_all_strings_query_executor("SELECT content FROM quiz_question WHERE quizId = " + quizSelection)
                    questionTypes = select_all_strings_query_executor("SELECT type FROM quiz_question WHERE quizId = " + quizSelection)
                    questionIds = select_all_integers_query_executor("SELECT id FROM quiz_question WHERE quizId = " + quizSelection)

                    # If the user has selected to randomise the question order, this for loop will randomise each in the same way
                    if randOrder == True:
                        for i in range(len(questions)-1, 0, -1):
                            j = random.randint(0, i)
                            questions[i], questions[j] = questions[j], questions[i]
                            questionTypes[i], questionTypes[j] = questionTypes[j], questionTypes[i]
                            questionIds[i], questionIds[j] = questionIds[j], questionIds[i]

                    # For each question (Multiple-Choice or Open ended) the answers are retrieved from the database,
                    # alongside their corresponding correct value
                    # "1" - Correct
                    # "0" - Incorrect
                    for i in range(len(questions)):
                        if questionTypes[i] == "1":
                            multipleOptions = []
                            correctMCValues = []
                            multipleOptions = select_all_strings_query_executor("SELECT content FROM quiz_answer WHERE questionId = " + questionIds[i])
                            correctMCValues = select_all_integers_query_executor("SELECT correct FROM quiz_answer WHERE questionId = " + questionIds[i])

                            # Even if the question order is not random, the choices for a multiple choice question will always be random
                            # This will randomise the answer contents and the values determining if the answer choice is correct or not
                            # Both lists will be randomised the same way so their values still match up
                            for j in range(len(multipleOptions)-1, 0, -1):
                                k = random.randint(0, j)
                                multipleOptions[j], multipleOptions[k] = multipleOptions[k], multipleOptions[j]
                                correctMCValues[j], correctMCValues[k] = correctMCValues[k], correctMCValues[j]
                            
                        print()
                        print()    
                        print("Question", i+1)
                        print(questions[i])
                        print()     

                        # If the question type is multiple-choice, the answer options are printed
                        if questionTypes[i] == "1":
                            for j in range(len(multipleOptions)):
                                print(str(j+1) + ".", multipleOptions[j])

                            # This while loop will make sure the user's choice is valid
                            # Checking to see if the choice is an integer
                            # Checking if the choice is one of the available options
                            while True:
                                try:          
                                    print()
                                    takeOption = int(input("Enter your choice here: "))
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
                                        print("Error! Input must be an integer preceding one of the options above")
                                        print()
                                except:
                                    print("Error! Input must be an integer")
                                    print()

                            # If the value at position "takeOption - 1" in "correctMCValues" is 1, the chosen option is correct
                            # The user's score for the take is increased by one
                            if correctMCValues[takeOption - 1] == "1":
                                scoreCount += 1
                                print()
                                print("Correct")

                            # If the value is not "1" (is "0") the chosen option is incorrect
                            # The user's score for the take remains the same
                            else:
                                print()
                                print("Incorrect")

                        # If the question type for the question is open ended, all the necessary data is collected and stored in the "openEndedOption" object
                        if questionTypes[i] == "2":
                            openEndedOption = []
                            openEndedOption = select_query_executor("SELECT content FROM quiz_answer WHERE questionId = " + questionIds[i])
                            takeOption = input("Enter your answer here: ")
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

                            # If the user input matches the answer's content, the entered answer is correct
                            # This enetered answer is not case sensitive
                            # The user's score for the take is increased by one
                            if takeOption.upper() == openEndedOption.upper():
                                scoreCount += 1
                                print()
                                print("Correct")

                            # If the user's input does not match the answer's content, the entered answer is incorrect
                            # The user's score for the take remains the same
                            else:
                                print()
                                print("Incorrect")

                    # All the questions have been answered so the take is finished
                    print()
                    print("Take Finished!")
                    takeId = str(takeQuiz.get_take_id())
                    update_query_executor("UPDATE take SET score = " + str(scoreCount) + " WHERE id = " + takeId)
                    profileScore = select_query_executor("SELECT profile FROM user WHERE id = " + str(signedInUserId))
                    update_query_executor("UPDATE user SET profile = " + str(int(profileScore) + scoreCount) + " WHERE id = " + str(signedInUserId))
                    maxPossibleScore = select_query_executor("SELECT maxScore FROM quiz WHERE id = " + quizSelection)
                    profileScore = select_query_executor("SELECT profile FROM user WHERE id = " + str(signedInUserId))
                    
                    print("You scored", scoreCount, "out of", maxPossibleScore)
                    print()
                    print("Your total Quiz Points is now:", profileScore)
                    user_menu(signedInUserEmail, signedInUserId)

                # If the user does not want to take this test, they can back out and the take quizzes menu will display itself once more
                elif choice == "N":
                    takeQuizYNvalid = True
                    take_quizzes_menu(signedInUserEmail, signedInUserId)

                # If the user does not input either 'Y' or 'N' they are prompted to enter the input again
                else:
                    print("Error! Please enter Y or N")

        # If the user wants to go back to the main menu the loop will break
        elif quizSelection == 0:
            quizSelectionValid = True
                    
        else:
            print("Error! Please select an existing ID")
            print()

    user_menu(signedInUserEmail, signedInUserId)


def create_quiz_menu(signedInUserEmail, signedInUserId):
    time.sleep(0.4)
    print()
    print("    __________  _________  ____________   ____  __  ___________")
    print("   / ____/ __ \/ ____/   |/_  __/ ____/  / __ \/ / / /  _/__  /")
    print("  / /   / /_/ / __/ / /| | / / / __/    / / / / / / // /   / / ")
    print(" / /___/ _, _/ /___/ ___ |/ / / /___   / /_/ / /_/ // /   / /__")
    print(" \____/_/ |_/_____/_/  |_/_/ /_____/   \___\_\____/___/  /____/")
    print()
    print()
    # The user is immediately put into the process of creating a quiz
    # The user's inputs are recorded and temporarily stored in the 'quiz' object variables
    quiz = Quiz()
    quiz.set_host_id(signedInUserId)
    quiz.set_title(input("Quiz title: "))
    quiz.set_quiz_type()
    quiz.set_max_score()
    print()
    quiz.set_content(input("Quiz description: "))
    quiz.add_quiz() # Quiz is added to the database
    quiz.set_quiz_id()

    # Since each question is always worth one point, the max score is euqal to the number of questions in the quiz
    # So repeat the question create process a 'max score' amount of times
    for i in range(quiz.get_max_score()):
        # The user's inputs are recorded and temporarily stored in the 'question' object variables
        print()
        print("Question", i+1)
        question = Question()
        question.set_quiz_id(quiz.get_quiz_id())
        question.set_question_type(quiz.get_quiz_type())
        question.set_level(input("Easy[1], Medium[2] or Hard[3]: "))
        question.set_score()
        print()
        question.set_question_content(input("Question content: "))
        question.add_question() # Question is added to the database
        question.set_question_id()

        # If the user has chosen to create a multiple-choice question,
        # the user must input wrong answers as well as one right answer
        # The user can choose either two options (one right, one wrong) or four options (one right and three wrong) 
        if question.get_question_type() == "1":
            # The user's inputs are recorded and temporarily stored in the 'multipleChoice' object variables
            multipleChoice = Answer()
            multipleChoice.set_quiz_id(quiz.get_quiz_id())
            multipleChoice.set_question_id(question.get_question_id())
            numberOfOptions = multiple_choice_handling()
            for j in range(numberOfOptions):
                print()
                print("Option",j+1)
                if str(j) == "0":
                    print("You can only have one correct option. Enter your correct option first.")
                    multipleChoice.set_correct()
                    multipleChoice.set_answer_content(input("Question Content: "))
                    multipleChoice.add_answer() # The correct answer is added to the database       
                else:
                    print("Enter your incorrect option(s) now.")
                    multipleChoice.set_incorrect()
                    multipleChoice.set_answer_content(input("Question Content: "))
                    multipleChoice.add_answer() # The incorrect answer is added to the database
                print("Option",j+1,"has been created")

        # If the user has chosen to create an open ended question, the user must input just the right answer
        elif question.get_question_type() == "2":
            # The user's inputs are recorded and temporarily stored in the 'openEnded' object variables
            openEnded = Answer()
            openEnded.set_correct()
            openEnded.set_quiz_id(quiz.get_quiz_id())
            openEnded.set_question_id(question.get_question_id())
            openEnded.set_answer_content(input("Answer Content: "))
            openEnded.add_answer() # The correct answer is added to the database

        # If the user has chosen to create a quiz with mixed question types,
        # the user gets to choose whether each questions is open ended or multiple choice
        elif question.get_question_type() == "3":
            # This while loop will validate the user's input
            # Their choice must either be 'M' or 'O'
            mOrOValid = False
            while mOrOValid is False:
                multipleOrOpen = input("Multiple choice question or Open ended [M/O]: ")
                # If the user has chosen 'M', they go through the process for creating a multiple choice question
                if multipleOrOpen.upper() == "M":
                    mOrOValid = True
                    update_query_executor("UPDATE quiz_question SET type = 1 WHERE type = 3") # Since there is no 'question type 3',
                    multipleChoice = Answer()                                                 # the type needs to be set to multiple choice (type 1)
                    multipleChoice.set_quiz_id(quiz.get_quiz_id())                            # Type 3 is used as a palceholder for qeustions within a mixed quiz
                    multipleChoice.set_question_id(question.get_question_id())
                    numberOfOptions = multiple_choice_handling()
                    for j in range(numberOfOptions):
                        print()
                        print("Option",j+1)
                        if str(j) == "0":
                            print("You can only have one correct option. Enter your correct option first.")
                            multipleChoice.set_correct()
                            multipleChoice.set_answer_content(input("Content: "))
                            multipleChoice.add_answer()      
                        else:
                            print("Enter your incorrect option(s) now.")
                            multipleChoice.set_incorrect()
                            multipleChoice.set_answer_content(input("Content: "))
                            multipleChoice.add_answer()
                        print("Option",j+1,"has been created")
                    
                elif multipleOrOpen.upper() == "O":
                    mOrOValid = True
                    update_query_executor("UPDATE quiz_question SET type = 2 WHERE type = 3") # Since there is no 'question type 3',
                    openEnded = Answer()                                                      # the type needs to be set to open ended (type 2)
                    openEnded.set_correct()                                                   # Type 3 is used as a placeholder for questions withing a mixed quiz
                    openEnded.set_quiz_id(quiz.get_quiz_id())
                    openEnded.set_question_id(question.get_question_id())
                    openEnded.set_answer_content(input("Answer Content: "))
                    openEnded.add_answer()
                    
                else:
                    print("Error! Input must be either 'M' or 'O'")
                    print()

    # Once the quiz has been created, the user is notified that the creation process is over,
    # and is taken back to the user menu
    print()
    print("Quiz Creation Complete")
    user_menu(signedInUserEmail, signedInUserId) 
   
    

def delete_menu(signedInUserEmail, signedInUserId):
    time.sleep(0.4)
    print()
    print("     ____  ________    __________________")
    print("    / __ \/ ____/ /   / ____/_  __/ ____/")
    print("   / / / / __/ / /   / __/   / / / __/   ")
    print("  / /_/ / /___/ /___/ /___  / / / /___   ")
    print(" /_____/_____/_____/_____/ /_/ /_____/   ")
    print()
    print()                                       
    print("Select a quiz you want to delete")
    print()
    time.sleep(0.4)
    print("YOU CAN ONLY DELETE THE QUIZZES YOU HAVE MADE")
    time.sleep(2)
    # All the details of every quiz the user has created is collected for future use
    # The user can only modify their quizzes and no one elses
    availableRecordIds, availableHostIds, availableTitles, availableTypes, availableMaxScores, availableContents = select_users_quizzes(signedInUserId)

    # Using the retrieved data from each quiz the user has made,
    # print each quiz
    for i in range(len(availableRecordIds)):
        time.sleep(0.2)
        HostName = name_selector(availableHostIds[i])
        print()
        print("ID:", availableRecordIds[i], "\n"
              "Quiz Title:", availableTitles[i], "\n"
              "Created by:", HostName, "\n"
              "Question Type:", availableTypes[i], "\n"
              "Maximum Score:", availableMaxScores[i], "\n"
              "Description:", availableContents[i])
        print("\n")

    # This while loop checks if the ID entered is in the list of quiz IDs
    isIdInQuizIdList = False
    while isIdInQuizIdList is False:

        # This while loop checks that the ID entered is an integer
        while True:
                try:
                    deleteSelection = int(input("Select a quiz ID or '0' to go back: "))
                    break
                except:
                    print("Error! Please enter an integer")
                    print()

        # If the entered ID is in the list of available quizzes,
        #
        if deleteSelection in availableRecordIds:
            isIdInQuizIdList = True
            deleteSelection = str(deleteSelection)
            takeTitle = select_query_executor("SELECT title FROM quiz WHERE id = " + deleteSelection)
            print()
            
            # This while loop ask the user if they are sure they want to delete the quiz
            # The user's input is also validated and can only be 'Y' or 'N' (not case sensitive)
            deleteQuizYNValid = False
            while deleteQuizYNValid is False:
                print("Are you sure you want to delete this quiz [Y/N]: ", takeTitle)
                choice = input()
                choice = choice.upper()

                # If they are sure they want to delete the quiz, the quiz is deleted
                # However not just the quiz is deleted
                # To delete the quiz, all 'take answers', 'takes', 'quiz answers' and 'quiz questions' must be deleted first
                # The quiz is then deleted
                if choice == "Y":
                    deleteQuizYNValid = True
                    selectedTakeIds = select_all_integers_query_executor("SELECT id FROM take WHERE quizId = " + deleteSelection)
                    
                    for TakeId in selectedTakeIds:
                        update_query_executor("DELETE FROM take_answer WHERE takeId = " + TakeId)
                        
                    update_query_executor("DELETE FROM take WHERE quizId = " + deleteSelection)
                    update_query_executor("DELETE FROM quiz_answer WHERE quizId = " + deleteSelection)
                    update_query_executor("DELETE FROM quiz_question WHERE quizId = " + deleteSelection)
                    update_query_executor("DELETE FROM quiz WHERE id = " + deleteSelection)
                    # The user is notified of the quiz's deletion,
                    # and is taken back to the modify menu
                    print()
                    print("Your Quiz has been deleted")
                    delete_menu(signedInUserEmail, signedInUserId)

                elif choice == "N":
                    deleteQuizYNValid = True
                    print("Your Quiz has not been deleted")
                    delete_menu(signedInUserEmail, signedInUserId)

                else:
                    print("Error! Please enter either 'Y' or 'N'")
                    print()

        # If the user decided to go back to the user menu, the while loop will end
        elif deleteSelection == 0:
            isIdInQuizIdList = True

        else:
            print("Error! That ID doesn't exist")
            print()

    user_menu(signedInUserEmail, signedInUserId)



def leaderboard_menu(signedInUserEmail, signedInUserId):
    time.sleep(0.4)
    print()
    print("     __    _________    ____  __________  ____  ____  ___    ____  ____  _____")
    print("    / /   / ____/   |  / __ \/ ____/ __ \/ __ )/ __ \/   |  / __ \/ __ \/ ___/")
    print("   / /   / __/ / /| | / / / / __/ / /_/ / __  / / / / /| | / /_/ / / / /\__ \ ")
    print("  / /___/ /___/ ___ |/ /_/ / /___/ _, _/ /_/ / /_/ / ___ |/ _, _/ /_/ /___/ / ")
    print(" /_____/_____/_/  |_/_____/_____/_/ |_/_____/\____/_/  |_/_/ |_/_____//____/  ")
    print()
    print()
    print("1. View overall Leaderboard")
    print("2. View leaderboards per quiz")
    print("0. Go back")
    print()

    # This while loop validates the user's choice of action at the leaderboard menu
    leaderboardChoiceValid = False
    while leaderboardChoiceValid is False:
        choice = input("Select 1, 2 or 0: ")

        # If choice is '1' all user IDs are retreived from the database
        if choice == "1":
            leaderboardChoiceValid = True
            userIdList = select_all_integers_query_executor("SELECT id FROM user")
            userNameList = []
            scoreList = []
            userIdNameScoreList = []

            # For each user ID, their full name and profile score is retrieved
            for userId in userIdList:
                userName = name_selector(userId)
                userNameList.append(userName)
                profileScore = select_query_executor("SELECT profile FROM user WHERE id = " + userId)
                scoreList.append(profileScore)

            # For each user ID, their data is concatenated and added to a list as one item
            for i in range(len(userIdList)):
                userIdNameScore = ("USER ID: " + userIdList[i] + "  " + "USERNAME: " + userNameList[i] + "  " + "SCORE: " + scoreList[i])
                userIdNameScoreList.append(userIdNameScore)

            # All the user scores are ordered from highest to lowest
            # The concatenated user IDs, names and scores are ordered in the same way
            # This makes sure each user profile is matched up with their own score
            scoreList, userIdNameScoreList = zip(*sorted(zip(scoreList, userIdNameScoreList)))
            scoreList = scoreList[::-1]
            userIdNameScoreList = userIdNameScoreList[::-1]

            time.sleep(0.5)
            print()
            print()
            print("TOP 50 PLAYERS")
            print()

            # The top 50 highest scoring users are displayed one user at a time
            for i in range(len(scoreList[:50])):
                time.sleep(0.25)
                print(str(i+1) + ". " + str(userIdNameScoreList[i]))

            # After the top 50 users have been displayed, the user is asked if they want to return to the leaderboard menu
            # Their choice is validated
            print()
            goBackToLeaderboardsValid = False
            while goBackToLeaderboardsValid is False:
                print("0. Go Back")
                goBack = input()
                
                if goBack == "0":
                    goBackToLeaderboardsValid = True
                    leaderboard_menu(signedInUserEmail, signedInUserId)
                    
                else:
                    print("Error! Must enter '0' to go back")
                    print()
                    pass

        # If the user wants to view a specific leaderboard for a certain quiz,
        # all quizzes are displayed for the user to choose which one they want to select
        elif choice == "2":
            leaderboardChoiceValid = True
            availableRecordIds, availableHostIds, availableTitles, availableTypes, availableMaxScores, availableContents = select_all_quizzes()
            for i in range(len(availableRecordIds)):
                time.sleep(0.25)
                HostName = name_selector(availableHostIds[i])
                print()
                print("ID:", availableRecordIds[i], "\n"
                      "Quiz Title:", availableTitles[i], "\n"
                      "Created by:", HostName, "\n"
                      "Question Type:", availableTypes[i], "\n"
                      "Maximum Score:", availableMaxScores[i], "\n"
                      "Description:", availableContents[i])
                print("\n")

            # This while loop will check if the entered quiz ID is in the list of available quizIDs
            quizLeaderboardSelectionValid = False
            while quizLeaderboardSelectionValid is False:

                # This while loop will check if the entered ID is an integer
                while True:
                        try:
                            quizSelection = int(input("Select a quiz ID or '0' to go back: "))
                            break
                        except:
                            print("Error! Please enter an integer.")
                            print()

                # If the entered ID is in the list of quiz IDs,
                # Select the user ID and score for each user who has taken this quiz
                if quizSelection in availableRecordIds:
                        quizSelection = str(quizSelection)
                        userIdsOfQuizTakers = select_all_integers_query_executor("SELECT userId FROM take WHERE quizId = " + quizSelection)
                        scoreForEachTake = select_all_integers_query_executor("SELECT score FROM take WHERE quizId = " + quizSelection)
                        userNameList = []
                        userIdNameScoreList = []

                        # Gather each user's full name
                        for userId in userIdsOfQuizTakers:
                            userName = name_selector(userId)
                            userNameList.append(userName)

                        # If no one has taken the quiz, the following message is displayed
                        if userIdsOfQuizTakers == []:
                            time.sleep(0.5)
                            print()
                            print("No one has completed this quiz")
                            print()

                        # If other users have taken the quiz, each user is ordered from highest score to lowest score
                        else:
                            scoreForEachTake, userIdsOfQuizTakers, userNameList = zip(*sorted(zip(scoreForEachTake, userIdsOfQuizTakers, userNameList)))
                            userIdsOfQuizTakers = userIdsOfQuizTakers[::-1]
                            scoreForEachTake = scoreForEachTake[::-1]
                            userNameList = userNameList[::-1]
                            
                            for i in range(len(userIdsOfQuizTakers)):
                                userIdNameScore = ("USER ID: " + userIdsOfQuizTakers[i] + "  " + "USERNAME: " + userNameList[i] + "  " + "SCORE: " + scoreForEachTake[i])
                                userIdNameScoreList.append(userIdNameScore)

                            leaderBoardQuizTitle = select_query_executor("SELECT title FROM quiz WHERE id = " + quizSelection)
                            
                            time.sleep(0.5)
                            print()
                            print()
                            print("TOP 50 PLAYERS WHO COMPLETED:", leaderBoardQuizTitle)
                            print()
                            
                            for i in range(len(userIdsOfQuizTakers[:50])):
                                time.sleep(0.25)
                                print(str(i+1) + ". " + str(userIdNameScoreList[i]))

                            print()
                            goBackToLeaderboardsValid = False
                            while goBackToLeaderboardsValid is False:
                                print("0. Go Back")
                                goBack = input()
                                if goBack == "0":
                                    goBackToLeaderboardsValid = True
                                    leaderboard_menu(signedInUserEmail, signedInUserId)
                                    
                                else:
                                    print("Error! Must enter '0' to go back")
                                    print()

                elif quizSelection == 0:
                    quizLeaderboardSelectionValid = True
                    leaderboard_menu(signedInUserEmail, signedInUserId)

                else:
                    print("Error! That ID doesn't exist")
                    print()

        elif choice == "0":            
            break

        else:
            print("Error! Input must be an integer preceding one of the options above")
            print()
        
    user_menu(signedInUserEmail, signedInUserId)

# After the user has logged in with their MySQL account, the program runs by starting at the login_menu                       
login_menu()



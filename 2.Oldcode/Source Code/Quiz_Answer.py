import mysql.connector
from mysql.connector import errorcode

# Database connection established
def quiz_answer_connection(cnxUser, cnxPassword):
    global cnx
    global cursor
    cnx = mysql.connector.connect(user=cnxUser,
                                  password=cnxPassword,
                                  database='quiz')
    cursor = cnx.cursor()

# The class used for creating quiz answer objects
class Answer():

    # Each variable represents a field in the 'quiz_answer' table in the database
    def __init__(self):
        self.quizId           = ""
        self.questionId       = ""
        self.correct          = 0  # This variable can only store integers (1 or 0)
        self.answerContent    = ""


    # The setters used for setting all the data for the object variables
    
    def set_quiz_id(self, quizId):
        self.quizId = quizId

    def set_question_id(self, questionId):
        self.questionId = questionId

    def set_answer_content(self, answerContent):
        valid = False
        while valid is False:
            if len(answerContent) > 50:
                print("Error! Limit of 50 characters!")
                answerContent = input("Answer content: ")
            else:
                valid = True
                break
        self.answerContent = answerContent

    def set_correct(self):
        self.correct = 1

    def set_incorrect(self):
        self.correct = 0


    # The getters, for retrieving the data from the object variables 

    def get_quiz_id(self):
        return self.quizId

    def get_question_id(self):
        return self.questionId

    def get_correct(self):
        return self.correct

    def get_answer_content(self):
        return self.answerContent


    # This is the function which uses the object variables
    # to add a quiz to the 'quiz_answer' table

    def add_answer(self):
        query = ("INSERT INTO quiz_answer"
                 "(quizId, questionId, correct, content) "
                 "VALUES (%s, %s, %s, %s)")
        answerData = (self.quizId, self.questionId, self.correct, self.answerContent)
        cursor.execute(query, answerData)
        cnx.commit()
        emp_no = cursor.lastrowid
        

# This is a function used to determine whether a user wants to have
# 2 multiple choice option or 4
# The function vaidates the process and returns the number of chosen options
def multiple_choice_handling():
    print()
    numberOfOptionsValid = False
    numberOfOptions = input("Number of options [2 or 4]: ")
    while numberOfOptionsValid == False:
        if numberOfOptions == "2":
            numberOfOptionsValid = True
            numberOfOptions = int(numberOfOptions)
        elif numberOfOptions == "4":
            numberOfOptionsValid = True
            numberOfOptions = int(numberOfOptions)
        else:
            numberOfOptions = input("Number of options [2 or 4]: ")             
    return numberOfOptions



        

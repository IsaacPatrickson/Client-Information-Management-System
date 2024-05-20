import mysql.connector
from mysql.connector import errorcode

# Database connection established
def take_answer_connection(cnxUser, cnxPassword):
    global cnx
    global cursor
    cnx = mysql.connector.connect(user=cnxUser,
                                  password=cnxPassword,
                                  database='quiz')
    cursor = cnx.cursor()

# The class used for creating take answers
class Take_Answer():

    # Each variable represents a field in the 'take_answer' table in the database
    def __init__(self):
        self.takeId               = ""
        self.questionId           = ""
        self.answerId             = ""
        self.takeAnswerContent    = ""


    # The setters used for setting all the data for the object variables

    def set_take_id(self, takeId):
        self.takeId = takeId

    def set_question_id(self, questionId):
        self.questionId = questionId

    def set_answer_id(self, answerId):
        self.answerId = answerId

    def set_answer_content(self, answerContent):
        valid = False
        while valid is False:
            if len(answerContent) > 50:
                print("Error! Limit of 50 characters!")
                answerContent = input("Enter your answer here: ")
            else:
                valid = True
                break
        self.answerContent = answerContent


    # The getters, for retrieving the data from the object variables 

    def get_quiz_id(self):
        return self.quizId

    def get_question_id(self):
        return self.questionId

    def get_answer_id(self):
        return self.answerId

    def get_take_answer_content(self):
        return self.takeAnswerContent


    # This is the function which uses the object variables
    # to add a take answer to the 'take_answer' table

    def add_take_answer(self):
        query = ("INSERT INTO take_answer"
                 "(takeId, questionId, answerId, content) "
                 "VALUES (%s, %s, %s, %s)")
        takeAnswerData = (self.takeId, self.questionId, self.answerId, self.answerContent)
        cursor.execute(query, takeAnswerData)
        cnx.commit()
        emp_no = cursor.lastrowid        

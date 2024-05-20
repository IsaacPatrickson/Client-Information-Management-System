import mysql.connector
from mysql.connector import errorcode

# Database connection established
def quiz_question_connection(cnxUser, cnxPassword):
    global cnx
    global cursor
    cnx = mysql.connector.connect(user=cnxUser,
                                  password=cnxPassword,
                                  database='quiz')
    cursor = cnx.cursor()

# The class used for creating question objects
class Question():

    # Each variable represents a field in the 'quiz_question' table in the database
    def __init__(self):
        self.questionId       = ""
        self.quizId           = ""
        self.questionType     = ""
        self.level            = ""
        self.score            = ""
        self.questionContent  = ""


    # The setters used for setting all the data for the object variables

    def set_question_id(self):
        questionId = cursor.lastrowid
        self.questionId = questionId

    def set_quiz_id(self, quizId):
        self.quizId = quizId

    def set_question_type(self, questionType):
        self.questionType = questionType

    def set_level(self, level):
        levelValid = False
        while levelValid is False:
            if level == "1":
                levelValid = True
                self.level = level
            elif level == "2":
                levelValid = True
                self.level = level
            elif level == "3":
                levelValid = True
                self.level = level
            else:
                print("Error! Input 1, 2 or 3")
                print()
                level = input("Easy[1], Medium[2] or Hard[3]: ")

    def set_score(self):
        self.score = 1

    def set_question_content(self, content):
        valid = False
        while valid is False:
            if len(content) > 50:
                print("Error! Limit of 50 characters!")
                content = input("Question content: ")
            else:
                valid = True
                break
        self.questionContent = content


    # The getters, for retrieving the data from the object variables 

    def get_question_id(self):
        return self.questionId
    
    def get_quiz_id(self):
        return self.quizId

    def get_question_type(self):
        return self.questionType

    def get_level(self):
        return self.level

    def get_score(self):
        return self.score

    def get_question_content(self):
        return self.questionContent


    # This is the function which uses the object variables
    # to add a quiz question to the 'quiz_question' table

    def add_question(self):
        query = ("INSERT INTO quiz_question"
                 "(quizId, type, level, score, content) "
                 "VALUES (%s, %s, %s, %s, %s)")
        questionData = (self.quizId, self.questionType, self.level, self.score,
                        self.questionContent)
        cursor.execute(query, questionData)
        cnx.commit()
        emp_no = cursor.lastrowid
        print()
        print("Your Question has been created")        
        







    
        
        

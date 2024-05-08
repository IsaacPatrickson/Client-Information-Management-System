import mysql.connector
from mysql.connector import errorcode

# Database connection established
def take_connection(cnxUser, cnxPassword):
    global cnx
    global cursor
    cnx = mysql.connector.connect(user=cnxUser,
                                  password=cnxPassword,
                                  database='quiz')
    cursor = cnx.cursor()

# The class used for creating take objects
class Take():

    # Each variable represents a field in the 'take' table in the database
    def __init__(self):
        self.takeId  = ""
        self.userId  = ""
        self.quizId  = ""
        self.score   = 0    # The score variable only stores integers
        self.content = ""


    # The setters used for setting all the data for the object variables

    def set_take_id(self):
        takeId = cursor.lastrowid
        self.takeId = takeId
    
    def set_user_id(self, userId):
        self.userId = userId
        
    def set_quiz_id(self, quizId):
        self.quizId = quizId

    def set_score(self, score):
        self.score = score

    def set_content(self, content):
        self.content = content


    # The getters, for retrieving the data from the object variables     

    def get_take_id(self):
        return self.takeId

    def get_user_id(self):
        return self.userId
    
    def get_quiz_id(self):
        return self.quizId

    def get_score(self):
        return self.score

    def get_content(self):
        return self.content


    # This is the function which uses the object variables
    # to add a take to the 'take' table

    def add_take(self):
        query = ("INSERT INTO take"
                 "(userId, quizId, score, content) "
                 "VALUES (%s, %s, %s, %s)")
        takeData = (self.userId, self.quizId, self.score, self.content)
        cursor.execute(query, takeData)
        cnx.commit()
        emp_no = cursor.lastrowid
        print()
        print("You have begun taking the quiz")





        

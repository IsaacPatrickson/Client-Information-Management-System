import mysql.connector

# Database connection established
def quiz_connection(cnxUser, cnxPassword):
    global cnx
    global cursor
    cnx = mysql.connector.connect(user=cnxUser,
                                  password=cnxPassword,
                                  database='quiz')
    cursor = cnx.cursor()

# The class used for creating 'quiz' objects
class Quiz():

    # Each variable represents a field in the 'quiz' table in the database
    def __init__(self):
        self.quizId    = ""
        self.hostId    = ""
        self.title     = ""
        self.type      = ""
        self.maxScore  = ""
        self.content   = ""


    # The setters used for setting all the data for the object variables
    
    def set_quiz_id(self):
        quizId = cursor.lastrowid
        self.quizId = quizId

    def set_host_id(self, hostId):
        self.hostId = hostId

    def set_title(self, title):
        titleValid = False
        while titleValid is False:
            if len(title) > 75:
                print("Error! Limit of 75 characters!")
                title = input("Title: ")
            else:
                titleValid = True
        self.title = title

    def set_quiz_type(self):
        print()
        print("Quiz type:")
        print()
        print(" 1. Multiple Choice")
        print(" 2. Open-ended Answer")
        print(" 3. Mixed")
        print()
        quizTypeValid = False
        quizType = input("Select 1, 2 or 3: ")
        while quizTypeValid is False:
            if quizType == "1":
                quizTypeValid = True
                self.quizType = quizType
            elif quizType == "2":
                quizTypeValid = True
                self.quizType = quizType
            elif quizType == "3":
                quizTypeValid = True
                self.quizType = quizType
            else:
                quizType = input("Error! Please enter 1, 2 or 3: ")

    def set_max_score(self):
        print()
        numberOfQuestionsValid = False
        while numberOfQuestionsValid is False:
            while True:
                try:
                    maxScore = int(input("Number of questions in your quiz [1-50]: "))
                    break
                except ValueError:
                    print("Error! Input must be an integer")

            if maxScore > 0 and maxScore <= 50:
                numberOfQuestionsValid = True
                self.maxScore = maxScore
            else:
                print("Error! Integer must be between 1 and 50")


    def set_content(self, content):
        valid = False
        while valid is False:
            if len(content) > 50:
                print("Error! Limit of 50 characters!")
                content = input("Quiz description: ")
            else:
                valid = True
                break
        self.content = content


    # The getters, for retrieving the data from the object variables    

    def get_quiz_id(self):
        return self.quizId

    def get_hostId(self):
        return self.hostId

    def get_title(self):
        return self.title

    def get_quiz_type(self):
        return self.quizType

    def get_max_score(self):
        return self.maxScore

    def get_content(self):
        return self.content


    # This is the function which uses the object variables
    # to add a quiz to the 'quiz' table

    def add_quiz(self):
        query = ("INSERT INTO quiz"
                 "(hostId, title, type, maxScore, content) "
                 "VALUES (%s, %s, %s, %s, %s)")
        quizData = (self.hostId, self.title, self.quizType, self.maxScore, self.content)
        cursor.execute(query, quizData)
        cnx.commit()
        emp_no = cursor.lastrowid
        print()
        print("Quiz created. Now for the questions.")
        
        
    
        

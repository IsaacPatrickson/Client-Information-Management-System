import mysql.connector
from mysql.connector import errorcode

# Database connection established
def sql_executor_connection(cnxUser, cnxPassword):
    global cnx
    global cursor
    cnx = mysql.connector.connect(user=cnxUser,
                                  password=cnxPassword,
                                  database='quiz')
    cursor = cnx.cursor()

# This function takes a select query as a parameter and executes it
# The select query should select one string or integer
# The value selected is then formatted so it can be used in other algorithms
def select_query_executor(query):
    cursor.execute(query)
    for data in cursor:
        data = ("{}".format(data))
        data = data.replace("'","")
        data = data.replace("(","")
        data = data.replace(")","")
        data = data.replace(",","")
    return data

# This function takes a select query as a parameter and executes it
# The select query should select more than one string
# All strings selected are formatted so they can be used in other algorithms
def select_all_strings_query_executor(query):
    cursor.execute(query)
    records = cursor.fetchall()
    recordList = []
    for record in records:
        record = ("{}".format(record))
        record = record[2:]
        record = record[:-3]
        recordList.append(record)
    return recordList        

# This function takes a select query as a parameter and executes it
# The select query should select more than one integer
# All integers selected are formatted so they can be used in other algorithms
def select_all_integers_query_executor(query):
    cursor.execute(query)
    integers = cursor.fetchall()
    integerList = []
    for integer in integers:
        integer = str(integer)
        integer = integer.replace("(","")
        integer = integer.replace(")","")
        integer = integer.replace(",","")
        integerList.append(integer)
    return integerList   

# This function is used for executing UPDATE and DELETE queries
def update_query_executor(query):
    cursor.execute(query)
    cnx.commit()

# This function retrieves all data about each quiz
# Each list represent a field in a table
# Since each field contains a values, the indexes should match up
# Therefore the data in index 5 of each list will be the data about quiz 5
# Full names are also retrieved, using the quiz's host ID
def select_all_quizzes():
    availableRecordIds = []
    availableHostIds = []
    availableTitles = []
    availableTypes = []
    availableMaxScores = []
    avaiableContents = []
    query = "SELECT * FROM quiz"
    cursor.execute(query)
    quizTable = cursor.fetchall()
    if quizTable == []:
        print("No quizzes have been made yet")
        print()
    else:   
        for record in quizTable:
            recordId = record[0]
            recordHostId = record[1]
            recordTitle = record[2]
            recordType = record[3]
            if recordType == 1:
                recordType = "Multiple Choice"
                
            elif recordType == 2:
                recordType = "Open Ended"
                 
            elif recordType == 3:
                recordType = "Mixed"
                
            recordMaxScore = record[4]
            recordContent = record[5]
            quizCreatorName = name_selector(recordHostId)
            availableRecordIds.append(recordId)
            availableHostIds.append(recordHostId)
            availableTitles.append(recordTitle)
            availableTypes.append(recordType)
            availableMaxScores.append(recordMaxScore)
            avaiableContents.append(recordContent)

    return availableRecordIds, availableHostIds, availableTitles, availableTypes, availableMaxScores, avaiableContents

# This function retrieves all data about each quiz the logged in user has made
# Each list represent a field in a table
# Since each field contains a values, the indexes should match up
# Therefore the data in index 5 of each list will be the data about quiz 5
# Full names are also retrieved, using the quiz's host ID
# Since this function is only retrieving quizzes made by the logged in user,
# All quizzes have the same Host ID and therefore the same creator name
def select_users_quizzes(signedInUserId):
    availableRecordIds = []
    availableHostIds = []
    availableTitles = []
    availableTypes = []
    availableMaxScores = []
    avaiableContents = []
    query = "SELECT * FROM quiz WHERE hostId = " + str(signedInUserId)
    cursor.execute(query)
    quizTable = cursor.fetchall()
    if quizTable == []:
        print("No quizzes have been made yet")
        print()
    else: 
        for record in quizTable:
            recordId = record[0]
            recordHostId = signedInUserId
            recordTitle = record[2]
            recordType = record[3]
            if recordType == 1:
                recordType = "Multiple Choice"
                
            elif recordType == 2:
                recordType = "Open Ended"
                 
            elif recordType == 3:
                recordType = "Mixed"
                
            recordMaxScore = record[4]
            recordContent = record[5]
            quizCreatorName = name_selector(recordHostId)
            availableRecordIds.append(recordId)
            availableHostIds.append(recordHostId)
            availableTitles.append(recordTitle)
            availableTypes.append(recordType)
            availableMaxScores.append(recordMaxScore)
            avaiableContents.append(recordContent)

    return availableRecordIds, availableHostIds, availableTitles, availableTypes, availableMaxScores, avaiableContents


# This function uses the id of a user to retireve the user's full name
# Their first name and last name are concatenated with a space in the middle,
# to create their full name
def name_selector(signedInUserId):
    name = ""
    query = "SELECT firstName, lastName FROM user WHERE id = %s"
    cursor.execute(query, (signedInUserId,))
    for firstName, lastName in cursor:
        name = str(("{}".format(firstName) + " " + "{}".format(lastName)))
    return name


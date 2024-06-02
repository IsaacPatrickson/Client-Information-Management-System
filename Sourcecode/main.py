import sqlite3
import pandas as pd
import re
from itertools import zip_longest
import inspect
import ast
from SQLiteDatabase.InitDatabase import *
from SQLQueries import *
from userClass import *
from clientClass import *

# Connect to a (new) database
def conntectToDatabase():
    try:
        connection = sqlite3.connect("SQLiteDatabase/mediaworksUsersAndClients.db")
        return connection
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")

# Login menu is the main branch of the program
# The login process is executed 
# and depending on the user permissions different options are presented
def main():
    connection = conntectToDatabase()
    cursor = connection.cursor()
    # Functions that create the 'users' and the 'clients' table
    createUsersTable(cursor)
    createClientsTable(cursor)

    # Check if the tables are already populated and hardcode values accordingly
    hardcodeValues(cursor, isTablePopulated(sqlite3, cursor, "users") 
                and isTablePopulated(sqlite3, cursor, "clients"))
    # This while loop will help validate the user's choice of action at the Login Menu
    # 'loginMenuValid' is True when the user has successfully entered a valid choice
    # and the loop ends
    loginMenuValid = False
    while loginMenuValid == False:
        print()
        print("MAIN MENU")
        print()
        print(" 1. Login")
        print(" 0. Quit")
        print()
        choice = input("Select 1 or 0: ")
        # User enters '1' and is prompted to ennter a username to log in
        if choice == "1":
            loginMenuValid = True
            login = User()
            # This while loop will help validate the user's username
            # If the username is not alpha (spaces included)
            # and the username is not in the database, the user will be prompted to enter a username again
            userNameInput = False
            while userNameInput == False:
                inputName = input("(Enter '0' to Abort) Enter your username: ")
                if validateUserName(re, inputName):
                    if isUserNameInTable(selectAttribute(cursor, "userName", "users", "userName", inputName)):
                        userNameInput = True
                        login.setExistingUserName(inputName)
                        login.setLoginStatus(True)
                        print("Login successful")
                        print()
                        print(f"Welcome to the Client Information Management System, {inputName}")
                    else:
                        print("An error occurred: The entered username is not in our database")
                else:
                    if inputName == "0":
                        userNameInput = True
                        loginMenuValid = False
                        print("Login aborted")
                    else:
                        print("An error occurred: Username must contain alpha characters (spaces included)")

            # Systems checks if user has successfully logged in
            # and displays the 'clients' table using the pandas package
            while login.getLoginStatus() == True:
                permissionLevel = []
                clientsTable = getTableWithPandas(pd, connection, "clients")
                print()
                print()
                print(clientsTable)
                
                # The permission value for the logged in user is retrieved from the 'users' table and stored in a list
                # and a for loop retrieves the value
                # A for loop needs to be used as the permission value is stored in a tuple even though it is just one value
                permissionValues = selectAttribute(cursor, "permissionLevel", "users", "userName", inputName)
                for permissionValue in permissionValues:
                    login.setExistingPermissionLevel(permissionValue)
                
                # If the user's permission value is greated than or equal to 5 they are presented the Admin menu
                # Admins can amend, add, delete and search for clients
                # Both admin and employee can log out
                permissionLevel = login.getPermissionLevel()
                if permissionLevel >= 5:
                    # A while loop that validates the users input on the menu screen
                    validChoice = False
                    while validChoice == False:
                        choice = []
                        print()
                        print()
                        print("ADMIN MENU")
                        print()
                        print("(1) Amend client information")
                        print("(2) Add a client")
                        print("(3) Delete a client")
                        print("(4) Search for clients")
                        print("(0) Log out")
                        print()
                        choice = input("Enter (0-4) to select an option: ")
                        # Each choice (except log out) calls a function
                        # corresponding to the action the user wants to execute
                        if choice == "1":
                            validChoice = True
                            amendClientInformation(cursor)
                        elif choice == "2":
                            validChoice = True
                            addClient(cursor)
                        elif choice == "3":
                            validChoice = True
                            removeClient(cursor)
                        elif choice == "4":
                            validChoice = True
                            searchClients(connection, cursor)
                        elif choice == "0":
                            validChoice = True
                            print()
                            print("Log out successful")
                            login.setLoginStatus(False)
                        else:
                            print("An error occurred: Input must be an integer between (0-4)")
                        
                # If the user's permission value is less than 5 they are presented the Employee menu
                # Employees can search for clients
                elif permissionLevel < 5:
                    # A while loop that validates the users input on the menu screen
                    validChoice = False
                    while validChoice == False:
                        choice = []
                        print()
                        print()
                        print("EMPLOYEE MENU")
                        print()
                        print("(1) Search for clients")
                        print("(0) Log out")
                        print()
                        choice = input("Enter (0-1) to select an option: ")
                        if choice == "1":
                            validChoice = True
                            searchClients(connection, cursor)                                                
                        elif choice == "0":
                            validChoice = True
                            print()
                            login.setLoginStatus(False)
                        else:
                            print("An error occurred: Input must be an integer between (0-1)")
            loginMenuValid = False
            
        # If the User has chosen to exit the program, the program will start the exit process    
        elif choice == "0":
            # This while loop asks the user if they are sure if they want to exit the program
            # user input is validated
            sureValid = False
            while sureValid == False:
                isUserSure = input("You are okay with exiting the system (Y/N): ")
                if isUserSure.upper() == "Y":
                    sureValid = True
                    loginMenuValid = True
                    break
                elif isUserSure.upper() == "N":
                    sureValid = True
                    print()
                    print("Exit aborted")
                else:
                    print(f"An error occurred: {isUserSure} is not 'Y' or 'N'")
        # If the user did not input a '1' to log in or a '0' to exit
        # they are prompted to enter either a '1' or a '0'
        else:
            print("An error occurred: Input must be an integer (0-1)")
     
    # Committing all changes to the database once the user has decided to exit the system
    # If for whatever reason the system stops before the user exits
    # all changes will be reverted
    connection.commit()

    # Close connection
    connection.close()
    print("System exit successful")
    exit()
        
            
def amendClientInformation(cursor):
    # A while loop that validates the user input on the amend menu
    ammendOptionValid = False
    while ammendOptionValid == False:
        abort = False
        print()
        print()
        print("AMEND CLIENT INFORMATION")
        print()
        print("To abort enter '000'")
        iDofClientToAmend = input("Enter the clientID of the details you want to amend: ")
        if iDofClientToAmend == "000":
            ammendOptionValid = True
            print("Amend process aborted")
        # Client ID is in the table therefore the amend process continues
        # The user should not be able to amend a record that doesn't exist
        elif checkIfInputInTable(cursor, "clientID", "clients", iDofClientToAmend) == True:
            fieldToModify = input("Select an attribute to modify ('000' to abort): ")
            # ClientID cannot be modified as it is the unique identifier for each record
            if fieldToModify == "clientID":
                print()
                print(f"An error occurred: {fieldToModify} is the primary key, this cannot be modified")
            # If the field the user chose to amend matches a column name in the 'clients' table
            # and is not 'clientID' the user will be asked to enter a replacement value
            # The system checks if this value's datatype matches the column's datatype
            # If they match the value is valid to be updated
            elif attributeNameMatchClientColumnName(cursor, fieldToModify):
                replacementValue = input("Input the replacement value ('000' to abort): ")
                if replacementValue == "000":
                    ammendOptionValid = True
                    print()
                    print("Add process aborted")
                # The answer must be 60 characters or less
                elif len(replacementValue) > 60:
                    print("The length of each answer must be below 60 characters")
                elif compareDatatypes(cursor, replacementValue, "clients", fieldToModify):
                    # If the datatype is BOOLEAN the replacement value must either be '1' or '0'
                    if getColumnDataType(cursor, "clients", fieldToModify) == "BOOLEAN":
                        while replacementValue != "1" and replacementValue != "0":
                            replacementValue = input("Replacement value for for BOOLEAN fileds must be '1' or '0' ('000' to abort): ")
                            if replacementValue == "000":
                                ammendOptionValid = True
                                abort = True
                                print()
                                print("Add process aborted")
                    if abort == False:            
                        replaceAttribute(cursor, "clients", fieldToModify, replacementValue, "clientID", iDofClientToAmend)
                        print()
                        print("Attribute amended successfully")
                        ammendOptionValid = True
                else:               
                    print(f"An error occurred: The datatype of {replacementValue} does not match the datatype of that field")
        elif checkIfInputInTable(cursor, "clientID", "clients", iDofClientToAmend) == False:
            print(f"An error occurred: {iDofClientToAmend} does not exist as a clientID in the clients table")
        else:
            print(f"An error occurred: {iDofClientToAmend} is an invalid clientID! A clientID must be an integer")
       
def addClient(cursor):
    # A while loop that validates the user input on the add menu
    addProcessComplete = False
    while addProcessComplete == False:
        print()
        print()
        print("ADD CLIENT INFORMATION")
        print()
        print("To abort enter '000'")
        clientToAdd = Client()
        # Gathering all the column names excluding clientID
        # ClientID is incremented automatically
        # The user does not need to input a clientID
        columnNames = getColumnNames(cursor)
        for columnName in columnNames:
            if columnName == "clientID":
                columnNames.remove(columnName)
            else:
                pass
        # Creating a list of questions relating to each column name
        questions = [
                    "Client name: ", 
                    "Contract status ('1'=Active/'0'=Inactive): ",
                    "Contract start date: ",
                    "Contract end date: ",
                    "Contract includes project work ('1'=Yes/'0'=No): ",
                    "Longitude of client HQ: ",
                    "Latitude of client HQ: ",
                    "Estimated total revenue: "
                    ]
        # Getting all the 'Client' methods in order of appearance
        methods = getMethodNamesInOrder(Client)
        # Merging all three lists into one list
        # Each item in the new list contains a list containing three items
        # The length of the new merged list will be the length of the shortest list
        # This shouldn't be a problem as all lists should be the same length
        # This is just a precaution and makes the code more robust
        mergedColNamesQuestionsMethods = [[a, b, c] for a, b, c in zip_longest(columnNames, questions, methods)]
        # For each item in the new list, gather an input by asking the question
        # stored in the merged list value
        abort = False
        for ColQuestionMethod in mergedColNamesQuestionsMethods:
            answerValid = False
            while answerValid == False:
                answer = input(ColQuestionMethod[1])
                # If the answer is '000' the process is aborted
                # I chose to use '000' instead of '0' as '0'
                # because '0' can be a valid and common input for a client value
                if answer == "000":
                    answerValid = True
                    abort = True
                    print()
                    print("Add process aborted")
                # The answer must be 60 characters or less
                elif len(answer) > 60:
                    print("The length of each answer must be below 60 characters")
                # The datatype of the answer must match the column
                # The corresponding column is retrieved from the merged list item
                elif compareDatatypes(cursor, answer, "clients", ColQuestionMethod[0]):
                    answerValid = True
                    method = getattr(clientToAdd, ColQuestionMethod[2])
                    method(answer)
                else:
                    print("The datatype of the answer you entered does not match the field")
            if abort:
                addProcessComplete = True
                break
        
        # If the user has not aborted, the attribute values are retrieved
        # from the 'clientToAdd' instance of Client
        # The values are inserted into the 'clients' table, forming a new client record 
        if abort == False:    
            answerValues = [clientToAdd.getClientName(),
                            clientToAdd.getContractStatus(),
                            clientToAdd.getContractStartDate(),
                            clientToAdd.getContractEndDate(),
                            clientToAdd.getProjectBasedWork(),
                            clientToAdd.getHqLongitude(),
                            clientToAdd.getHqLatitude(),
                            clientToAdd.getEstimatedTotalRevenue()]
            insertInto(cursor, "clients", columnNames, answerValues)
            print("Client successfully added to table")
            addProcessComplete = True
       
def removeClient(cursor):
    # A while loop that validates the user input on the remove menu
    removeOptionValid = False
    while removeOptionValid == False:
        print()
        print()
        print("REMOVE CLIENT INFORMATION")
        print()
        print("To abort enter '0'")
        iDofClientToRemove = input("Enter the clientID of the details you want to remove: ")
        if iDofClientToRemove == "0":
            removeOptionValid = True
            print()
            print("Delete process aborted")
        # Client ID is in the table therefore the delete process continues
        # The user should not be able to delete a record that doesn't exist
        elif checkIfInputInTable(cursor, "clientID", "clients", iDofClientToRemove) == True:
            removeOptionValid = True
            # This while loop asks the user if they are sure if they want to delete the selected record
            # user input is validated
            sureValid = False
            while sureValid == False:
                isUserSure = input("You are okay with this record being permanently deleted from the database (Y/N): ")
                if isUserSure.upper() == "Y":
                    sureValid = True
                    removeRecord(cursor, "clients", "clientID", iDofClientToRemove)
                    print("Client successfully deleted from the database")
                elif isUserSure.upper() == "N":
                    sureValid = True
                    print()
                    print("Delete process aborted")
                else:
                    print(f"An error occurred: {isUserSure} is not 'Y' or 'N'")
                    
        elif checkIfInputInTable(cursor, "clientID", "clients", iDofClientToRemove) == False:
            print(f"An error occurred: {iDofClientToRemove} does not exist as a clientID in the clients table")
        else:
            print(f"An error occurred: {iDofClientToRemove} is an invalid clientID! A clientID must be an integer")
              
def searchClients(connection, cursor):
    # A while loop that validates the user input on the search menu
    searchOptionValid = False
    while searchOptionValid == False:
        print()
        print()
        print("SEARCH FOR CLIENTS")
        print()
        print("To abort enter '0'")
        attributeToSearchBy = input("Enter the attribute you want to search by: ")
        if attributeToSearchBy == "0":
            searchOptionValid = True
            print("Search process aborted")
        # If the process has not been aborted and the input attribute name (aka field name)
        # matches a column name in the table the process continues
        elif attributeNameMatchClientColumnName(cursor, attributeToSearchBy) == True:
            valueToSearchFor = input("Enter the value this attribute needs to have: ")
            # The search results are stored in 'searchResults' using pandas
            searchResults = str(selectAttributesWithPandas(pd, connection, "*", "clients", attributeToSearchBy, valueToSearchFor))
            # If 'searchResults' is not empty, display the table of search results
            if "Empty DataFrame" not in searchResults:
                print()
                print("Search successfull")
                print()
                print(searchResults)
            # If the table is empty, display search error message
            else:
                print()
                print("An error occurred: No results match that search")
        elif attributeNameMatchClientColumnName(cursor, attributeToSearchBy) == False:
            print("An error occurred: The attribute you have selected does not exist as a column in the clients table")
        else:
            print(f"An error occurred: {attributeToSearchBy} is an invalid attribute name")                
       
def compareDatatypes(cursor, inputValue, tableName, columnName):
    columnDatatype = getColumnDataType(cursor, tableName, columnName)
    # A dictionary that assings a SQLite column datatype to a usable python datatype
    datatypeMap = {
        "INTEGER": int,
        "BOOLEAN": int,
        "TEXT": str,
        "REAL": float,
        "BLOB": bytes,
        "NUMERIC": float
    }
    # Check if the input value can be represented as an int or a float
    # before assuming its always a string
    convertedInputValue = detectAndConvertInput(inputValue)
    # If types match return true
    # If types do not match return false
    inputDatatype = type(convertedInputValue)
    if inputDatatype == datatypeMap.get(columnDatatype.upper()):
        return True
    else:
        return False               
                   
def detectAndConvertInput(userInput):
    try:
        # Try to convert the input to a float first
        float_value = float(userInput)
        # Check if the float value can be represented as an integer
        if float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except ValueError:
        # If conversion to float fails, return the input as a string
        return userInput
    
def getMethodNamesInOrder(className):
    # Uses the inspect package to inspect a class
    source = inspect.getsource(className)
    # Stores the classes methods and relationships in a 'tree'  
    tree = ast.parse(source)
    # Navigating the tree to get methods that are not protected or getters
    methods = [node.name for node in tree.body[0].body 
               if isinstance(node, ast.FunctionDef) 
               and not node.name.startswith("__")
               and not node.name.startswith("get")]
    return methods

# Checks if an input attribute name (aka field name) matches a colum in a table
def attributeNameMatchClientColumnName(cursor, attributeName):
    columnNames = getColumnNames(cursor)
    for columnName in columnNames:
        if attributeName == columnName:
            return True
        else:
            pass
    return False  
    
    
if __name__ == "__main__":
    main()
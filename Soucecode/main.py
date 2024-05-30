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
try:
    connection = sqlite3.connect("SQLiteDatabase/mediaworksUsersAndClients.db")
    cursor = connection.cursor()
except sqlite3.OperationalError as e:
    print(f"An error occurred: {e}")
    
createUsersTable(cursor)
createClientsTable(cursor)
hardcodeValues(cursor, isTablePopulated(sqlite3, cursor, "users") 
               and isTablePopulated(sqlite3, cursor, "clients"))
# checkTableContents(cursor)

# Displays the login menu   
def login_menu():
    # This while loop will validate the user's choice of action at the Login Menu
    loginMenuValid = False
    while loginMenuValid == False:
        print()
        print("MAIN MENU")
        print()
        print(" 1. Login")
        print(" 0. Quit")
        print()
        choice = input("Select 1 or 0: ")
        if choice == "1":
            loginMenuValid = True
            login = User()
            userNameInput = False
            while userNameInput == False:
                inputName = input("(Enter '0' to Abort) Enter your username: ")
                if validateUserName(re, inputName):
                    if login.isUserNameInTable(selectAttribute(cursor, "userName", "users", "userName", inputName)):
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
            
            while login.getLoginStatus() == True:
                permissionLevel = []
                clientsTable = getTableWithPandas(pd, connection, "clients")
                
                print()
                print()
                print(clientsTable)
                permissionValues = selectAttribute(cursor, "permissionLevel", "users", "userName", inputName)
                for permissionValue in permissionValues:
                    login.setExistingPermissionLevel(permissionValue)
                

                permissionLevel = login.getPermissionLevel()
                
                if permissionLevel >= 5:
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
                        if choice == "1":
                            validChoice = True
                            amendClientInformation()
                        elif choice == "2":
                            validChoice = True
                            addClient()
                        elif choice == "3":
                            validChoice = True
                            removeClient()
                        elif choice == "4":
                            validChoice = True
                            searchClients()
                        elif choice == "0":
                            validChoice = True
                            print()
                            print("Log out successful")
                            login.setLoginStatus(False)
                        else:
                            print("An error occurred: Input must be an integer between (0-4)")
                        
                        
                elif permissionLevel < 5:
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
                            searchClients()                                                
                        elif choice == "0":
                            validChoice = True
                            print()
                            login.setLoginStatus(False)
                        else:
                            print("An error occurred: Input must be an integer between (0-1)")
            loginMenuValid = False
        # If the User has chosen to exit the program, the program will close    
        elif choice == "0":
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
        else:
            print("An error occurred: Input must be an integer (0-1)")
            
    # Committing all changes to the database
    connection.commit()

    # Close connection
    connection.close()
    print("System exit successful")
    exit()
        
            
def amendClientInformation():
    ammendOptionValid = False
    while ammendOptionValid == False:
        print()
        print()
        print("AMEND CLIENT INFORMATION")
        print()
        print("To abort enter '0'")
        iDofClientToAmend = input("Enter the clientID of the details you want to amend: ")
        if iDofClientToAmend == "0":
            ammendOptionValid = True
            print("Amend process aborted")
            
        elif checkIfInputInTable(cursor, "clientID", "clients", iDofClientToAmend) == True:
            fieldToModify = input("Select an attribute to modify: ")
            if fieldToModify == "clientID":
                print()
                print(f"An error occurred: {fieldToModify} is the primary key, this cannot be modified")
                
                
            elif attributeNameMatchClientColumnName(cursor, fieldToModify):
                replacementValue = input("Input the replacement value: ")
                if compareDatatypes(cursor, replacementValue, "clients", fieldToModify):
                    if getColumnDataType(cursor, "clients", fieldToModify) == "BOOLEAN":
                        while replacementValue != "1" and replacementValue != "0":
                            replacementValue = input("Replacement value for for BOOLEAN fileds must be '1' or '0': ")
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
       
def addClient():
    addProcessComplete = False
    while addProcessComplete == False:
        print()
        print()
        print("ADD CLIENT INFORMATION")
        print()
        print("To abort enter '000'")
        clientToAdd = Client()
        columnNames = getColumnNames(cursor)
        for columnName in columnNames:
            if columnName == "clientID":
                columnNames.remove(columnName)
            else:
                pass
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
        methods = getMethodNamesInOrder(Client)
        mergedColNamesQuestionsMethods = [[a, b, c] for a, b, c in zip_longest(columnNames, questions, methods)]
        abort = False
        for ColQuestionMethod in mergedColNamesQuestionsMethods:
            answerValid = False
            while answerValid == False:
                answer = input(ColQuestionMethod[1]) 
                if answer == "000":
                    answerValid = True
                    abort = True
                    print()
                    print("Add process aborted")
                elif len(answer) > 60:
                    print("The length of each answer must be below 60 characters")
                elif compareDatatypes(cursor, answer, "clients", ColQuestionMethod[0]):
                    answerValid = True
                    method = getattr(clientToAdd, ColQuestionMethod[2])
                    method(answer)
                else:
                    print("The datatype of the answer you entered does not match the field")
            if abort:
                addProcessComplete = True
                break
        
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
       
def removeClient():
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
        elif checkIfInputInTable(cursor, "clientID", "clients", iDofClientToRemove) == True:
            removeOptionValid = True
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
              
def searchClients():
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
        elif attributeNameMatchClientColumnName(cursor, attributeToSearchBy) == True:
            valueToSearchFor = input("Enter the value this attribute needs to have: ")
            searchResults = str(selectAttributesWithPandas(pd, connection, "*", "clients", attributeToSearchBy, valueToSearchFor))
            if "Empty DataFrame" not in searchResults:
                print()
                print("Search successfull")
                print()
                print(searchResults)
            else:
                print()
                print("An error occurred: No results match that search")
        elif attributeNameMatchClientColumnName(cursor, attributeToSearchBy) == False:
            print("An error occurred: The attribute you have selected does not exist as a column in the clients table")
        else:
            print(f"An error occurred: {attributeToSearchBy} is an invalid attribute name")                
       
def compareDatatypes(cursor, inputValue, tableName, columnName):
    columnDatatype = getColumnDataType(cursor, tableName, columnName)
    datatypeMap = {
        "INTEGER": int,
        "BOOLEAN": int,
        "TEXT": str,
        "REAL": float,
        "BLOB": bytes,
        "NUMERIC": float
    }
    
    convertedInputValue = detectAndConvertInput(inputValue)
    
    inputDatatype = type(convertedInputValue)
    if inputDatatype == datatypeMap.get(columnDatatype.upper()):
        return True
    else:
        return False               
                   
def detectAndConvertInput(inputValue):
    try:            
        # Tries to convert the input to an integer
        convertedValue = int(inputValue)
        return convertedValue
    except ValueError:
        # If conversion fails, try to convert to float
        try:
            convertedValue = float(inputValue)
            return convertedValue
        except ValueError:
            # If both conversions fail, return the original input (assumed to be a string)
            return inputValue            
    
def getMethodNamesInOrder(className):
    source = inspect.getsource(className)  
    tree = ast.parse(source)
    methods = [node.name for node in tree.body[0].body 
               if isinstance(node, ast.FunctionDef) 
               and not node.name.startswith("__")
               and not node.name.startswith("get")]
    return methods
    
    
login_menu()
    
    

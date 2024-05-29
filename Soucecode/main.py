import sqlite3
import time
import pandas as pd
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
hardcodeValues(cursor, isTablePopulated(cursor, "users") and isTablePopulated(cursor, "clients"))
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
                if validateUserName(inputName):
                    if login.isUserNameInTable(selectAttribute(cursor, "userName", "users", "userName", inputName)):
                        userNameInput = True
                        login.setExistingUserName(inputName)
                        login.setLoginStatus(True)
                        print(f"Welcome to the Client Information Management System, {inputName}")
                    else:
                        print("The entered username is not in our database")
                        time.sleep(3)
                else:
                    if inputName == "0":
                        userNameInput = True
                        loginMenuValid = False
                    else:
                        print("Characters must belong to the alphabet (spaces included)")
                        time.sleep(3)
            
            while login.getLoginStatus() == True:
                permissionLevel = []
                clientsTable = getTableWithPandas(pd, connection, "clients")
                
                print()
                print()
                time.sleep(2)
                print(clientsTable)
                permissionValues = selectAttribute(cursor, "permissionLevel", "users", "userName", inputName)
                for permissionValue in permissionValues:
                    login.setExistingPermissionLevel(permissionValue)
                

                permissionLevel = login.getPermissionLevel()
                
                if permissionLevel == 9:
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
                            ammendClients()
                        elif choice == "2":
                            validChoice = True
                            print("Add")
                        elif choice == "3":
                            validChoice = True
                            print("Remove")  
                        elif choice == "4":
                            validChoice = True
                            searchClients()
                        elif choice == "0":
                            validChoice = True
                            print()
                            login.setLoginStatus(False)
                        else:
                            print("Input must be an integer between (0-4)")
                            time.sleep(3)
                        
                        
                elif permissionLevel == 1:
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
                            print("Input must be an integer between (0-1)")
                            time.sleep(3)
                    
            loginMenuValid = False
            
                        
                        
            
                
        # If the User has chosen to exit the program, the program will close    
        elif choice == "0":
            loginMenuValid = True
            break
            
        else:
            print("Error! Input must be an integer (0-1)")
            time.sleep(3)
            
    # Committing all changes to the database
    connection.commit()

    # Close connection
    connection.close()
    exit()
    
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
        elif attributeNameMatchClientColumnName(cursor, attributeToSearchBy) == True:
            valueToSearchFor = input("Enter the value this attribute needs to have: ")
            searchResults = str(selectAttributesWithPandas(pd, connection, "*", "clients", attributeToSearchBy, valueToSearchFor))
            if "Empty DataFrame" not in searchResults:
                print()
                print(searchResults)
                time.sleep(2)
            else:
                print()
                print("No results match that search")
        elif attributeNameMatchClientColumnName(cursor, attributeToSearchBy) == False:
            print("The attribute you have selected does not exist as a column in the clients table")
        else:
            print(f"{attributeToSearchBy} is an invalid attribute name! Enter '0' to abort")        
    
def ammendClients():
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
            
        elif checkIfInputInTable(cursor, "clientID", "clients", iDofClientToAmend) == True:
            fieldToModify = input("Select an attribute to modify: ")
            if fieldToModify == "clientID":
                print()
                print(f"{fieldToModify} is the primary key, this cannot be modified")
                
                
            elif attributeNameMatchClientColumnName(cursor, fieldToModify):
                replacementValue = input("Input the replacement value: ")
                if compareDatatypes(cursor, replacementValue, "clients", fieldToModify):
                    replaceAttribute(cursor, "clients", fieldToModify, replacementValue, "clientID", iDofClientToAmend)
                    print()
                    print("Attribute amended successfully")
                    time.sleep(2)
                    ammendOptionValid = True
                else:               
                    print(f"The datatype of {replacementValue} does not match the datatype of that field")
        elif checkIfInputInTable(cursor, "clientID", "clients", iDofClientToAmend) == False:
            print(f"{iDofClientToAmend} does not exist as a clientID in the clients table")
        else:
            print(f"{iDofClientToAmend} is an invalid clientID! A clientID must be an integer")
       
       
       
       
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
    
    
    
    
    
login_menu()
    
    

import sqlite3
import time
import pandas as pd
from SQLiteDatabase.InitDatabase import *
from userClass import *

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
    # I have used time.sleep to create an animation for the title's appearancee.
    # This style choice mimmicks that of an old computer and gives my program more character
    print()
    print(" 1. Login")
    print(" 0. Quit")
    print()

    # This while loop will validate the user's choice of action at the Login Menu
    loginMenuValid = False
    while loginMenuValid == False:
        choice = input("Select 1 or 0: ")
        
        if choice == "1":
            loginMenuValid = True
            
            login = User()
            userNameInput = False
            while userNameInput == False:
                inputName = input("(Enter '0' to Abort) Enter your username: ")
                if login.validateUserName(inputName):
                    if login.isUserNameInTable(cursor, inputName):
                        login.setExistingUserName(inputName)
                        login.setLoginStatus(True)
                        print(f"Welcome, {inputName}")
                        userNameInput = True
                    else:
                        print("The entered username is not in our database")
                        time.sleep(3)
                else:
                    if inputName == "0":
                        login_menu()
                    else:
                        print("Characters must belong to the alphabet (spaces included)")
                        time.sleep(3)
            
            while login.getLoginStatus() == True:
                print(pd.read_sql_query("SELECT * FROM users", connection))
                # # Fetch the table data
                # cursor.execute("SELECT * FROM users")
                # rows = cursor.fetchall()

                # # Fetch the column names
                # column_names = [description[0] for description in cursor.description]

                # # Print the column names
                # print(" | ".join(column_names))
                # print("-" * (len(column_names) * 10))

                # # Print each row
                # for row in rows:
                #     print(" | ".join(str(item) for item in row))
                
                break
                # login.setExistingPermissionLevel(cursor, inputName)
                # if login.getPermissionLevel() == 9:
                # elif login.getPermissionLevel() == 1:
            
            
            
            # if login.setExistingUserName(login.isUserNameInTable(cursor, inputName), inputName):
            #     print(f"Welcome, {inputName}")
            # else:
            #     pass
                
            # if login.validateUserName(inputName):
            #     try:
            #         login.isUserNameInTable(cursor, inputName)
            #     except sqlite3.OperationalError as e:
            #         print(f"An error occurred: {e}")
            # else:
            #     print("Invalid name! Please enter only alphabetic characters and spaces.")
            
            # print(login.getUserName)
            #         print()
            #         login.set_email(input("Email address: "))
            #         userEmail = login.get_email()
            #         query = "SELECT salt FROM user WHERE email = %s"
            #         cursor.execute(query, (userEmail,))
            #         for salt in cursor:
            #             userSalt = ("{}".format(salt))
            #             userSalt = userSalt.replace("'","")
            #             userSalt = userSalt.replace("(","")
            #             userSalt = userSalt.replace(")","")
            #             userSalt = userSalt.replace(",","")
            #         query = "SELECT passwordHash FROM user WHERE email = %s"
            #         cursor.execute(query, (userEmail,))
            #         for passwordHash in cursor:
            #             userHPassword = ("{}".format(passwordHash))
            #             userHPassword = userHPassword.replace("'","")
            #             userHPassword = userHPassword.replace("(","")
            #             userHPassword = userHPassword.replace(")","")
            #             userHPassword = userHPassword.replace(",","")
            #         check = check_password(userSalt, userHPassword, input("Password: "))
            #         break
            # #     # If the email entered does not exist and a salt cannot be selected,
            # #     # the error will be dealt with using exception handling
                # except:
                #     print("Error! An account with this email does not exist")
                #     print()
                #     login_menu()

            # # If the email does exist in the database and the passwords match,
            # # the user is sent to the User Menu        
            # if check == True:
            #     email = login.get_email()
            #     login.set_user_id(email)
            #     name = name_selector(login.get_user_id())
            #     print()
            #     print("Login Successful")
            #     print("Welcome,", name)
            #     user_menu(login.get_email(), login.get_user_id())

            # If the password does not match, the user is sent back to the Login Menu    
            # else:
            #     print("Error! Incorrect username")
            #     print()
            #     login_menu()
                
        # If the User has chosen to exit the program, the program will close    
        elif choice == "0":
            loginMenuValid = True
            exit()
            
        else:
            print("Error! Input must be an integer preceding one of the options above")   
    
    
    
    
    
login_menu()
    
    
    
# Committing all changes to the database
connection.commit()

# Close connection
connection.close()
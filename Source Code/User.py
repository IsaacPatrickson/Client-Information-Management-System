import mysql.connector
import hashlib, binascii, os

# Database connection established
def user_connection(cnxUser, cnxPassword):
    global cnx
    global cursor
    cnx = mysql.connector.connect(user=cnxUser,
                                  password=cnxPassword,
                                  database='quiz')
    cursor = cnx.cursor()

# The class used for creating 'user' objects
class User():

    # Each variable represents a field in the 'user' table in the database
    def __init__(self):
        self.userId       = ""
        self.firstName    = ""
        self.lastName     = ""
        self.email        = ""
        self.salt         = ""
        self.passwordHash = ""
        self.profile      = 0


    # The setters used for setting all the data for the object variables

    def set_user_id(self, email):
        query = "SELECT id FROM user WHERE email = %s"
        cursor.execute(query, (email,))
        for selectedId in cursor:
            selectedId = ("{}".format(selectedId))
            selectedId = selectedId.replace("'","")
            selectedId = selectedId.replace("(","")
            selectedId = selectedId.replace(")","")
            selectedId = selectedId.replace(",","")
        self.userId  = selectedId     

    def set_first_name(self, firstName):
        valid = False
        while valid is False:
            if not str(firstName).isalpha():
                print("Error! Only letters a-z allowed!")
                firstName = input("First Name: ")
            elif len(firstName) > 50:
                print("Error! Limit of 50 characters!")
                firstName = input("First Name: ")
            else:
                valid = True
                break
        self.firstName = firstName

    def set_last_name(self, lastName):
        valid = False
        while valid is False:
            if not str(lastName).isalpha():
                print("Error! Only letters a-z allowed!")
                lastName = input("Last Name: ")
            elif len(lastName) > 50:
                print("Error! Limit of 50 characters!")
                lastName = input("Last Name: ")
            else:
                valid = True
                break
        self.lastName = lastName

    def set_email(self, email):
        valid = False
        while valid == False:
            if "@" not in email:
                print("Error! Must include '@' symbol!")
                email = input("Email address: ")
            elif len(email) > 50:
                print("Error! Limit of 50 characters!")
                email = input("Email address: ")
            elif " " in email:
                print("Error! No spaces allowed!")
                email = input("Email address: ")         
            else:
                valid = True
                break
        self.email = email

    # The salt is set in the user class. If I were to instead call the 'salt()' function,
    # there would be an UnboundLocalError
    def set_salt(self):
        salt = hashlib.sha256(os.urandom(60)).hexdigest()
        self.salt = salt

    # The hashed password is set in the user class. If I were to instead call the 'hash_password()' function,
    # there would be an UnboundLocalError
    # The entered password has to be at least 8 characters
    def set_password_hash(self, password, salt):
        valid = False
        while valid is False:
            if len(password) < 8:
                print("Error! Password must be at least 8 characters")
                print()
                password = input("Password: ")
            else:
                valid = True
        salt = salt.encode('ascii')
        passwordHash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                       salt, 100000)
        passwordHash = binascii.hexlify(passwordHash)
        (passwordHash).decode('ascii')
        self.passwordHash = passwordHash

    def set_profile(self, profile):
        self.profile = profile


    # The getters, for retrieving the data from the object variables 

    def get_user_id(self):
        return self.userId 

    def get_first_name(self):
        return self.firstName

    def get_last_name(self):
        return self.lastName

    def get_email(self):
        return self.email

    def get_salt(self):
        return self.salt

    def get_password_hash(self):
        return self.passwordHash

    def get_profile(self):
        return self.profile

    def get_user_salt(self):
        return self.selectedSalt

    def get_user_hashed_password(self):
        return self.selectedPassword

    # This is the function which uses the object variables
    # to add a user to the 'user' table

    def add_user(self):
        query = ("INSERT INTO user"
                 "(firstName, lastName, email, salt, passwordHash, profile) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        userData = (self.firstName, self.lastName, self.email, self.salt,
                    self.passwordHash, self.profile)
        cursor.execute(query, userData)
        cnx.commit()
        emp_no = cursor.lastrowid
        print("Your Account has been created")



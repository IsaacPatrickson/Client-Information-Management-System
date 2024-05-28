import re

class User():
    
    def __init__(self) -> None:
        self.userName        = ""
        self.permissionLevel = ""
        self.loginStatus     = False
        
    def validateUserName(self, inputName):
        # Creating a pattern using the Regular Expressions(RE) library
        # The pattern includes all letters of the alphabet (uppercase and lowercase) and blank spaces
        pattern = r'^[a-zA-Z\s]+$'
        
        # Using the RE library, I have check if the input matches the pattern
        if re.match(pattern, inputName):
            return True
        else:
            return False
        
    def isUserNameInTable(self, cursor, inputName):
        cursor.execute("SELECT userName FROM users WHERE userName = ?", (inputName,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
            
    def setExistingPermissionLevel(self, cursor, inputName):
        cursor.execute("SELECT permissionLevel FROM users WHERE userName = ?", (inputName,))
        result = cursor.fetchone()
        self.permissionLevel = result     
            
    def setExistingUserName(self, inputName):
        self.userName = inputName
        
    def setLoginStatus(self, loginStatus):
        self.loginStatus = loginStatus
        
    def getUserName(self):
        return self.userName
    
    def getPermissionLevel(self):
        return self.permissionLevel
    
    def getLoginStatus(self):
        return self.loginStatus
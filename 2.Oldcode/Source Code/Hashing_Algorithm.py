import hashlib, binascii, os

# Generates a salt for combining with the account password
def salt():
    salt = hashlib.sha256(os.urandom(60)).hexdigest()
    return salt

# Uses the hashing algorithm SHA-512 to create a hashed password,
# out of the account password and the salt
def hash_password(password, salt):
    salt = salt.encode('ascii')
    passwordHash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                   salt, 100000)
    passwordHash = binascii.hexlify(passwordHash)
    return(passwordHash).decode('ascii')

# Uses the retrieved salt and an entered password to create a hashed password
# If that hashed password matches the stored hashed password,
# the function returns True
def check_password(salt, storedPasswordHash, enteredPassword):
    passwordHash = hashlib.pbkdf2_hmac('sha512', enteredPassword.encode('utf-8'),
                   salt.encode('ascii'), 100000)
    passwordHash = binascii.hexlify(passwordHash).decode('ascii')
    return passwordHash == storedPasswordHash


#salt = salt()
#print(salt)
#storedPasswordHash = hash_password(input('Set your password: '), salt)
#print(storedPasswordHash)
#print(check_password(salt, storedPasswordHash, input('Enter your password: ')))

# Compares the entered password with the stored one

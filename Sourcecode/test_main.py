import sqlite3
import pytest
from main import *

@pytest.fixture
def dbConnection():
    # Setup: creates a temporary in-memory database and table
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE users(
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        userName TEXT NOT NULL,
        permissionLevel INT NOT NULL
        )""")
    cursor.execute("""CREATE TABLE clients(
        clientID INTEGER PRIMARY KEY AUTOINCREMENT,
        clientName TEXT NOT NULL,
        contractStatus BOOLEAN NOT NULL,
        contractStartDate TEXT,
        contractEndDate TEXT,
        projectWork BOOLEAN NOT NULL,
        hqLongitude REAL,
        hqLatitude REAL,
        estimatedTotalRevenue REAL
        )""")
    conn.commit()
    yield conn, cursor  # Provides the connection and cursor to the test
    # Teardown: closes the cursor and connection
    cursor.close()
    conn.close()


def testCompareDatatypes(dbConnection):
    conn, cursor = dbConnection
    stringTest = "HelloWorld"
    integerTest = 1
    floatTest = 1.1342234
    characterLimitTest = "dfhbnjsevbag345579vbvbu@#~@@egfyuae~]!u879ovberbcvuhegyuivhbusyfs"
    # assert compareDatatypes(cursor, stringTest, "clients", "hqLatitude") == False
    # assert compareDatatypes(cursor, integerTest, "clients", "hqLatitude") == False
    # assert compareDatatypes(cursor, floatTest, "clients", "hqLatitude") == True
    # assert compareDatatypes(cursor, characterLimitTest, "clients", "hqLatitude") == False
    
def testDetectAndConvertInput(dbConnection):
    conn, cursor = dbConnection
    stringTest = "HelloWorld"
    integerTest = 1
    floatTest = 1.1342234
    characterLimitTest = "dfhbnjsevbag345579vbvbu@#~@@egfyuae~]!u879ovberbcvuhegyuivhbusyfs"
    assert detectAndConvertInput(stringTest) == "HelloWorld"
    assert detectAndConvertInput(integerTest) == 1
    assert detectAndConvertInput(floatTest) == 1.1342234
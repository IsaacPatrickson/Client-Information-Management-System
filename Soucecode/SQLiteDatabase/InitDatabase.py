def createUsersTable(cursor):
    # Create users table
    initUsersTable = """CREATE TABLE IF NOT EXISTS users(
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        userName TEXT NOT NULL,
        permissionLevel INT NOT NULL
        )"""
    # Executing the command that creates the users table
    cursor.execute(initUsersTable)

def createClientsTable(cursor):
    # Create clients table
    initClientsTable = """CREATE TABLE IF NOT EXISTS clients(
        clientID INTEGER PRIMARY KEY AUTOINCREMENT,
        clientName TEXT NOT NULL,
        contractStatus BOOLEAN NOT NULL,
        contractStartDate TEXT,
        contractEndDate TEXT,
        projectWork BOOLEAN NOT NULL,
        hqLongitude REAL,
        hqLatitude REAL,
        estimatedTotalRevenue REAL
        )"""
    # Executing the command that creates the clients table
    cursor.execute(initClientsTable)

def isTablePopulated(sqlite3, cursor, tableName):
    # SQL query to count the number of rows in the table
    query = f"SELECT COUNT(*) FROM {tableName}"
    
    try:
        # Execute the query
        cursor.execute(query)
        
        # Fetch the result
        count = cursor.fetchone()[0]
        
        # Check if the table is populated
        if count > 0:
            return True
        else:
            return False
    except sqlite3.OperationalError as e:
        # Handle case where the table does not exist
        print(f"An error occurred: {e}")
        return False

def hardcodeValues(cursor, populated):
    if populated:
        pass
    else:
        # Add to users
        # cursor.execute("INSERT INTO users VALUES (1, 'Isaac Patrickson', 9)")
        columns = ["userName", "permissionLevel"]
        rows = [
            ('Isaac Patrickson', 9),
            ('John Doe', 1),
            ('Jane Doe', 2),
            ('Jacob Doe', 3),
            ('Jamie Doe', 4),
            ('Jonathan Doe', 5),
            ('Jemima Doe', 6),
            ('Jade Doe', 7),
            ('Jasper Doe', 8),
            ('Jessie Doe', 1)
        ]
        query = f"INSERT INTO {"users"} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})"
        cursor.executemany(query, rows)
               
        # Add to clients
        columns = ["clientName", "contractStatus", "contractStartDate", "contractEndDate", "projectWork", "hqLongitude", "hqLatitude", "estimatedTotalRevenue"]
        rows = [
            ('VetPartners', "TRUE", '25-03-2024', '', "TRUE", 53.98797, -1.10369, 650000.00),
            ('SouthernWater', "TRUE", '12-02-2023', '17-08-2024', "FALSE", 50.82407, -0.42637, 750000.00),
            ('Stonebridge', "TRUE", '02-02-2024', '15-06-2025', "TRUE", 158.0954, 7.6217, 200000.00),
            ('DCC Propane', "FALSE", '01-06-2022', '26-07-2023', "TRUE", 32.4100, 9.0015, 150000.00),
            ('Reconomy', "TRUE", '04-01-2024', '15-01-2025', "TRUE", 81.5597, -82.9807, 125000.00),
            ('LEGO', "FALSE", '15-06-2024', '', "FALSE", -138.1759, -15.8445, 900000.00),
            ('SkipsandBins', "TRUE", '11-10-2023', '04-09-2024', "FALSE", 141.7670, 9.2339, 75000.00),
            ('Altus', "FALSE", '05-05-2023', '22-01-2024', "FALSE", 69.9109, -5.7904, 30000.00),
            ('Serios Group', "TRUE", '27-06-2024', '', "TRUE", -28.2190, 33.1939, 75000.00),
            ('Zentia', "TRUE", '19-04-2023', '', "TRUE", 97.0081, 3.3163, 500000.00)
        ]
        query = f"INSERT INTO {"clients"} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})"
        cursor.executemany(query, rows)
        
def checkTableContents(cursor):
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
    cursor.execute("SELECT * FROM clients")
    results = cursor.fetchall()
    print(results)
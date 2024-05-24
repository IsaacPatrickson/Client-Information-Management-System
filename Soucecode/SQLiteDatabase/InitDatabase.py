import sqlite3

# Connect to a (new) database
conn = sqlite3.connect("SQLiteDatabase/mediaworksUsersAndClients.db")
cursor = conn.cursor()

# Create users table
initUsersTable = """CREATE TABLE IF NOT EXISTS users(
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    userName TEXT(60) NOT NULL,
    permissionLevel INT(1) NOT NULL
    )"""

# Executing the command that creates the users table
cursor.execute(initUsersTable)

# Create clients table
initClientsTable = """CREATE TABLE IF NOT EXISTS clients(
    clientID INTEGER PRIMARY KEY AUTOINCREMENT,
    clientName TEXT(60) NOT NULL,
    contractStatus BOOLEAN NOT NULL,
    contractStartDate TEXT(10),
    contractEndDate TEXT(10),
    projectWork BOOLEAN NOT NULL,
    hqLongitude REAL(13),
    hqLatitude REAL(13),
    estimatedTotalRevenue REAL(13)
    )"""

# Executing the command that creates the clients table
cursor.execute(initClientsTable)


def is_table_populated(cursor, table_name):
    # SQL query to count the number of rows in the table
    query = f"SELECT COUNT(*) FROM {table_name}"
    
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



if is_table_populated(cursor, "users") and is_table_populated(cursor, "clients"):
    pass
else:
    # Add to users
    cursor.execute("INSERT INTO users VALUES (1, 'Isaac Patrickson', 9)")
    cursor.execute("INSERT INTO users (userName, permissionLevel) VALUES ('John Doe', 1)")
    
    # Add to clients
    cursor.execute("INSERT INTO clients VALUES (1, 'VetPartners', TRUE, '25-03-2024', '', TRUE, 53.98797, -1.10369, 650000.00)")
    cursor.execute("""INSERT INTO clients (clientName, contractStatus, contractStartDate, contractEndDate, projectWork, hqLongitude, hqLatitude, estimatedTotalRevenue) 
                VALUES ('SouthernWater', FALSE, '12-02-2023', '15-12-2023', TRUE, 50.82407, -0.42637, 750000.00)""")

cursor.execute("SELECT * FROM users")
results = cursor.fetchall()
print(results)
cursor.execute("SELECT * FROM clients")
results = cursor.fetchall()
print(results)






# Committing all changes to the database
conn.commit()

# Close connection
conn.close()
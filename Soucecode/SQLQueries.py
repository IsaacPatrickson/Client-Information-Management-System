def getTableWithPandas(pd, connection, table):
    neatTable = pd.read_sql_query(f"SELECT * FROM {table}", connection)
    return neatTable
    
def selectAttribute(cursor, selector, table, column, value):
    query = f"SELECT {selector} FROM {table} WHERE {column} = ?"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    return result

def selectAttributesWithPandas(pd, connection, selector, table, column, value):
    query = f"SELECT {selector} FROM {table} WHERE {column} = ?"
    results = pd.read_sql_query(query, connection, params=(value,))
    return results

def attributeNameMatchClientColumnName(cursor, attributeName):
    cursor.execute("""SELECT clientID, clientName, contractStatus, contractStartDate,
                contractEndDate, projectWork, hqLongitude, hqLatitude, estimatedTotalRevenue 
                FROM clients""")
    # Fetch the column names
    columnNames = [description[0] for description in cursor.description]
    for columnName in columnNames:
        if attributeName == columnName:
            return True
        else:
            pass
    return False

def checkIfInputInTable(cursor, selectedValuesInColumn, table, inputValue):
    query = f"SELECT {selectedValuesInColumn} FROM {table}"
    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        if str(inputValue) == str(result[0]):
            return True
        else:
            pass
    return False

def replaceAttribute(cursor, table, columnToUpdate, newValue, conditionColumn, conditionValue):
    query = f"""
    UPDATE {table} 
    SET {columnToUpdate} = ? 
    WHERE {conditionColumn} = ?
    """
    cursor.execute(query, (newValue, conditionValue))
    
def getColumnDataType(cursor, tableName, columnName):
    cursor.execute(f"PRAGMA table_info({tableName})")
    columnsInfo = cursor.fetchall()
        
    for column in columnsInfo:
        if column[1] == columnName:
            typeName = []
            for char in column[2]:
                if char == "(":
                    break
                else:
                    typeName.append(char)
            typeName = "".join(typeName)
            return typeName
        
    return None     
        
        
# def selectAllCases(cursor, selector, table, condition, value):
#     cursor.execute("SELECT ? FROM ? WHERE ? = ?", (selector, table, condition, value,))
#     result = cursor.fetchall()
#     return result
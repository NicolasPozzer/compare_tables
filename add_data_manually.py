import pyodbc as db

# I load new data into my new table

# Connection to Database
try:
    conn = db.connect(
        driver="SQL Server",
        server="DESKTOP-NICO",
        database="compare_data"
    )
    print("Succesful connection!")
except db.Error as ex:
    print("Error connecting: ",ex)

def insertData(table):
    result = f"""
    INSERT INTO {table} (ID,Name,Last_Name,Email,Phone) VALUES (11,'asdasiro','Parra','rami@gmail.com','7585368')
    INSERT INTO {table} (ID,Name,Last_Name,Email,Phone) VALUES (12,'asdaiel','Ruiz','dani@gmail.com','65735368')
    """
    return result

# I run the insert query and commit the transaction
try:
    cursor = conn.cursor()  # I use cursor to manage the connection

    # Execute the insert query
    cursor.execute(insertData("main_table"))
    conn.commit()  # Confirm the transaction

    print("Insertion completed successfully")

except db.Error as ex:
    print(f"Error executing query: {ex}")
finally:
    # Close the connection whether errors occur or not.
    if 'conn' in locals():
        conn.close()
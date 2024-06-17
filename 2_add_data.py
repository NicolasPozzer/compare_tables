import pyodbc as db

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


insert_data = """
INSERT INTO main_table (ID,Name,Last_Name,Email,Phone) VALUES (7,'Javier','Gomez','javo15@gmail.com','436354768')
INSERT INTO main_table (ID,Name,Last_Name,Email,Phone) VALUES (8,'Ivan','Trebuc','tertu-88@gmail.com','657374468')
INSERT INTO main_table (ID,Name,Last_Name,Email,Phone) VALUES (9,'Fernando','Villacorta','fer18@gmail.com','244235368')
"""



# I run the insert query and commit the transaction
try:
    cursor = conn.cursor()  # I use cursor to manage the connection

    # Execute the insert query
    cursor.execute(insert_data)

    conn.commit() # Confirm the transaction
    print("Insertion completed successfully")

except db.Error as ex:
    print(f"Error executing query: {ex}")
finally:
    # Close the connection whether errors occur or not.
    if 'conn' in locals():
        conn.close()
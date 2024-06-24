import pyodbc as db

#Creo 2 tablas copias de la tabla main -> mirror_tabla & backup_table

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

#Query: create mirror table
create_backup_table = """
SELECT *
INTO backup_table
FROM main_table;
"""

# I run the insert query and commit the transaction
try:
    cursor = conn.cursor()  # I use cursor to manage the connection

    cursor.execute(create_backup_table)
    conn.commit()
    print("Insertion completed successfully")

except db.Error as ex:
    print(f"Error executing query: {ex}")
finally:
    # Close the connection whether errors occur or not.
    if 'conn' in locals():
        conn.close()
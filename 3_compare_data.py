import pyodbc as db
import pandas as pd

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


select_mirror_table = "SELECT * FROM mirror_table"
select_main_table = "SELECT * FROM main_table"


# Function to check and add the column if it does not exist
def verify_and_add_column(conn, table_name, column_name, column_type):
    cursor = conn.cursor()
    check_column_query = f"""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{table_name}' AND COLUMN_NAME = '{column_name}'
    """
    cursor.execute(check_column_query)
    result = cursor.fetchone()

    if not result:
        add_column_query = f"""
        ALTER TABLE {table_name}
        ADD {column_name} {column_type}
        """
        cursor.execute(add_column_query)
        conn.commit()
        print(f"Column Add! '{column_name}' a '{table_name}'.")

# I run the insert query and commit the transaction
try:
    verify_and_add_column(conn, 'main_table', 'isNew_element', 'VARCHAR(50)')

    main_table = pd.read_sql(select_main_table, conn)
    mirror_table = pd.read_sql(select_mirror_table, conn)

    #Compare
    main_table['isNew_element'] = main_table['ID'].apply(
        lambda x: 'YES' if x not in mirror_table['ID'].values else ''
    )

    # Save Changes
    cursor = conn.cursor()
    # Update Table
    for index, row in main_table.iterrows():
        update_query = """
            UPDATE main_table
            SET isNew_element = ?
            WHERE id = ?
            """
        cursor.execute(update_query, row['isNew_element'], row['ID'])

    conn.commit()
    print("Compare and update successfully.")

except db.Error as ex:
    print(f"Error executing query: {ex}")
finally:
    # Close the connection whether errors occur or not.
    if 'conn' in locals():
        conn.close()
from datetime import datetime
import pyodbc as db
import pandas as pd
import warnings

# Connection to Database
try:
    conn = db.connect(
        driver="SQL Server",
        server="DESKTOP-NICO",
        database="compare_data"
    )
    print("Successful connection!")
except db.Error as ex:
    print("Error connecting: ", ex)

# Query: Execute stored procedure and fetch results
execute_stored_procedure = "EXEC [dbo].[getMain_table]"




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
        print(f"Column '{column_name}' added to '{table_name}'.")

# Function to check if a table exists
def table_exists(conn, table_name):
    cursor = conn.cursor()
    check_table_query = f"""
    SELECT 1 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME = '{table_name}'
    """
    cursor.execute(check_table_query)
    return cursor.fetchone() is not None

select_new_table = "SELECT * FROM new_table"
select_mirror_table = "SELECT * FROM mirror_table"

# Query to create mirror table if it does not exist
create_mirror_table = """
SELECT *
INTO mirror_table
FROM new_table;
"""

# Logical explanation: First I create a mirror table of new_table and then compare the new data from the table
# new_table with the old data from the backup table and then create a new column in the mirror table
# and assign with current date to new recently added items!

try:
    # Ignore warnings from SQLAlchemy
    warnings.filterwarnings('ignore', message='pandas only supports SQLAlchemy connectable')

    cursor = conn.cursor()
    if not table_exists(conn, 'new_table'):
        if not table_exists(conn, 'backup_table'):
            try:
                # Execute the stored procedure
                cursor.execute(execute_stored_procedure)
                results = cursor.fetchall()  # Fetch all results
                columns = [column[0] for column in cursor.description]  # Get column names

                # Crea la nueva tabla basandose en los resultados de la misma
                create_new_table = f"""
                CREATE TABLE new_table ({', '.join([f'{col} NVARCHAR(MAX)' for col in columns])});
                """
                cursor.execute(create_new_table)
                conn.commit()

                # Insert the fetched results into the new table
                for row in results:
                    insert_row = f"""
                    INSERT INTO new_table ({', '.join(columns)})
                    VALUES ({', '.join([f"'{str(val)}'" for val in row])});
                    """
                    cursor.execute(insert_row)
                conn.commit()
                print("Stored procedure executed and results stored in new_table successfully")

                # Create backup_table from new_table
                create_backup_table = """
                SELECT *
                INTO backup_table
                FROM new_table;
                """
                cursor.execute(create_backup_table)
                conn.commit()
                print("Backup table created successfully from new_table")

            except db.Error as ex:
                print(f"Error executing query: {ex}")

    if not table_exists(conn, 'mirror_table'):
        # Create the mirror table
        cursor.execute(create_mirror_table)
        conn.commit()
        print("Mirror table created successfully.")

    verify_and_add_column(conn, 'mirror_table', 'isNew_element', 'VARCHAR(50)')

    new_table = pd.read_sql(select_new_table, conn)
    mirror_table = pd.read_sql(select_mirror_table, conn)

    # Identify new rows
    new_rows = new_table[~new_table['ID'].isin(mirror_table['ID'])]

    if not new_rows.empty:
        # Insert new rows into mirror_table
        for index, row in new_rows.iterrows():
            insert_query = f"""
            INSERT INTO mirror_table ({', '.join(new_table.columns)}, isNew_element)
            VALUES ({', '.join(['?' for _ in new_table.columns])}, ?)
            """
            cursor.execute(insert_query, *row.tolist(), datetime.now())
        conn.commit()
        print("New rows inserted into mirror_table successfully.")

    # Update isNew_element for new rows in mirror_table
    for index, row in new_rows.iterrows():
        update_query = """
            UPDATE mirror_table
            SET isNew_element = ?
            WHERE ID = ?
            """
        cursor.execute(update_query, datetime.now(), row['ID'])

    conn.commit()
    print("Comparison and update completed successfully.")

except db.Error as ex:
    print(f"Error executing query: {ex}")
finally:
    # Close the connection whether errors occur or not.
    if 'conn' in locals():
        conn.close()

from datetime import datetime
import pyodbc as db
import pandas as pd
import warnings
from faker import Faker
from src.comp.necesary_functions import (table_exists,
verify_new_rows, verify_and_add_column, mask_data)

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

# Query: Execute stored procedure and fetch results⬇
execute_stored_procedure = "EXEC [dbo].[getMain_table]"

# Set Primary Key Ej. EMPLEID, id, ID, etc
primary_key = "ID"

# ⬆⬆⬆ Just modify the fields above ⬆⬆⬆



# Do not touch these fields ⬇⬇
select_new_table = "SELECT * FROM new_table"
select_mirror_table = "SELECT * FROM mirror_table"

# Query to create mirror table if it does not exist
create_mirror_table = """
SELECT *
INTO mirror_table
FROM new_table;
"""


# Función para enmascarar datos


fake = Faker()

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



                # Create the new table based on the results of the table
                create_new_table = f"""
                CREATE TABLE new_table ({', '.join([f'{col} NVARCHAR(MAX)' for col in columns])});
                """
                cursor.execute(create_new_table)
                conn.commit()

                # Insert the fetched results into the new table
                for row in results:
                    masked_row = mask_data(row, columns, fake, primary_key)
                    insert_row = f"""
                    INSERT INTO new_table ({', '.join(columns)})
                    VALUES ({', '.join([f"'{str(val)}'" for val in masked_row])});
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
    else:
        verify_new_rows(conn, execute_stored_procedure, fake, primary_key)

    if not table_exists(conn, 'mirror_table'):
        # Create the mirror table
        cursor.execute(create_mirror_table)
        conn.commit()
        print("Mirror table created successfully.")

    verify_and_add_column(conn, 'mirror_table', 'isNew_element', 'VARCHAR(50)')

    new_table = pd.read_sql(select_new_table, conn)
    mirror_table = pd.read_sql(select_mirror_table, conn)

    # Identify new rows
    new_rows = new_table[~new_table[primary_key].isin(mirror_table[primary_key])]

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
        update_query = f"""
            UPDATE mirror_table
            SET isNew_element = ?
            WHERE {primary_key} = ?
            """
        cursor.execute(update_query, datetime.now(), row[primary_key])

    conn.commit()
    print("Comparison and update completed successfully.")

except db.Error as ex:
    print(f"Error executing query: {ex}")
finally:
    # Drop temp_table if it exists
    if table_exists(conn, 'temp_table'):
        drop_temp_table_query = "DROP TABLE temp_table;"
        conn.execute(drop_temp_table_query)
        conn.commit()
        print("Temporary table 'temp_table' dropped successfully.")

    # Close the connection whether errors occur or not.
    if 'conn' in locals():
        conn.close()
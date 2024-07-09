import sys
import importlib
from datetime import datetime
import pyodbc as db
import pandas as pd
import warnings
from faker import Faker
from src.comp.necesary_functions import (
    table_exists, verify_new_rows, verify_and_add_column, mask_data
)

def load_config(config_file):
    config_name = config_file.replace('.py', '')
    config = importlib.import_module(config_name)
    return config

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("falta correr por comando con el archivo de la configuracion")
        sys.exit(1)

    config_file = sys.argv[1]
    config = load_config(config_file)

    primary_key = config.primary_key
    dont_mask = config.dont_mask
    column_fakes = config.column_fakes
    execute_stored_procedure = config.execute_stored_procedure
    mirror_table = config.name_output_table

    fake = Faker()

    # Do not touch these fields ⬇⬇
    # Connection to Database
    try:
        conn = config.conn
        conn2 = config.conn2
        print("Successful connection!")
    except db.Error as ex:
        print("Error connecting: ", ex)

    select_temp_table = "SELECT * FROM temp_table"
    select_mirror_table = f"SELECT * FROM {mirror_table}"

    cache = {}

    try:
        # Ignore warnings from SQLAlchemy
        warnings.filterwarnings('ignore', message='pandas only supports SQLAlchemy connectable')

        cursor = conn.cursor()
        cursor2 = conn2.cursor()
        if not table_exists(conn2, mirror_table):
            try:
                # Execute the stored procedure
                cursor.execute(execute_stored_procedure)
                results = cursor.fetchall()  # Fetch all results
                columns = [column[0] for column in cursor.description]  # Get column names

                # Create the new table based on the results of the table
                create_mirror_table = f"""
                CREATE TABLE {mirror_table} ({', '.join([f'{col} NVARCHAR(MAX)' for col in columns])});
                """
                cursor2.execute(create_mirror_table)
                conn2.commit()

                # Insert the fetched results into the new table
                for row in results:
                    masked_row = mask_data(row, columns, fake, primary_key, cache, dont_mask, column_fakes)
                    insert_row = f"""
                    INSERT INTO {mirror_table} ({', '.join(columns)})
                    VALUES ({', '.join([f"'{str(val)}'" for val in masked_row])});
                    """
                    cursor2.execute(insert_row)

                conn2.commit()
                print(f"Stored procedure zexecuted and results stored in {mirror_table} successfully")
            except db.Error as ex:
                print(f"Error executing query: {ex}")
        else:
            verify_and_add_column(conn2, mirror_table, 'isNew_element', 'VARCHAR(50)')
            verify_new_rows(conn, conn2, mirror_table, execute_stored_procedure, fake, primary_key, cache, dont_mask, column_fakes)

    except db.Error as ex:
        print(f"Error executing query: {ex}")
    finally:
        # Drop temp_table if it exists
        if table_exists(conn2, 'temp_table'):
            drop_temp_table_query = "DROP TABLE temp_table;"
            conn2.execute(drop_temp_table_query)
            conn2.commit()
            print("Temporary table 'temp_table' dropped successfully.")

        # Close the connection whether errors occur or not.
        if 'conn' in locals():
            conn.close()
        if 'conn2' in locals():
            conn2.close()

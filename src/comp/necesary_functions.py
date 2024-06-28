
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

def verify_new_rows(conn, execute_stored_procedure,fake,primary_key):
    try:
        cursor = conn.cursor()

        # Execute the stored procedure and create temp_table
        cursor.execute(execute_stored_procedure)
        results = cursor.fetchall()  # Fetch all results
        columns = [column[0] for column in cursor.description]  # Get column names

        # Create temp_table based on stored procedure results
        create_temp_table = f"""
        CREATE TABLE temp_table ({', '.join([f'{col} NVARCHAR(MAX)' for col in columns])});
        """
        cursor.execute(create_temp_table)
        conn.commit()

        # Insert fetched results into temp_table
        for row in results:
            masked_row = mask_data(row, columns, fake)
            insert_row = f"""
            INSERT INTO temp_table ({', '.join(columns)})
            VALUES ({', '.join([f"'{str(val)}'" for val in masked_row])});
            """
            cursor.execute(insert_row)
        conn.commit()
        print("Temporary table 'temp_table' created and populated successfully.")

        # Insert new rows from temp_table into new_table if they don't already exist
        insert_new_rows_query = f"""
        INSERT INTO new_table ({', '.join(columns)})
        SELECT {', '.join(columns)}
        FROM temp_table
        WHERE NOT EXISTS (
            SELECT 1 FROM new_table WHERE new_table.{primary_key} = temp_table.{primary_key}
        );
        """
        cursor.execute(insert_new_rows_query)
        conn.commit()
        print("searching new rows...")

    except Exception as ex:
        print(f"Error executing query: {ex}")

#Data masking
def mask_data(row, columns, fake, primary_key):
    masked_row = []
    for col, val in zip(columns, row):
        if col == primary_key:
            masked_row.append(val)
        else:
            # Generar la data falsa dependiendo del tipo de dato
            if isinstance(val, int):
                masked_row.append(fake.random_number(digits=len(str(val))))
            elif isinstance(val, float):
                masked_row.append(fake.random_number(digits=len(str(val).replace('.', '')))/100)
            elif isinstance(val, str):
                masked_row.append(fake.word())
            else:
                masked_row.append(val)
    return masked_row
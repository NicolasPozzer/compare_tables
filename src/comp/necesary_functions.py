
# Function to check and add the column if it does not exist
def verify_and_add_column(conn2, table_name, column_name, column_type):
    cursor2 = conn2.cursor()
    check_column_query = f"""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{table_name}' AND COLUMN_NAME = '{column_name}'
    """
    cursor2.execute(check_column_query)
    result = cursor2.fetchone()

    if not result:
        add_column_query = f"""
        ALTER TABLE {table_name}
        ADD {column_name} {column_type} 
        """
        cursor2.execute(add_column_query)
        conn2.commit()
        print(f"Column '{column_name}' added to '{table_name}'.")

# Function to check if a table exists
def table_exists(conn2, table_name):
    cursor2 = conn2.cursor()
    check_table_query = f"""
    SELECT 1 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME = '{table_name}'
    """
    cursor2.execute(check_table_query)
    return cursor2.fetchone() is not None

def verify_new_rows(conn, conn2, mirror_table, execute_stored_procedure, fake, primary_key, cache, dont_mask, column_fakes):
    try:
        cursor = conn.cursor()
        cursor2 = conn2.cursor()

        # Execute the stored procedure and create temp_table
        cursor.execute(execute_stored_procedure)
        results = cursor.fetchall()  # Fetch all results
        columns = [column[0] for column in cursor.description]  # Get column names

        # Create temp_table based on stored procedure results
        create_temp_table = f"""
        CREATE TABLE temp_table ({', '.join([f'{col} NVARCHAR(MAX)' for col in columns])}, isNew_element DATETIME);
        """
        cursor2.execute(create_temp_table)
        conn2.commit()

        # Insert fetched results into temp_table
        for row in results:
            masked_row = mask_data(row, columns, fake, primary_key, cache, dont_mask, column_fakes)
            insert_row = f"""
            INSERT INTO temp_table ({', '.join(columns)}, isNew_element)
            VALUES ({', '.join([f"'{str(val)}'" for val in masked_row])}, NULL);
            """
            cursor2.execute(insert_row)
        conn2.commit()
        print("Temporary table 'temp_table' created and populated successfully.")

        # Insert new rows from temp_table into mirror_table if they don't already exist
        insert_new_rows_query = f"""
        INSERT INTO {mirror_table} ({', '.join(columns)}, isNew_element)
        SELECT {', '.join(columns)}, GETDATE()
        FROM temp_table
        WHERE NOT EXISTS (
            SELECT 1 FROM {mirror_table} WHERE {mirror_table}.{primary_key} = temp_table.{primary_key}
        );
        """
        cursor2.execute(insert_new_rows_query)
        conn2.commit()
        print(f"New rows inserted into {mirror_table} successfully.")

    except Exception as ex:
        print(f"Error executing query: {ex}")


from faker import Faker

# Data masking
def mask_data(row, columns, fake, primary_key, cache, dont_mask, column_fakes):
    masked_row = []

    # Obtener el valor de la clave primaria de la fila
    pk_value = row[columns.index(primary_key)]

    if pk_value in cache:
        masked_row = cache[pk_value]
    else:
        for col, val in zip(columns, row):
            if col in dont_mask:
                masked_row.append(val)
            else:
                # Generar la data falsa dependiendo del tipo de dato
                if isinstance(val, int):
                    column_mask = next((cf for cf in column_fakes if cf.name == col), None)
                    if column_mask:
                        fake_expression = f'fake.{column_mask.type_mask}'
                        fake_value = eval(fake_expression)
                        masked_row.append(fake_value)
                    else:
                        masked_row.append(fake.random_number(digits=len(str(val))))
                elif isinstance(val, float):
                    column_mask = next((cf for cf in column_fakes if cf.name == col), None)
                    if column_mask:
                        fake_expression = f'fake.{column_mask.type_mask}'
                        fake_value = eval(fake_expression)
                        masked_row.append(fake_value)
                    else:
                        masked_row.append(fake.random_number(digits=len(str(val).replace('.', '')))/100)
                elif isinstance(val, str):
                    column_mask = next((cf for cf in column_fakes if cf.name == col), None)
                    if column_mask:
                        fake_expression = f'fake.{column_mask.type_mask}'
                        fake_value = eval(fake_expression)
                        masked_row.append(fake_value)
                    else:
                        masked_row.append(fake.word())
                else:
                    masked_row.append(val)
        # Almacenar la fila con datos falsos en el cache
        cache[pk_value] = masked_row

    return masked_row

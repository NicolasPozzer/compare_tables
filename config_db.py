import pyodbc as db
from src.comp.ColumnMask import ColumnMask

# Origin Database
conn = db.connect(
        driver="SQL Server",
        server="DESKTOP-NICO",
        database="compare_data",
        username="",
        password=""
    )

# Destination Database
conn2 = db.connect(
        driver="SQL Server",
        server="DESKTOP-NICO",
        database="crud_sql_server",
        username="",
        password=""
    )

# Query: Execute stored procedure and fetch results⬇
execute_stored_procedure = "EXEC [dbo].[getMain_table]"

name_output_table = "test_table"

# Set Primary Key Ej. EMPLEID, id, ID, etc
primary_key = "EMPLID"

# Set Dont mask columns (Ej. ["FIRST_NAME","LAST_NAME"])
dont_mask = [primary_key, "FIRST_NAME"]

# Implement column field name and fake to use for it
column1 = ColumnMask("LAST_NAME", "last_name()")
column2 = ColumnMask("LVL", "random_int()")
column3 = ColumnMask("ORDR", "ssn()")

# List of Objects to Mask
column_fakes = [column1, column2, column3]

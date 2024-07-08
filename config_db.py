import pyodbc as db


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
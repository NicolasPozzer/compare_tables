# Compare Data from stored procedure


## Dependencies

To run the script, install the dependencies.

```bash
  pip install pandas pyodbc
```

## Instructions

- Run the main.py script (This will create the first necessary tables).

- Once executed for the first time, enter or change parameters of the stored procedure for new data, so that the script logic automatically takes care of adding them to the mirror_table, establishing its current date.

#### mirror_table result:
![plot](https://i.imgur.com/WQJfNaU.jpeg)

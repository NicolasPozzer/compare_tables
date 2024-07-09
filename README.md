# Compare Data from stored procedure


## Dependencies

To run the script, install the dependencies.

```bash
  pip install pandas pyodbc Faker
```

## Instructions

- Configure the "config_db.py" script to map the origin and destination databases. Then assign columns to be masked with the masking method.

- Run the following command with the desired configuration file to run the project:
```bash
  py.exe main.py config_db.py
```

#### mirror_table result:
![plot](https://i.imgur.com/WQJfNaU.jpeg)

## Faker Methods
![plot](https://i.imgur.com/We9pwAX.png)
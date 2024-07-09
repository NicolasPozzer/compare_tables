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
```bash
# General Faker methods
fake.name()                   # Generates a full name
fake.first_name()             # Generates a first name
fake.last_name()              # Generates a last name
fake.address()                # Generates a full address
fake.street_address()         # Generates a street address
fake.city()                   # Generates a city name
fake.state()                  # Generates a state name
fake.country()                # Generates a country name
fake.zipcode()                # Generates a postal code
fake.email()                  # Generates an email address
fake.phone_number()           # Generates a phone number
fake.date_of_birth()          # Generates a date of birth
fake.company()                # Generates a company name
fake.job()                    # Generates a job title
fake.catch_phrase()           # Generates a catch phrase
fake.bs()                     # Generates a business term
fake.ssn()                    # Generates a social security number (SSN)

# Financial methods
fake.credit_card_number()     # Generates a credit card number
fake.credit_card_provider()   # Generates a credit card provider
fake.credit_card_expire()     # Generates a credit card expiration date
fake.iban()                   # Generates an IBAN number
fake.bban()                   # Generates a BBAN number

# Location related methods
fake.latitude()               # Generates a latitude
fake.longitude()              # Generates a longitude
fake.coordinate()             # Generates a coordinate (latitude and longitude)
fake.local_latlng()           # Generates a local coordinate

# Web related methods
fake.domain_name()            # Generates a domain name
fake.url()                    # Generates a URL
fake.user_name()              # Generates a username
fake.password()               # Generates a password
fake.ipv4()                   # Generates an IPv4 address
fake.ipv6()                   # Generates an IPv6 address
fake.mac_address()            # Generates a MAC address

# Text related methods
fake.word()                   # Generates a random word
fake.sentence()               # Generates a sentence
fake.paragraph()              # Generates a paragraph
fake.text()                   # Generates a text

# Random number and data methods
fake.random_int()             # Generates a random integer
fake.random_number()          # Generates a random number
fake.random_digit()           # Generates a random digit
fake.random_element(['A', 'B', 'C'])  # Generates a random element from a list

# Custom location-specific methods
fake.city_prefix()            # Generates a city prefix
fake.city_suffix()            # Generates a city suffix
fake.street_suffix()          # Generates a street suffix
fake.state_abbr()             # Generates a state abbreviation
fake.country_code()           # Generates a country code
fake.postcode()               # Generates a postal code

# Date and time related methods
fake.date()                   # Generates a date
fake.time()                   # Generates a time
fake.date_time()              # Generates a date and time
fake.date_time_this_year()    # Generates a date and time this year
fake.date_time_this_month()   # Generates a date and time this month
fake.date_time_between('-30y', 'now')  # Generates a date and time within a specific time range

# Color related methods
fake.color_name()             # Generates a color name
fake.hex_color()              # Generates a hex color
fake.rgb_color()              # Generates an RGB color
fake.safe_color_name()        # Generates a safe color name

# Technology related methods
fake.file_name()              # Generates a file name
fake.mime_type()              # Generates a MIME type
fake.ascii_free_email()       # Generates an ASCII email address
fake.ascii_company_email()    # Generates an ASCII company email address

# Cryptocurrency related methods
fake.cryptocurrency()         # Generates a cryptocurrency
fake.cryptocurrency_code()    # Generates a cryptocurrency code

# Other useful methods
fake.uuid4()                  # Generates a UUID version 4
fake.safe_email()             # Generates a safe email address
fake.sha256()                 # Generates a SHA-256 hash
fake.image_url()              # Generates an image URL
fake.locale()                 # Generates a locale code
fake.currency_code()          # Generates a currency code
fake.currency_name()          # Generates a currency name
fake.timezone()               # Generates a timezone name

# Advanced usage examples
fake.profile()                # Generates a complete profile (includes name, address, job, etc.)
fake.simple_profile()         # Generates a simple profile (includes name, address, etc.)
```
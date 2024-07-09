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
print(fake.name())                   # Generates a full name
print(fake.first_name())             # Generates a first name
print(fake.last_name())              # Generates a last name
print(fake.address())                # Generates a full address
print(fake.street_address())         # Generates a street address
print(fake.city())                   # Generates a city name
print(fake.state())                  # Generates a state name
print(fake.country())                # Generates a country name
print(fake.zipcode())                # Generates a postal code
print(fake.email())                  # Generates an email address
print(fake.phone_number())           # Generates a phone number
print(fake.date_of_birth())          # Generates a date of birth
print(fake.company())                # Generates a company name
print(fake.job())                    # Generates a job title
print(fake.catch_phrase())           # Generates a catch phrase
print(fake.bs())                     # Generates a business term
print(fake.ssn())                    # Generates a social security number (SSN)

# Financial methods
print(fake.credit_card_number())     # Generates a credit card number
print(fake.credit_card_provider())   # Generates a credit card provider
print(fake.credit_card_expire())     # Generates a credit card expiration date
print(fake.iban())                   # Generates an IBAN number
print(fake.bban())                   # Generates a BBAN number

# Location related methods
print(fake.latitude())               # Generates a latitude
print(fake.longitude())              # Generates a longitude
print(fake.coordinate())             # Generates a coordinate (latitude and longitude)
print(fake.local_latlng())           # Generates a local coordinate

# Web related methods
print(fake.domain_name())            # Generates a domain name
print(fake.url())                    # Generates a URL
print(fake.user_name())              # Generates a username
print(fake.password())               # Generates a password
print(fake.ipv4())                   # Generates an IPv4 address
print(fake.ipv6())                   # Generates an IPv6 address
print(fake.mac_address())            # Generates a MAC address

# Text related methods
print(fake.word())                   # Generates a random word
print(fake.sentence())               # Generates a sentence
print(fake.paragraph())              # Generates a paragraph
print(fake.text())                   # Generates a text

# Random number and data methods
print(fake.random_int())             # Generates a random integer
print(fake.random_number())          # Generates a random number
print(fake.random_digit())           # Generates a random digit
print(fake.random_element(['A', 'B', 'C']))  # Generates a random element from a list

# Custom location-specific methods
print(fake.city_prefix())            # Generates a city prefix
print(fake.city_suffix())            # Generates a city suffix
print(fake.street_suffix())          # Generates a street suffix
print(fake.state_abbr())             # Generates a state abbreviation
print(fake.country_code())           # Generates a country code
print(fake.postcode())               # Generates a postal code

# Date and time related methods
print(fake.date())                   # Generates a date
print(fake.time())                   # Generates a time
print(fake.date_time())              # Generates a date and time
print(fake.date_time_this_year())    # Generates a date and time this year
print(fake.date_time_this_month())   # Generates a date and time this month
print(fake.date_time_between('-30y', 'now'))  # Generates a date and time within a specific time range

# Color related methods
print(fake.color_name())             # Generates a color name
print(fake.hex_color())              # Generates a hex color
print(fake.rgb_color())              # Generates an RGB color
print(fake.safe_color_name())        # Generates a safe color name

# Technology related methods
print(fake.file_name())              # Generates a file name
print(fake.mime_type())              # Generates a MIME type
print(fake.ascii_free_email())       # Generates an ASCII email address
print(fake.ascii_company_email())    # Generates an ASCII company email address

# Cryptocurrency related methods
print(fake.cryptocurrency())         # Generates a cryptocurrency
print(fake.cryptocurrency_code())    # Generates a cryptocurrency code

# Other useful methods
print(fake.uuid4())                  # Generates a UUID version 4
print(fake.safe_email())             # Generates a safe email address
print(fake.sha256())                 # Generates a SHA-256 hash
print(fake.image_url())              # Generates an image URL
print(fake.locale())                 # Generates a locale code
print(fake.currency_code())          # Generates a currency code
print(fake.currency_name())          # Generates a currency name
print(fake.timezone())               # Generates a timezone name

# Advanced usage examples
print(fake.profile())                # Generates a complete profile (includes name, address, job, etc.)
print(fake.simple_profile())         # Generates a simple profile (includes name, address, etc.)
```
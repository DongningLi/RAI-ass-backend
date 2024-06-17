# Project Name

Data Process and Display: creating a web application that processes and displays data from a CSV file

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Receive file
- Save file locally
- Data Process
- Save data to MongoDB
- Download file

## Technologies Used

- Django
- Python
- REST API
- MongoDB

## Requirements

- Reuqest sent from http://localhost:3000

## Installation

```bash
# Clone the repository
$ git clone
# Go to the root directory
$ cd myproject
# Install dependencies
$ npm install
# Create migration files
$ python manage.py makemigrations
# Apply the migrations to the database
$ python manage.py migrate

# Start the application
$ python manage.py runserver
```

## Application Port

Defautly, port is 8000. To modify the application's port, specify `portNumber` in cmd when running.

```bash
# Example
$ python manage.py runserver <portNumber>
```

## Database Configuration

In the `myproject/db_connection.py` file, set up the **MongoDB** connection, and database name.

```typescript
url = "mongodb://localhost:27017";
client = pymongo.MongoClient(url);

db = client["raidb1"];
```

## Directory Structure

```bash
/RAI-ASS-BACKEND
|-- /myproject
|   |-- /core            # Core functionalities for type detect and infer
|   |-- /myapp           # App functionalities including API generation
|   |-- /myprject        # Project settings
|   |-- /public          # Default file downloading location
|   |-- /db_connection   # Database connection information
|   |-- /manage.py       # Django's command-line utility for administrative tasks.
|-- .gitignore           # Files to ignore
|-- README.md            # Project overview and guidelines
```

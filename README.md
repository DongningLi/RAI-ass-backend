# Project Name

Data Process and Display: creating a web application that processes and displays data from a CSV file.

Please refer to the frontend repository https://github.com/DongningLi/RAI-ass-frontend

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Requirements](#Requirements)
- [Installation](#installation)
- [Directory Structure](#Directory-structure)

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
- Docker image of front-end has been built
- Server could be deployed at http://0.0.0.0:8000/

## Installation

```bash
# Clone the repository
$ git clone
# Go to the root directory
$ cd myproject
# Build docker image
$ docker build -t raiassbackend .
# Run docker
$ docker-compose up -d
```

## Directory Structure

```bash
/RAI-ASS-BACKEND
|-- /myproject
|   |-- /core               # Core functionalities for type detect and infer
|   |-- /myapp              # App functionalities including API generation
|   |-- /myprject           # Project settings
|   |-- /public             # Default file downloading location
|   |-- db_connection.py    # Database connection information
|   |-- manage.py           # Django's command-line utility for administrative tasks
|   |-- Dockerfile          # Dockerfile
|-- .gitignore              # Files to ignore
|-- README.md               # Project overview and guidelines
```

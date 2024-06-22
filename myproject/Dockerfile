# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12.3

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /myapp
COPY . /myapp

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

CMD [ "python", "manage.py","runserver","0.0.0.0:8000" ]


import datetime
from mongoengine import Document, fields
from db_connection import db

FileContentCollection = db["file_content"]
ColsTypeCollection = db["cols_types"]
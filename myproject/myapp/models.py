import json
from bson import ObjectId
from db_connection import db
from djongo import models

FileContentCollection = db["file_content"]
ColsTypeCollection = db["cols_types"]

def update_types_in_mongodb(data_json):

    # Extract _id from the data
    _id = data_json.get('_id')
    if not _id:
        raise ValueError("Missing '_id' in the data")

    # Prepare the update fields, excluding _id
    update_fields = {key: value for key, value in data_json.items() if key != '_id'}

    ColsTypeCollection.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})




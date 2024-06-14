import json
from bson import ObjectId
from db_connection import db

FileContentCollection = db["file_content"]
ColsTypeCollection = db["cols_types"]

def update_document_in_mongodb(data_json):

    # Extract _id from the data
    _id = data_json.get('_id')
    if not _id:
        raise ValueError("Missing '_id' in the data")

    # Prepare the update fields, excluding _id
    update_fields = {key: value for key, value in data_json.items() if key != '_id'}

    # Perform the update
    result = ColsTypeCollection.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})


def update_field_types(file_id, colsTypes):

    # Retrieve documents with the given file ID
    documents = FileContentCollection.find({"file_id": file_id})

    for doc in documents:
        updated_doc = {}
        for field, value in doc.items():
            if field in colsTypes:
                target_type = colsTypes[field]
                try:
                    updated_doc[field] = target_type(value)
                except (ValueError, TypeError):
                    updated_doc[field] = value  # Keep the original value if conversion fails
            else:
                updated_doc[field] = value  # Keep the original value if no conversion needed

        # Update the document in MongoDB
        FileContentCollection.update_many({"_id": doc["_id"]}, {"$set": updated_doc})

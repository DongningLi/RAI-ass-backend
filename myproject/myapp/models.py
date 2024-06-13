import datetime
from mongoengine import Document, fields
from db_connection import db

FileContentCollection = db["file_content"]

class ColsTypes(Document):
    name = fields.StringField(max_length=255)
    birthdate = fields.StringField(max_length=255)
    score = fields.StringField(max_length=255)
    grade = fields.StringField(max_length=255)
    
class FileContent(Document):
    createTime = fields.DateTimeField(required=True,auto_now_add=True)

def create_dynamic_model(model_name, col_fields):
    
    # Define the attributes dictionary for the dynamic model class
    attrs = {'__module__': __name__}
    
    # Map field types to Django model fields
    field_type_mapping = {
        'object': fields.StringField(max_length=100),
        'int8': fields.IntField(),
        'int16': fields.IntField(),
        'int32': fields.IntField(),
        'int64': fields.IntField(),
        'float32': fields.FloatField(),
        'float64': fields.FloatField(),
        'complex':fields.ComplexBaseField(),
        'timedelta[ns]':fields.DateTimeField(),
        'datetime64': fields.DateField(),
        'datetime64[ns]': fields.DateField(),
        'bool':fields.BooleanField(),
        'category':fields.StringField()
    }
    
    # Add the fields to the attrs dictionary
    for col_name, col_type in col_fields.items():
        print("1.1:",col_type )
        if col_type not in field_type_mapping:
            raise ValueError(f'Unsupported field type: {col_type}')
        attrs[col_name] = field_type_mapping[col_type]
    
    print("1.2:", attrs)

    # Create the model class
    model_class = type(model_name, (Document,), attrs)
    print("1.3:",model_class)
    
    return model_class
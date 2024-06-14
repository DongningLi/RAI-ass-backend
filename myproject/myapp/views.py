import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import uuid
import json
from core.infer_data_types import detect_type, infer_type
import math

from .models import ColsTypeCollection, FileContentCollection, update_document_in_mongodb

def handle_uploaded_file(file_obj, file_id):
    filename = f"public/uploadedFile_{file_id}.csv"
    try:
        with open(filename, "wb+") as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        return (True, filename)
    except Exception as e:
        return (False, e)


def clean_data(data):
    if isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return None  # or another placeholder value
        return data
    elif isinstance(data, dict):
        return {k: clean_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    return data

class FileUploadView(APIView):

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']

        

        try:
            file_id = uuid.uuid4()
            success,file_save_result = handle_uploaded_file(file_obj, file_id)

            if success:
                df_sample = pd.read_csv(file_save_result, nrows=1000)

                try:
                    column_types = detect_type(df_sample)
                except Exception as e_detect_type:
                     return Response({'error': str(e_detect_type)}, status=status.HTTP_400_BAD_REQUEST)

                df = pd.read_csv(file_save_result)

                try:
                    df_con = infer_type(df,column_types)
                except Exception as e_infer_type:
                     return Response({'error': str(e_infer_type)}, status=status.HTTP_400_BAD_REQUEST)

                df_con['fileId'] = str(file_id)
                data_content_dict = df_con.to_dict(orient='records')
                data_content = clean_data(data_content_dict)
                column_types['fileId'] = str(file_id)

                try:
                    FileContentCollection.insert_many(data_content) 
                    ColsTypeCollection.insert_one(column_types)
                except Exception as e_insert_to_mongo:
                    return Response({'error': str(e_insert_to_mongo)}, status=status.HTTP_400_BAD_REQUEST)
                    
                # convert objectId to str for json response
                for record in data_content:
                    if '_id' in record:
                        record['_id'] = str(record['_id'])

                column_types['_id'] = str(column_types['_id'])

                data = {"contents":data_content,
                        "types":column_types}
        
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': str(file_save_result)}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class saveColsTypesView(APIView):

    def post(self, request, *args, **kwargs):

        data = request.data['data']
        data_json = json.loads(data)

        try:
            update_document_in_mongodb(data_json)

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
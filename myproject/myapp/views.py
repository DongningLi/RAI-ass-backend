import csv
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import uuid
import json
from core.infer_data_types import detect_type, infer_type

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

                contents = []
                chunk_iterator = pd.read_csv(file_save_result, chunksize=1000)
                for chunk in chunk_iterator:

                    try:
                        df_con = infer_type(chunk,column_types)
                    except Exception as e_infer_type:
                        return Response({'error': str(e_infer_type)}, status=status.HTTP_400_BAD_REQUEST)
                    
                    try:
                        df_con['fileId'] = str(file_id)
                        data_content = df_con.replace({np.nan:None}).to_dict(orient='records')
                        column_types['fileId'] = str(file_id)
                    except Exception as e_add_fileId:
                        return Response({'error': str(e_add_fileId)}, status=status.HTTP_400_BAD_REQUEST)
                    
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
                    
                    contents = np.concatenate((contents,data_content))

                data = {"contents":contents,
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
    

class generateNewFileView(APIView):

    def post(self, request, fileId, *args, **kwargs):
        try:
            print(fileId)
            
            records = list(FileContentCollection.find({'fileId': fileId}))
            
            if not records:
                    return JsonResponse({'error': 'No records found for the provided fileId'}, status=404)

            # Create a HttpResponse object and set the appropriate CSV headers
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)

            # Write the headers (keys of the first record)
            if records:
                header = [key for key in records[0].keys() if key != "_id" and key != "fileId"]
                writer.writerow(header)

                # Write data rows
                for record in records:
                    values = [value for key, value in record.items() if key != "_id" and key != "fileId"]
                    writer.writerow(values)

            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
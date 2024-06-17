import csv
import json
import uuid
import numpy as np
import pandas as pd
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse


from core.infer_data_types import detect_type, infer_type
from .models import ColsTypeCollection, FileContentCollection, update_types_in_mongodb

# generate file with an unique name under 'public' folder
def handle_uploaded_file(file_obj, file_id):
    filename = f"public/uploadedFile_{file_id}.csv"
    try:
        with open(filename, "wb+") as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        return (True, filename)
    except Exception as e:
        return (False, e)

# handle uploaded file
class FileUploadView(APIView):

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']

        try:
            file_id = uuid.uuid4()
            success,file_save_result = handle_uploaded_file(file_obj, file_id)

            # read chunk of file as sample
            if success:
                df_sample = pd.read_csv(file_save_result, nrows=1000)

                try:
                    # detect types of sample df
                    column_types = detect_type(df_sample)
                except Exception as e_detect_type:
                     return Response({'error': str(e_detect_type)}, status=status.HTTP_400_BAD_REQUEST)

                # read file in chunks
                contents = []
                chunk_iterator = pd.read_csv(file_save_result, chunksize=1000)
                for chunk in chunk_iterator:

                    try:
                        df_con = infer_type(chunk,column_types)
                    except Exception as e_infer_type:
                        return Response({'error': str(e_infer_type)}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # add fileid to records
                    try:
                        df_con['fileId'] = str(file_id)
                        data_content = df_con.replace({np.nan:None}).to_dict(orient='records')
                        column_types['fileId'] = str(file_id)
                    except Exception as e_add_fileId:
                        return Response({'error': str(e_add_fileId)}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # insert into mongodb 
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

                # form data and pass to api
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

        # attempt to update type
        try:
            update_types_in_mongodb(data_json)

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class generateNewFileView(APIView):

    def post(self, request, fileId, *args, **kwargs):
        try:
            
            # get records from mongoDB given by file ID
            records = list(FileContentCollection.find({'fileId': fileId}))
            
            if not records:
                    return JsonResponse({'error': 'No records found for the provided fileId'}, status=404)

            # create a HttpResponse object and set the appropriate csv headers
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)

            # write the headers (keys of the first record)
            if records:
                header = [key for key in records[0].keys() if key != "_id" and key != "fileId"]
                writer.writerow(header)

                # write data rows
                for record in records:
                    values = [value for key, value in record.items() if key != "_id" and key != "fileId"]
                    writer.writerow(values)

            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
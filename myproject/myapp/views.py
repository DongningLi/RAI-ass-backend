import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import uuid
import json
from core.infer_data_types import detect_type, infer_type


from .models import ColsTypeCollection, FileContentCollection



class FileUploadView(APIView):

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']

        try:
            df = pd.read_csv(file_obj)
            column_types = detect_type(df)
            file_id = uuid.uuid4()
            df['fileId'] = str(file_id)
            data_content = df.to_dict(orient='records')
            column_types['fileId'] = str(file_id)
            FileContentCollection.insert_many(data_content)
            ColsTypeCollection.insert_one(column_types)
            
            # convert objectId to str for json response
            for record in data_content:
                if '_id' in record:
                    record['_id'] = str(record['_id'])
            column_types['_id'] = str(column_types['_id'])

            data = {"contents":data_content,
                    "types":column_types}
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class saveColsTypesView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data['data']
        data_json = json.loads(data)
        name_type = data_json['Name']

        try:
            print(name_type)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
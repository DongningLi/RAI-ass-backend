import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

from core.infer_data_types import detect_type, infer_type
from .models import ColsTypes, FileContent


def save_type_instance(column_types):

    cols_types = ColsTypes (
        name = column_types["Name"],
        birthdate = column_types["Birthdate"],
        score = column_types["Score"],
        grade = column_types["Grade"]
    )

    cols_types.save()

def save_content_instance(df):

    for _, row in df.iterrows():

        content = FileContent(
            name = row["Name"],
            birthdate = row["Birthdate"],
            score = row["Score"],
            grade = row["Grade"],
        )

        content.save()

        
class FileUploadView(APIView):

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']

        try:
            df = pd.read_csv(file_obj)

            data_content = df.to_dict(orient='records')
            column_types = detect_type(df)
            df = infer_type(df,column_types)

            save_type_instance(column_types)
            save_content_instance(df)

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
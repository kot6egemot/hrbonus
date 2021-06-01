import csv
import io
import os
import zipfile

import requests
from django.http import FileResponse, HttpResponse, JsonResponse
from idna import unicode
from rest_framework.views import APIView
from base.models import CSVExportView_Basic, Constant
from base.serializers.bonus_serializer import ConstantsSerializer
from base.serializers.csv_serializer import CSVExportView_BasicSerializer
from base.views.utils import get_month_year
import urllib.parse
from django.http import StreamingHttpResponse


# def getfiles(file):
#     url = 'https://www.imgonline.com.ua/examples/bee-on-daisy.jpg'
#     response = requests.get(url)
#     # Get filename from url
#     filename = os.path.split(url)[1]
#     # Create zip
#     buffer = io.BytesIO()
#     zip_file = zipfile.ZipFile(buffer, 'w')
#     print(filename)
#     f = open('sample.csv', 'r')
#     zip_file.write('sample.csv')
#     f.close()
#     zip_file.close()
#     # Return zip
#     response = HttpResponse(buffer.getvalue())
#     response['Content-Type'] = 'application/x-zip-compressed'
#     response['Content-Disposition'] = 'attachment; filename=album.zip'
#     return response

class DownloadCSVView(APIView):
    serializer_class = CSVExportView_BasicSerializer

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        Year = request.GET['Year']
        Month = request.GET['Month']
        serializer = self.get_serializer(
            CSVExportView_Basic.objects.filter(Month=Month, Year=Year).all(),
            many=True
        )
        headers = [field['name'] for field in CSVExportView_Basic.get_model_fields() if field['name'] not in ['ID', 'Year', 'Month']]

        with open("sample.csv", "w", encoding='utf-8-sig') as csv_file:
            w = csv.DictWriter(csv_file, headers, delimiter=";")
            w.writeheader()
            for stats in serializer.data:
                w.writerow(stats)

        csv_file = open('sample.csv', 'rb')
        response = FileResponse(csv_file)
        return response

    def delete(self, request, *args, **kwargs):
        os.remove('sample.csv')
        return JsonResponse({'result': True})
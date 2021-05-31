import csv
import io
from django.http import  FileResponse
from rest_framework.views import APIView
from base.models import CSVExportView_Basic, Constant
from base.serializers.bonus_serializer import ConstantsSerializer
from base.serializers.csv_serializer import CSVExportView_BasicSerializer
from base.views.utils import get_month_year


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
        output = io.StringIO()
        writer = csv.DictWriter(output, headers, delimiter=";")
        writer.writeheader()
        for stats in serializer.data:
            writer.writerow(stats)
        csv_output = output.getvalue()
        response = FileResponse(csv_output, as_attachment=True)
        return response

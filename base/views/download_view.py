import csv
import io
from django.http import  FileResponse
from rest_framework.views import APIView

from base.models import Constant
from base.serializers.bonus_serializer import ConstantsSerializer

class DownloadCSVView(APIView):
    serializer_class = ConstantsSerializer

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            Constant.objects.all(),
            many=True
        )

        headers = ('ID', 'Year', 'Month','PersPart', 'DaysInMonth', 'LeadMultiplier', 'extMultiplier')

        output = io.StringIO()
        writer = csv.DictWriter(output, headers)
        writer.writeheader()
        for stats in serializer.data:
            writer.writerow(stats)
        csv_output = output.getvalue()
        response = FileResponse(csv_output, as_attachment=True)
        return response


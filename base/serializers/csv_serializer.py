from rest_framework import serializers

from base.models import CSVExportView_Basic


class CSVExportView_BasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVExportView_Basic
        exclude = ('Month', 'Year', 'ID')

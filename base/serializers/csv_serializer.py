from rest_framework import serializers

from base.models import CSVExportView_Basic


class CSVExportView_BasicSerializer(serializers.ModelSerializer):

    ID = serializers.CharField()
    Year= serializers.CharField()
    Month= serializers.CharField()
    LastName= serializers.CharField()
    FirstName= serializers.CharField()
    PositionName= serializers.CharField()
    Line= serializers.CharField()
    HourlyRate= serializers.CharField()
    DaysAtWork= serializers.CharField()
    ProdPart= serializers.CharField()
    PersPart= serializers.CharField()
    BO10= serializers.CharField()
    DaysInMonth= serializers.CharField()
    BasicPay= serializers.CharField()
    Bonus= serializers.CharField()
    LeadMoney= serializers.CharField()
    TeachMoney= serializers.CharField()
    OneTimeMoney= serializers.CharField()
    LeadHours= serializers.CharField()
    TeachHours= serializers.CharField()
    ExtHours= serializers.CharField()
    BonusBudget= serializers.CharField()
    BonusDelta= serializers.CharField()
    BO46= serializers.CharField()
    BO19= serializers.CharField()
    PersNr= serializers.CharField()

    class Meta:
        model = CSVExportView_Basic
        fields = '__all__'
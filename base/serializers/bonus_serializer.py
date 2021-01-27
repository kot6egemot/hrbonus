from rest_framework import serializers
from base.models import Bonuses_Summary, Lines, Position


class BonusSerializer(serializers.ModelSerializer):
    PositionFK = serializers.CharField()
    LineFK = serializers.CharField()
    PersPart = serializers.CharField()
    BO10 = serializers.CharField()
    DaysInMonth = serializers.CharField()
    LeadMoney = serializers.CharField()
    TeachMoney = serializers.CharField()
    OneTimeMoney = serializers.CharField()
    LeadHours = serializers.CharField()
    TeachHours = serializers.CharField()
    TotalExtMoney = serializers.CharField()
    BO46 = serializers.CharField()
    BO19 = serializers.CharField()

    class Meta:
        model = Bonuses_Summary
        fields = '__all__'


class LinesSerializer(serializers.ModelSerializer):
    LineId = serializers.CharField()
    Name = serializers.CharField()
    CostCenter = serializers.CharField()
    EffectivePlan = serializers.CharField()
    EffectiveFact = serializers.CharField()
    ErrorPlan = serializers.CharField()
    ErrorFact = serializers.CharField()
    Decision = serializers.CharField()

    class Meta:
        model = Lines
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    PositionID = serializers.CharField()
    PositionName = serializers.CharField()
    HourlyRate = serializers.CharField()

    class Meta:
        model = Position
        fields = '__all__'

from rest_framework import serializers
from base.models import Bonuses_Summary


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

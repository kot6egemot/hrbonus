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

    def to_representation(self, instance):
        """
            Подставляет пустую строчку в значение поля если поле == None
        """
        data = super().to_representation(instance)
        for field in Bonuses_Summary.editable_columns():
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        return data


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


class LinesDependSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='LineId')
    text = serializers.CharField(source='Name')

    class Meta:
        model = Lines
        fields = ('value', 'text')


class PositionSerializer(serializers.ModelSerializer):
    PositionID = serializers.CharField()
    PositionName = serializers.CharField()
    HourlyRate = serializers.CharField()

    class Meta:
        model = Position
        fields = '__all__'

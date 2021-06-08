from rest_framework import serializers
from base.models import Bonuses_Summary, Constant, IndividualChanges, Positions, LinesRates, LinesList, DailyReports


class BonusSerializer(serializers.ModelSerializer):
    ID = serializers.CharField()

    PositionFK = serializers.CharField()
    LineFK = serializers.CharField()  # Поле зависимой модели.
    PersPart = serializers.CharField()
    BO10 = serializers.CharField()
    DaysInMonth = serializers.CharField()
    LeadMoney = serializers.CharField()
    TeachMoney = serializers.CharField()
    OneTimeMoney = serializers.CharField()
    LeadHours = serializers.CharField()
    TeachHours = serializers.CharField()
    BonusMultiplier = serializers.CharField()
    ExtHours = serializers.CharField()
    TotalExtMoney = serializers.CharField()

    ExtMultiplier = serializers.SerializerMethodField()

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

    def get_ExtMultiplier(self, instance):
        constant = Constant.objects.filter(Year=instance.Year, Month=instance.Month).first()
        # Что то возвращать по умолчанию?
        if not constant:
            # temporary
            return 1
        return constant.extMultiplier

class LinesSerializer(serializers.ModelSerializer):
    ID = serializers.CharField()

    LineFK = serializers.SerializerMethodField()

    EffectivePlan = serializers.CharField()
    EffectiveFact = serializers.CharField()
    ErrorPlan = serializers.CharField()
    ErrorFact = serializers.CharField()
    Decision = serializers.CharField()

    class Meta:
        model = LinesRates
        fields = '__all__'

    def get_LineFK(self, instance):
        line = instance.LineFK
        return  f'{line.Name} | {line.CostCenter}'

class LinesDependSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='ID')
    text = serializers.CharField(source='Name')

    class Meta:
        model = LinesList
        fields = ('value', 'text')


class ConstantsSerializer(serializers.ModelSerializer):
    ID = serializers.CharField()

    Year = serializers.CharField()
    Month = serializers.CharField()
    PersPart = serializers.CharField()
    DaysInMonth = serializers.CharField()
    LeadMultiplier = serializers.CharField()
    extMultiplier = serializers.CharField()

    class Meta:
        model = Constant
        fields = '__all__'


class IndividualChangesSerializer(serializers.ModelSerializer):
    ID = serializers.CharField()

    Year = serializers.CharField()
    Month = serializers.CharField()

    PersNr = serializers.SerializerMethodField()

    HourlyRate = serializers.CharField()
    TimeMultiplier = serializers.CharField()
    LineFK = serializers.CharField()
    PositionFK = serializers.CharField()

    class Meta:
        model = IndividualChanges
        fields = '__all__'

    def get_PersNr(self, instance):
        person = Bonuses_Summary.objects.filter(Year=instance.Year, Month=instance.Month, PersNr=instance.PersNr).first()
        full_name = person.FirstName + ' ' + person.LastName
        return full_name

# Для загрузки людей в Select Column.
# Форма создания
class IndividualBonusDependSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='PersNr')
    text = serializers.SerializerMethodField()

    class Meta:
        model = Bonuses_Summary
        fields = ('value', 'text')

    def get_text(self, instance):
        return instance.full_name

class PostionDependSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='ID')
    text = serializers.CharField(source='PositionName')

    class Meta:
        model = Positions
        fields = ('value', 'text')



class DayliReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyReports
        fields = '__all__'

class DayliReportsCSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReports
        exclude = ('Month', 'Year', 'ID')

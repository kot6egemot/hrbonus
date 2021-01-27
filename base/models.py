from django.db import models


class Bonuses_Summary(models.Model):
    Year = models.TextField() # int
    Month = models.TextField()  # int
    PersNr = models.CharField(primary_key=True, max_length=10)

    BO46 = models.FloatField()
    BO19 = models.FloatField()
    BO10 = models.PositiveIntegerField()

    LastName = models.TextField()
    FirstName = models.TextField()
    AddName = models.TextField()
    PositionFK = models.PositiveIntegerField()
    LineFK = models.PositiveIntegerField()
    PersPart = models.PositiveIntegerField()
    DaysInMonth = models.PositiveIntegerField()
    LeadMoney = models.FloatField()
    TeachMoney = models.FloatField()
    OneTimeMoney = models.FloatField()
    LeadHours = models.PositiveIntegerField()
    TeachHours = models.PositiveIntegerField()
    TotalExtMoney = models.FloatField()


    class Meta:
        db_table = 'bonuses_summary'

    @classmethod
    def get_model_fields(cls):
        return [field.name for field in cls._meta.fields]

class Lines(models.Model):
    LineId = models.CharField(primary_key=True, max_length=10)
    Name = models.TextField()
    CostCenter = models.TextField()
    EffectivePlan = models.TextField()
    EffectiveFact = models.TextField()
    ErrorPlan = models.TextField()
    ErrorFact = models.TextField()
    Decision = models.TextField()

    class Meta:
        db_table = 'lines'

    @classmethod
    def get_model_fields(cls):
        return [field.name for field in cls._meta.fields]

class Position(models.Model):
    PositionID = models.CharField(primary_key=True, max_length=10)
    PositionName = models.TextField()
    HourlyRate = models.TextField()

    class Meta:
        db_table = 'positions'

    @classmethod
    def get_model_fields(cls):
        return [field.name for field in cls._meta.fields]
from django.db import models

class BaseModel(models.Model):

    class Meta:
        abstract = True

    @classmethod
    def get_headers(cls):
        fields = cls.get_model_fields()
        headers = [{'text': field['text'], 'value': field['name'], 'foreign_key': True} for field in fields] + [
            {'text': 'Actions', 'value': 'Actions'}]
        return headers

    @classmethod
    def get_model_fields(cls):
        return [{'name' : field.name,  'text': field.verbose_name or field.verbose_name or field.name} for field in cls._meta.fields]

class Bonuses_Summary(BaseModel):
    Year = models.TextField() # int
    Month = models.TextField()  # int
    PersNr = models.CharField(primary_key=True, max_length=10)

    BO46 = models.FloatField()
    BO19 = models.FloatField()
    BO10 = models.PositiveIntegerField()

    LastName = models.TextField()
    FirstName = models.TextField(verbose_name='Имя')
    AddName = models.TextField()
    PositionFK = models.PositiveIntegerField()
    LineFK = models.ForeignKey("Lines", on_delete=models.CASCADE, db_column="LineFK")
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





class Lines(BaseModel):
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

    def __str__(self):
        return self.Name if self.Name else 'НетИмени'

class Position(BaseModel):
    PositionID = models.CharField(primary_key=True, max_length=10)
    PositionName = models.TextField()
    HourlyRate = models.TextField()

    class Meta:
        db_table = 'positions'

from django.db import models

"""
    display_relative_model - внешнии ключи в другую таблицу, значение которых надо подгрузить.
                             предоставить url => entity_{foreign_key}
"""


class BaseModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_columns(cls, hide_columns=None):
        if hide_columns is None:
            hide_columns = list()
        fields = cls.get_model_fields()
        displayed_foreign_fields = cls.displayed_foreign_fields()
        columns = [{'text': 'Actions', 'value': 'Actions'}] \
                  + [
                      {
                          'text': field['text'], 'value': field['name'],
                          'display_relative_model': True if field['name'] in displayed_foreign_fields else False,
                      }
                      for field in fields if field['name'] not in hide_columns
                  ]
        return columns

    @classmethod
    def get_model_fields(cls):
        return [{'name': field.name, 'text': field.verbose_name or field.name} for field in
                cls._meta.fields]

    @staticmethod
    def displayed_foreign_fields() -> list:
        return []

    @staticmethod
    def editable_columns() -> list:
        return []


class Bonuses_Summary(BaseModel):
    Year = models.TextField(verbose_name='Год')  # int
    Month = models.TextField(verbose_name='Месяц')  # int
    PersNr = models.CharField(primary_key=True, max_length=10)

    BO46 = models.FloatField()
    BO19 = models.FloatField()
    BO10 = models.PositiveIntegerField()

    LastName = models.TextField(verbose_name='Фамилия')
    FirstName = models.TextField(verbose_name='Имя')
    AddName = models.TextField()
    PositionFK = models.PositiveIntegerField()
    LineFK = models.ForeignKey("Lines", on_delete=models.CASCADE, db_column="LineFK", verbose_name='Линия')
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

    @staticmethod
    def displayed_foreign_fields():
        return ['LineFK']

    @staticmethod
    def editable_columns():
        return ["LeadMoney", "TeachMoney", "PersPart", 'LineFK']


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
        return str(self.LineId)

    @staticmethod
    def editable_columns():
        return ["LeadMoney", "TeachMoney", "PersPart"]


class Position(BaseModel):
    PositionID = models.CharField(primary_key=True, max_length=10)
    PositionName = models.TextField()
    HourlyRate = models.TextField()

    class Meta:
        db_table = 'positions'

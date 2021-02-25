import uuid

from django.db import models

"""
    display_relative_model - внешнии ключи в другую таблицу, значение которых надо подгрузить.
                             предоставить url => entity_{foreign_key}
"""


class BaseModel(models.Model):
    ID = models.TextField(primary_key=True ,verbose_name='UUID', max_length=100)


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
        """
            Для отобраения выпадающего списка зависимой модели необходимо
            Добавить view на url ->  param_entity из BaseGenericListView + имя столбца
            Для примера ->  bonus_linefk

            Пример сериалайзера зависимой модели.
            class LinesDependSerializer(serializers.ModelSerializer):
                value = serializers.CharField(source='LineId')
                text = serializers.CharField(source='Name')

                class Meta:
                    model = Lines
                    fields = ('value', 'text')
        """
        return []

    @staticmethod
    def editable_columns() -> list:
        return []

    @staticmethod
    def depend_select_columns() -> list:
        """ Поля которые должны менятся в представлении при измении выбора в Select."""
        return []

    @staticmethod
    def forms_columns():
        return []

class Bonuses_Summary(BaseModel):
    LastName = models.TextField(verbose_name='Фамилия')
    FirstName = models.TextField(verbose_name='Имя')


    PositionFK = models.ForeignKey("Position", db_column="PositionFK",  related_name='position',  verbose_name='Позиция',
                                   on_delete=models.CASCADE, )  # +++ Отобразить с другой таблицы.


    LineFK = models.ForeignKey("Lines", related_name='line', db_column="LineFK",
                               on_delete=models.CASCADE, verbose_name='Линия')  # +++ Оторазить с другой таблицы.

    BO10 = models.PositiveIntegerField(verbose_name="Производственная часть")
    PersPart = models.PositiveIntegerField(verbose_name="Индивидуальная часть")
    BonusMultiplier = models.PositiveIntegerField(verbose_name="Коэф. премирования")
    DaysInMonth = models.PositiveIntegerField(verbose_name="Норма дней/месяц")
    LeadMoney = models.FloatField(verbose_name="Надбавка за бригадирство")
    TeachMoney = models.FloatField(verbose_name="Надбавка за наставничество")
    OneTimeMoney = models.FloatField(verbose_name="Единовременные премии")
    LeadHours = models.PositiveIntegerField(verbose_name="Часы управления бригадой")
    TeachHours = models.PositiveIntegerField(verbose_name="Часы наставничества")
    ExtHours = models.PositiveIntegerField(verbose_name="Часы расширения обязанностей")  # +++ Вычислямое поле
    TotalExtMoney = models.FloatField(verbose_name="Расширение обязанностей")  # +++ Вычислямое поле
    PersNr = models.CharField(max_length=10, verbose_name="Персональный номер SAP")

    Year = models.TextField(verbose_name='Год')  # int
    Month = models.TextField(verbose_name='Месяц')  # int

    # Не отображать в таблице
    BO46 = models.FloatField()
    BO19 = models.FloatField()
    AddName = models.TextField()

    class Meta:
        db_table = 'bonuses_summary'

    @staticmethod
    def displayed_foreign_fields():
        return []

    @staticmethod
    def editable_columns():
        return ["OneTimeMoney", "ExtHours", "PersPart"]

    @property
    def full_name(self):
        return f'{self.FirstName} {self.LastName}'

class Lines(BaseModel):
    LineID = models.CharField(max_length=10)

    Year = models.TextField(verbose_name='Год')  # int
    Month = models.TextField(verbose_name='Месяц')  # int

    Name = models.TextField(verbose_name="Линия")
    CostCenter = models.TextField()
    EffectivePlan = models.PositiveIntegerField()
    EffectiveFact = models.PositiveIntegerField()
    ErrorPlan = models.PositiveIntegerField()
    ErrorFact = models.PositiveIntegerField()
    Decision = models.PositiveIntegerField()

    class Meta:
        db_table = 'lines'

    def __str__(self):
        return str(self.LineID)

    @staticmethod
    def editable_columns():
        return ["EffectivePlan", "EffectiveFact", "ErrorPlan", "ErrorFact", "Decision"]


class Constant(BaseModel):

    Year = models.TextField(verbose_name='Год')  # int
    Month = models.TextField(verbose_name='Месяц')  # int

    PersPart = models.PositiveIntegerField(verbose_name="Персональная часть")
    DaysInMonth = models.TextField(verbose_name="Норма дней/месяц")
    LeadMultiplier = models.PositiveIntegerField()
    extMultiplier = models.PositiveIntegerField()

    class Meta:
        db_table = 'constants'

    @staticmethod
    def editable_columns():
        return ["PersPart", "DayslnMonth", "LeadMultiplier", "extMultiplier"]


class IndividualChanges(BaseModel):

    Year = models.TextField(verbose_name='Год')  # int
    Month = models.TextField(verbose_name='Месяц')  # int

    PersNr = models.CharField(max_length=10, verbose_name="Сотрудник")
    HourlyRate = models.TextField(verbose_name="Часовая ставка, Оклад")
    LineFK = models.TextField(verbose_name="Линия")
    PositionFK = models.TextField(verbose_name="Позиция")

    class Meta:
        db_table = 'individualchanges'

    @staticmethod
    def editable_columns():
        return ["HourlyRate", "LineFK", "PositionFK"]

    @staticmethod
    def displayed_foreign_fields():
        return ['LineFK', 'PositionFK']

    @staticmethod
    def depend_select_columns():
        return ['PositionFK']

    @staticmethod
    def forms_columns():
        return []

class Position(BaseModel):
    PositionID = models.CharField(max_length=10)

    Year = models.TextField(verbose_name='Год')  # int
    Month = models.TextField(verbose_name='Месяц')  # int

    PositionName = models.TextField()
    HourlyRate = models.TextField(verbose_name="Часовая ставка, Оклад")

    class Meta:
        db_table = 'positions'

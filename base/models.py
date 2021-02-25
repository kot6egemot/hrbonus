import uuid

from django.db import models

"""
    display_relative_model - внешнии ключи в другую таблицу, значение которых надо подгрузить.
                             предоставить url => entity_{foreign_key}
"""


class BaseModel(models.Model):
    ID = models.TextField(primary_key=True, verbose_name='UUID', max_length=100)

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

    PositionFK = models.ForeignKey("Positions", db_column="PositionFK", related_name='position', verbose_name='Позиция',
                                   on_delete=models.CASCADE, to_field='ID')  # +++ Отобразить с другой таблицы.

    LineFK = models.ForeignKey("LinesList", related_name='line', db_column="LineFK",
                               on_delete=models.CASCADE, verbose_name='Линия',
                               to_field='ID')  # +++ Оторазить с другой таблицы.

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


class LinesRates(BaseModel):
    LineFK = models.ForeignKey('LinesList', db_column="LineFK", to_field='ID', on_delete=models.CASCADE, verbose_name="Линия")
    EffectivePlan = models.FloatField(verbose_name="Эффективность(План)")
    EffectiveFact = models.FloatField(verbose_name="Эффективность(Факт)")
    ErrorPlan = models.FloatField(verbose_name="Брак(План)")
    ErrorFact = models.FloatField(verbose_name="Брак(Факт)")
    Decision = models.PositiveIntegerField(verbose_name="Решение по производственной части")

    Year = models.TextField(verbose_name='Год')  # int
    Month = models.TextField(verbose_name='Месяц')  # int

    class Meta:
        db_table = 'linesrates'

    def __str__(self):
        return str(self.ID)

    @staticmethod
    def editable_columns():
        return ["EffectivePlan", "EffectiveFact", "ErrorPlan", "ErrorFact", "Decision"]


class LinesList(BaseModel):
    Name = models.TextField()
    CostCenter = models.TextField()

    class Meta:
        db_table = 'lineslist'

    def __str__(self):
        return str(self.Name)


class Constant(BaseModel):
    PersPart = models.PositiveIntegerField(verbose_name="Персональная часть (По умолчанию)")
    DaysInMonth = models.PositiveIntegerField(verbose_name="Норма дней/месяц")
    LeadMultiplier = models.FloatField(verbose_name="Коэффициент (Бригадирство)")
    extMultiplier = models.FloatField(verbose_name="Коэффициент (Расширение обязанностей)")

    Year = models.TextField(verbose_name='Год')  # int
    Month = models.TextField(verbose_name='Месяц')  # int

    class Meta:
        db_table = 'constants'

    @staticmethod
    def editable_columns():
        return ["PersPart", "DayslnMonth", "LeadMultiplier", "extMultiplier"]


class IndividualChanges(BaseModel):
    PersNr = models.CharField(max_length=10, verbose_name="Сотрудник")
    HourlyRate = models.TextField(verbose_name="Часовая ставка, Оклад")
    LineFK = models.TextField(verbose_name="Линия")
    PositionFK = models.ForeignKey('Positions', db_column='PositionFK', to_field='ID', verbose_name='Позиция',
                                   on_delete=models.CASCADE)

    Year = models.TextField(verbose_name='Год')  # int
    Month = models.TextField(verbose_name='Месяц')  # int

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


class PositionRates(BaseModel):
    PositionFK = models.CharField(max_length=10)
    HourlyRate = models.TextField(verbose_name="Часовая ставка, Оклад")

    Year = models.TextField(verbose_name='Год')  # int
    Month = models.TextField(verbose_name='Месяц')  # int

    class Meta:
        db_table = 'positionsrates'


class Positions(BaseModel):
    PositionName = models.TextField()

    class Meta:
        db_table = 'positionslist'

    def __str__(self):
        return str(self.ID)

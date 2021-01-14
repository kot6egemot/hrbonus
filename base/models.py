from django.db import models


class Bonuses_Summary(models.Model):
    PersNr = models.CharField(primary_key=True, max_length=10)
    LastName = models.TextField()
    FirstName = models.TextField()
    AddName = models.TextField()
    PositionFK = models.PositiveIntegerField()
    LineFK = models.PositiveIntegerField()
    PersPart = models.PositiveIntegerField()
    BO10 = models.PositiveIntegerField()
    DaysInMonth = models.PositiveIntegerField()
    LeadMoney = models.FloatField()
    TeachMoney = models.FloatField()
    OneTimeMoney = models.FloatField()
    LeadHours = models.PositiveIntegerField()
    TeachHours = models.PositiveIntegerField()
    TotalExtMoney = models.FloatField()
    BO46 = models.FloatField()
    BO19 = models.FloatField()

    class Meta:
        db_table = 'bonuses_summary'

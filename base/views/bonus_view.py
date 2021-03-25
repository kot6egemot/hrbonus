from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Bonuses_Summary, LinesList, BlockBonus, BonusChange
from base.serializers.bonus_serializer import BonusSerializer, LinesDependSerializer
from base.views.utils import BaseGenericListView

from django.db import transaction


def attr_changed(old, new):
    return str(old) != str(new)


class BonusViewGenericListView(BaseGenericListView):
    _model = Bonuses_Summary
    _param_entity = 'bonus'
    _serialize = BonusSerializer
    _hide_columns = ['BO46', 'BO19', 'AddName', 'ID']


class BonusLineViewGenericListView(BaseGenericListView):
    _model = LinesList
    _param_entity = 'bonus_linefk'
    _serialize = LinesDependSerializer


def save_bonus_item(data):
    bonus = Bonuses_Summary.objects.get(ID=data['ID'])
    bonus.PersPart = data['PersPart']
    bonus.BonusMultiplier = data['BonusMultiplier']
    bonus.OneTimeMoney = data['OneTimeMoney']
    bonus.ExtHours = data['ExtHours']
    bonus.TotalExtMoney = data['TotalExtMoney']

    # Обаработка был ли столбец изменен.
    if attr_changed(bonus.LeadHours, data['LeadHours']) or attr_changed(bonus.TeachHours, data['TeachHours']):
        bonus_change = BonusChange.objects.filter(Year=data['Year'], Month=data['Month'], PersNr=data['PersNr']).first()
        if not bonus_change:
            bonus_change = BonusChange(
                Year=data['Year'],
                Month=data['Month'],
                PersNr=data['PersNr'],
            )
        if attr_changed(bonus.LeadHours, data['LeadHours']):
            bonus_change.LeadHours_changed = True
        if attr_changed(bonus.TeachHours, data['TeachHours']):
            bonus_change.TeachHours_changed = True
        bonus_change.save()

    bonus.LeadHours = data['LeadHours']
    bonus.TeachHours = data['TeachHours']

    bonus.save()

    return bonus


class BonusView(APIView, BonusViewGenericListView):
    def post(self, request):
        bonus_item = request.data

        if isinstance(bonus_item, list):
            try:
                with transaction.atomic():
                    for item in bonus_item:
                        save_bonus_item(item)
            except Exception:
                raise Exception('Не удалось сохранить элементы.')

            serialize = BonusSerializer(Bonuses_Summary.objects.all(), many=True)
            return JsonResponse({"result": True, "items": serialize.data})
        else:
            item = save_bonus_item(bonus_item)
            serialize = BonusSerializer(item)
            return JsonResponse({"result": True, "item": serialize.data})


class BonusLineView(APIView, BonusLineViewGenericListView):
    pass


class BlockBonusView(APIView):

    def get(self, request):
        Year = request.GET['Year']
        Month = request.GET['Month']
        block = BlockBonus.objects.filter(Year=Year, Month=Month).first()
        if not block:
            block = BlockBonus(Year=Year, Month=Month, is_blocking=False)
        block.save()

        return JsonResponse({
            'result': True,
            'block_data': {
                'is_block': block.is_blocking,
                'Year': block.Year,
                'Month': block.Month
            }
        })

    def post(self, request):
        Year = request.GET['Year']
        Month = request.GET['Month']
        block = BlockBonus.objects.filter(Year=Year, Month=Month).first()
        block.is_blocking = not block.is_blocking
        block.save()

        return JsonResponse({
            'result': True,
            'block_data': {
                'is_block': block.is_blocking,
                'Year': block.Year,
                'Month': block.Month
            }
        })

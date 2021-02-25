from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Bonuses_Summary, LinesList
from base.serializers.bonus_serializer import BonusSerializer, LinesDependSerializer
from base.views.utils import BaseGenericListView

from django.db import transaction

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
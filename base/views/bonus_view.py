from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Bonuses_Summary, Lines
from base.serializers.bonus_serializer import BonusSerializer, LinesDependSerializer
from base.views.utils import delete_props, BaseGenericListView


class BonusViewGenericListView(BaseGenericListView):
    _model = Bonuses_Summary
    _param_entity = 'bonus'
    _serialize = BonusSerializer
    _hide_columns = ['BO46', 'BO19', 'AddName']

class BonusLineViewGenericListView(BaseGenericListView):
    _model = Lines
    _param_entity = 'bonus_linefk'
    _serialize = LinesDependSerializer


class BonusView(APIView, BonusViewGenericListView):
    def post(self, request):
        bonus_item = request.data
        if isinstance(bonus_item, list):
            bonus_item = [delete_props(bonus) for bonus in bonus_item]
            return JsonResponse({"result": True, "items": bonus_item})
        else:
            delete_props(bonus_item)
            bonus_item["PositionFK"] = randint(1, 100)
            return JsonResponse({"result": True, "item": bonus_item})

class BonusLineView(APIView, BonusLineViewGenericListView):
    pass
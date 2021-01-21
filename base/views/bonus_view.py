from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Bonuses_Summary
from base.serializers.bonus_serializer import BonusSerializer


class BonusView(APIView):

    def get(self, request):
        bonuses = Bonuses_Summary.objects.all()
        fields = Bonuses_Summary.get_model_fields()
        headers = [{'text': field, 'value': field} for field in fields] + [{'text': 'Actions', 'value': 'Actions'}]
        serialize = BonusSerializer(bonuses, many=True)
        return JsonResponse({"result": True, "_bonus": serialize.data, "__bonus": serialize.data, 'bonus_headers': headers})

    def post(self, request):
        bonus_item = request.data
        bonus_item["PositionFK"]  = randint(1, 100)
        del bonus_item["changed"]
        return JsonResponse({"result": True, "_item": bonus_item,  "__item": bonus_item})
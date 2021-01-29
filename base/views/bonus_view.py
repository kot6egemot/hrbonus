from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Bonuses_Summary
from base.serializers.bonus_serializer import BonusSerializer
from base.views.utils import delete_props


class BonusView(APIView):

    def get(self, request):
        bonuses = Bonuses_Summary.objects.all()
        headers = Bonuses_Summary.get_headers()

        editable_columns = ["LeadMoney", "TeachMoney", "PersPart"]

        serialize = BonusSerializer(bonuses, many=True)

        return JsonResponse(
            {
                "result": True,
                "bonus": serialize.data,
                'headers': headers,
                "editable_columns": editable_columns
            }
        )

    def post(self, request):
        bonus_item = request.data
        if isinstance(bonus_item, list):
            bonus_item = [delete_props(bonus) for bonus in bonus_item]
            return JsonResponse({"result": True, "items": bonus_item})
        else:
            delete_props(bonus_item)
            bonus_item["PositionFK"] = randint(1, 100)
            return JsonResponse({"result": True, "item": bonus_item})




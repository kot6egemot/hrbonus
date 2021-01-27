from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Bonuses_Summary
from base.serializers.bonus_serializer import BonusSerializer

def delete_props(bonus):
    del bonus['changed']
    return bonus

class BonusView(APIView):

    def get(self, request):
        bonuses = Bonuses_Summary.objects.all()
        fields = Bonuses_Summary.get_model_fields()
        editable_columns = ["FirstName", "LastName"]
        headers = [{'text': field, 'value': field} for field in fields] + [{'text': 'Actions', 'value': 'Actions'}]
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

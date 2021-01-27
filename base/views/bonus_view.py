from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Lines, Bonuses_Summary, Position
from base.serializers.bonus_serializer import BonusSerializer, LinesSerializer, PositionSerializer


def delete_props(bonus):
    del bonus['changed']
    return bonus

class BonusView(APIView):

    def get(self, request):
        bonuses = Bonuses_Summary.objects.all()
        fields = Bonuses_Summary.get_model_fields()
        editable_columns = ["LeadMoney", "TeachMoney", "PersPart"]
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


class LinesView(APIView):

    def get(self, request):
        lineses = Lines.objects.all()
        fields = Lines.get_model_fields()
        editable_columns = ["EffectivePlan", "EffectiveFact", "ErrorPlan", "ErrorFact", "Decision"]
        headers = [{'text': field, 'value': field} for field in fields] + [{'text': 'Actions', 'value': 'Actions'}]
        serialize = LinesSerializer(lineses, many=True)
        return JsonResponse(
            {
                "result": True,
                "line": serialize.data,
                'headers': headers,
                "editable_columns": editable_columns
            }
        )

    def post(self, request):
        line_item = request.data
        if isinstance(line_item, list):
            line_item = [delete_props(line) for line in line_item]
            return JsonResponse({"result": True, "items": line_item})
        else:
            delete_props(line_item)
            line_item["PositionFK"] = randint(1, 100)
            return JsonResponse({"result": True, "item": line_item})


class PositionView(APIView):

    def get(self, request):
        positions = Position.objects.all()
        fields = Position.get_model_fields()
        editable_columns = ["EffectivePlan", "EffectiveFact", "ErrorPlan", "ErrorFact", "Decision"]
        headers = [{'text': field, 'value': field} for field in fields] + [{'text': 'Actions', 'value': 'Actions'}]
        serialize = PositionSerializer(positions, many=True)
        return JsonResponse(
            {
                "result": True,
                "position": serialize.data,
                'headers': headers,
                "editable_columns": editable_columns
            }
        )

    def post(self, request):
        position_item = request.data
        if isinstance(position_item, list):
            position_item = [delete_props(position) for position in position_item]
            return JsonResponse({"result": True, "items": position_item})
        else:
            delete_props(position_item)
            position_item["PositionFK"] = randint(1, 100)
            return JsonResponse({"result": True, "item": position_item})

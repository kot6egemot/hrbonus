from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Lines
from base.serializers.bonus_serializer import LinesSerializer
from base.views.utils import delete_props


class LinesView(APIView):

    def get(self, request):
        lineses = Lines.objects.all()
        headers = Lines.get_headers()

        editable_columns = ["EffectivePlan", "EffectiveFact", "ErrorPlan", "ErrorFact", "Decision"]
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
            return JsonResponse({"result": True, "item": line_item})

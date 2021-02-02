from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Lines
from base.serializers.bonus_serializer import LinesSerializer
from base.views.utils import delete_props


class LinesView(APIView):

    def get(self, request):
        lineses = Lines.objects.all()
        columns = Lines.get_columns(hide_columns=['LineId'])


        prop_columns = {
            'editable_columns': Lines.editable_columns(),
            'depend_columns': Lines.displayed_foreign_fields()
        }

        serialize = LinesSerializer(lineses, many=True)

        return JsonResponse(
            {
                "result": True,
                "line": serialize.data,
                'columns': columns,
                "prop_columns": prop_columns
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

from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Lines
from base.serializers.bonus_serializer import LinesSerializer
from base.views.utils import delete_props, BaseGenericListView


class LinesViewGenericListView(BaseGenericListView):
    _model = Lines
    _param_entity = 'line'
    _serialize = LinesSerializer
    _hide_columns = ['LineId']


class LinesView(APIView, LinesViewGenericListView):

    def post(self, request):
        line_item = request.data
        if isinstance(line_item, list):
            line_item = [delete_props(line) for line in line_item]
            return JsonResponse({"result": True, "items": line_item})
        else:
            delete_props(line_item)
            return JsonResponse({"result": True, "item": line_item})

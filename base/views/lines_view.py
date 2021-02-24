from random import randint

from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Lines
from base.serializers.bonus_serializer import LinesSerializer
from base.views.utils import delete_props, BaseGenericListView


def save_line_item(line_date):
    line = Lines.objects.get(ID=line_date['ID'])
    line.EffectivePlan = line_date['EffectivePlan']
    line.EffectiveFact = line_date['EffectiveFact']
    line.ErrorPlan = line_date['ErrorPlan']
    line.ErrorFact = line_date['ErrorFact']
    line.Decision = line_date['Decision']
    line.save()
    return line

class LinesViewGenericListView(BaseGenericListView):
    _model = Lines
    _param_entity = 'line'
    _serialize = LinesSerializer
    _hide_columns = ['LineId', 'ID']


class LinesView(APIView, LinesViewGenericListView):

    def post(self, request):
        line_item = request.data

        if isinstance(line_item, list):
            try:
                with transaction.atomic():
                    for line in line_item:
                        save_line_item(line)
            except Exception:
                raise Exception('Не удалось сохранить элементы.')

            lines = Lines.objects.all()
            serialize = LinesSerializer(lines, many=True)
            return JsonResponse({"result": True, "items": serialize.data})
        else:
            line = save_line_item(line_item)
            serialize = LinesSerializer(line)
            return JsonResponse({"result": True, "item": serialize.data})

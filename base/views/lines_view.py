from random import randint

from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Lines
from base.serializers.bonus_serializer import LinesSerializer
from base.views.utils import delete_props, BaseGenericListView


def save_line_item(line_date):
    line = Lines.objects.get(LineId=line_date['LineId'])
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
    _hide_columns = ['LineId']


class LinesView(APIView, LinesViewGenericListView):

    def post(self, request):
        line_item = request.data

        if isinstance(line_item, list):
            for line in line_item:
                save_line_item(line)
            lines = Lines.objects.all()
            serialize = LinesSerializer(lines, many=True)
            return JsonResponse({"result": True, "items": serialize.data})
        else:
            line = save_line_item(line_item)
            serialize = LinesSerializer(line)
            return JsonResponse({"result": True, "item": serialize.data})

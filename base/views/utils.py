from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import DailyReports, IndividualChanges


class BaseGenericListView:
    _model = None
    _param_entity = ''
    _serialize = None
    _hide_columns = []

    def get(self, request):
        entity = self._model.objects.all()
        columns = self._model.get_columns(hide_columns=self._hide_columns)
        prop_columns = {
            'editable_columns': self._model.editable_columns(),
            'select_columns': self._model.displayed_foreign_fields(),
            'depend_select_columns': self._model.depend_select_columns(),
        }
        serialize = self._serialize(entity, many=True)

        return JsonResponse(
            {
                "result": True,
                self._param_entity: serialize.data,
                'columns': columns,
                "prop_columns": prop_columns
            }
        )


def delete_props(bonus):
    del bonus['changed']
    return bonus


def get_month_year(request):
    month = request.GET['month']
    year = request.GET['year']
    return month, year


class UpdateModelField(APIView):
    def post(self, request, entity, id):
        print(request.data, entity, id)
        map_entities_models = {
            "individual_change": IndividualChanges
        }
        request_data = request.data
        item = map_entities_models.get(entity).objects.get(ID=id)
        item.__setattr__(request_data["field"], request_data["value"])
        print(item.TimeMultiplier)
        item.save()
        return JsonResponse({"result": True})

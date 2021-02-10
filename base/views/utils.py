from django.http import JsonResponse

class BaseGenericListView:
    _model = None
    _param_entity = ''
    _serialize = None
    _hide_columns = []

    def get(self, request):
        entity = self._model.objects.all()[:3]
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
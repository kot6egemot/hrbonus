from django.http import JsonResponse

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
            'depend_columns': self._model.displayed_foreign_fields()
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
from rest_framework.views import APIView

from base.models import IndividualChanges
from base.serializers.bonus_serializer import IndividualChangesSerializer
from base.views.utils import BaseGenericListView


class IndividualChangesViewGenericListView(BaseGenericListView):
    _model = IndividualChanges
    _param_entity = 'individual_change'
    _serialize = IndividualChangesSerializer


class IndividualChangesView(APIView, IndividualChangesViewGenericListView):
    pass
    # Удаление и добавлении персоны.

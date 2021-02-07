from rest_framework.views import APIView

from base.models import IndividualChanges, Lines
from base.serializers.bonus_serializer import IndividualChangesSerializer, LinesDependSerializer
from base.views.utils import BaseGenericListView


class IndividualChangesViewGenericListView(BaseGenericListView):
    _model = IndividualChanges
    _param_entity = 'individual_change'
    _serialize = IndividualChangesSerializer


class IndividualChangesLineViewGenericListView(BaseGenericListView):
    _model = Lines
    _param_entity = 'individual_change_linefk'
    _serialize = LinesDependSerializer


class IndividualChangesView(APIView, IndividualChangesViewGenericListView):
    pass
    # Удаление и добавлении персоны.


class IndividualLineView(APIView, IndividualChangesLineViewGenericListView):
    pass
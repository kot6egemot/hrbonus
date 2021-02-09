from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import IndividualChanges, Lines, Position, Bonuses_Summary
from base.serializers.bonus_serializer import IndividualChangesSerializer, LinesDependSerializer, \
    PostionDependSerializer, IndividualBonusDependSerializer
from base.views.utils import BaseGenericListView


class IndividualChangesViewGenericListView(BaseGenericListView):
    _model = IndividualChanges
    _param_entity = 'individual_change'
    _serialize = IndividualChangesSerializer


class IndividualChangesLineViewGenericListView(BaseGenericListView):
    _model = Lines
    _param_entity = 'individual_change_linefk'
    _serialize = LinesDependSerializer


class IndividualChangesPositionViewGenericListView(BaseGenericListView):
    _model = Position
    _param_entity = 'individual_change_positionfk'
    _serialize = PostionDependSerializer


class IndividualChangesView(APIView, IndividualChangesViewGenericListView):
    pass


class IndividualLineView(APIView, IndividualChangesLineViewGenericListView):
    pass


class IndividualPositionView(APIView, IndividualChangesPositionViewGenericListView):
    pass


class IndividualPositionDependView(APIView):
    def get(self, request):
        item = Position.objects.get(PositionID=request.GET['PositionFk'])
        print(item)
        print(request.GET)
        return JsonResponse(
            {
                "result": True,
                "individual_change_positionfk_depend": {
                    'HourlyRate': str(item.HourlyRate)
                }
            }
        )

class IndividualCreateDependView(APIView):
    def get(self, request):

        month = request.GET['month']
        year = request.GET['year']

        items = Bonuses_Summary.objects.filter(Month=month, Year=year).all()
        serializer = IndividualBonusDependSerializer(items, many=True)

        return JsonResponse(
            {
                "result": True,
                "PersNr": serializer.data
            }
        )

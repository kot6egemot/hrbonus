from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import IndividualChanges, Lines, Position, Bonuses_Summary
from base.serializers.bonus_serializer import IndividualChangesSerializer, LinesDependSerializer, \
    PostionDependSerializer, IndividualBonusDependSerializer
from base.views.utils import BaseGenericListView, get_month_year, delete_props


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

    def put(self, request):
        month, year = get_month_year(request)
        PersNr = request.data["PersNr"]
        person_bonus = Bonuses_Summary.objects.filter(Month=month, Year=year, PersNr=PersNr).first()
        position = Position.objects.filter(PositionID=person_bonus.LineFK).first()
        individual_change = IndividualChanges(
            Month=month,
            Year=year,
            PersNr=person_bonus.PersNr,
            LineFk=person_bonus.LineFK,
            HourlyRate=position.HourlyRate,
            PositionFk=position.PositionID
        )
        serialize = IndividualChangesSerializer(individual_change)
        data = serialize.data
        data["changed"] = True
        return JsonResponse({
            "result": True,
            "new_item": data
        })

    def post(self, request):
        bonus_item = request.data

        # if isinstance(bonus_item, list):
        #     for item in bonus_item:
        #         save_bonus_item(item)
        #     serialize = BonusSerializer(Bonuses_Summary.objects.all(), many=True)
        #     return JsonResponse({"result": True, "items": serialize.data})
        # else:
        #     item = save_bonus_item(bonus_item)
        #     serialize = BonusSerializer(item)
        #     return JsonResponse({"result": True, "item": serialize.data})

        item = request.data
        item =  delete_props(item)

        return JsonResponse({
            'result': True,
            'item': item
        })


class IndividualLineView(APIView, IndividualChangesLineViewGenericListView):
    pass


class IndividualPositionView(APIView, IndividualChangesPositionViewGenericListView):
    pass


class IndividualPositionDependView(APIView):
    def get(self, request):
        item = Position.objects.get(PositionID=request.GET['PositionFk'])
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
        month, year = get_month_year(request)

        items = Bonuses_Summary.objects.filter(Month=month, Year=year).all()
        serializer = IndividualBonusDependSerializer(items, many=True)

        return JsonResponse(
            {
                "result": True,
                "PersNr": serializer.data
            }
        )

import uuid

from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import IndividualChanges, Bonuses_Summary, Positions, PositionRates, LinesList
from base.serializers.bonus_serializer import IndividualChangesSerializer, LinesDependSerializer, \
    PostionDependSerializer, IndividualBonusDependSerializer
from base.views.utils import BaseGenericListView, get_month_year, delete_props


class IndividualChangesViewGenericListView(BaseGenericListView):
    _model = IndividualChanges
    _param_entity = 'individual_change'
    _serialize = IndividualChangesSerializer
    _hide_columns = ['ID']


class IndividualChangesLineViewGenericListView(BaseGenericListView):
    _model = LinesList
    _param_entity = 'individual_change_linefk'
    _serialize = LinesDependSerializer


class IndividualChangesPositionViewGenericListView(BaseGenericListView):
    _model = Positions
    _param_entity = 'individual_change_positionfk'
    _serialize = PostionDependSerializer


def save_individual_changes(data):
    individual_change = IndividualChanges.objects.get(ID=data['ID'])
    individual_change.HourlyRate = data['HourlyRate']
    individual_change.LineFK = data['LineFK']
    position = Positions.objects.get(ID=data['PositionFK'])
    individual_change.PositionFK = position
    individual_change.save()
    return individual_change


class IndividualChangesView(APIView, IndividualChangesViewGenericListView):

    def put(self, request):
        month, year = get_month_year(request)
        PersNr = request.data["PersNr"]
        person_bonus = Bonuses_Summary.objects.filter(Month=month, Year=year, PersNr=PersNr).first()
        try:
            position_rate = PositionRates.objects.get(PositionFK=person_bonus.PositionFK.ID, Year=year, Month=month)
        except PositionRates.DoesNotExist:
            position_rate = PositionRates(
                PositionFK=person_bonus.PositionFK.ID,
                Year=year,
                Month=month,
                HourlyRate=0
            )
            position_rate.save()
        position = Positions.objects.get(ID=person_bonus.PositionFK.ID)
        line = person_bonus.LineFK

        individual_change = IndividualChanges(
            ID=uuid.uuid4(),
            Month=month,
            Year=year,
            PersNr=person_bonus.PersNr,
            LineFK=line.ID,
            HourlyRate=position_rate.HourlyRate,
            PositionFK=position,
        )

        individual_change.save()
        serialize = IndividualChangesSerializer(individual_change)
        data = serialize.data

        return JsonResponse({
            "result": True,
            "new_item": data
        })

    def post(self, request):
        individual_items = request.data

        if isinstance(individual_items, list):
            try:
                with transaction.atomic():
                    for item in individual_items:
                        save_individual_changes(item)
            except Exception:
                raise Exception('Не удалось сохранить элементы.')
            serialize = IndividualChangesSerializer(IndividualChanges.objects.all(), many=True)
            return JsonResponse({"result": True, "items": serialize.data})
        else:
            item = save_individual_changes(individual_items)
            serialize = IndividualChangesSerializer(item)
            return JsonResponse({"result": True, "item": serialize.data})

    def delete(self, request):
        id = request.data['ID']
        individual_change = IndividualChanges.objects.get(ID=id)
        individual_change.delete()
        return JsonResponse({"result": True, })


class IndividualLineView(APIView, IndividualChangesLineViewGenericListView):
    pass


class IndividualPositionView(APIView, IndividualChangesPositionViewGenericListView):
    pass


class IndividualPositionDependView(APIView):
    def get(self, request):
        data = request.GET
        item = PositionRates.objects.get(PositionFK=data['PositionFK'], Year=data['Year'], Month=data['Month'])
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

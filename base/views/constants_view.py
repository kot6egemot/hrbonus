from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Constant
from base.serializers.bonus_serializer import ConstantsSerializer
from base.views.bonus_view import BonusViewGenericListView
from base.views.utils import BaseGenericListView, delete_props


class ConstantLineViewGenericListView(BaseGenericListView):
    _model = Constant
    _param_entity = 'constant'
    _serialize = ConstantsSerializer


def save_constant_item(constant_data):
    constant = Constant.objects.filter(Year=constant_data['Year'], Month=constant_data['Month']).first()
    constant.PersPart = constant_data['PersPart']
    constant.LeadMultiplier = constant_data['LeadMultiplier']
    constant.extMultiplier = constant_data['extMultiplier']
    return constant_data


class ConstantView(APIView, ConstantLineViewGenericListView):
    def post(self, request):
        constant_item = request.data

        if isinstance(constant_item, list):
            for constant in constant_item:
                save_constant_item(constant)
            constants = Constant.objects.all()
            serialize = ConstantsSerializer(constants, many=True)
            return JsonResponse({"result": True, "items": serialize.data})
        else:
            constant = save_constant_item(constant_item)
            serialize = ConstantsSerializer(constant)
            return JsonResponse({"result": True, "item": serialize.data})


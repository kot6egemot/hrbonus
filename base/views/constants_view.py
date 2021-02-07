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


class ConstantView(APIView, ConstantLineViewGenericListView):
    pass

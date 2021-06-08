from rest_framework.views import APIView

from base.models import DayliReports
from base.serializers.bonus_serializer import DayliReportsSerializer
from base.views.utils import BaseGenericListView


class DayliReportsGenericListView(BaseGenericListView):
    _model = DayliReports
    _param_entity = 'daily_report'
    _serialize = DayliReportsSerializer
    _hide_columns = ['ID']


class DailyReportsView(DayliReportsGenericListView, APIView):
    pass

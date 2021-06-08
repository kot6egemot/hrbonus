from rest_framework.views import APIView

from base.models import DailyReports
from base.serializers.bonus_serializer import DayliReportsSerializer
from base.views.utils import BaseGenericListView


class DailyReportsGenericListView(BaseGenericListView):
    _model = DailyReports
    _param_entity = 'daily_report'
    _serialize = DayliReportsSerializer
    _hide_columns = ['ID']


class DailyReportsView(DailyReportsGenericListView, APIView):
    pass

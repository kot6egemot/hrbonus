from django.urls import path
from base.views.auth_view import ApiLoginView, UserProfileView
from base.views.bonus_view import BonusView, BonusLineView, BlockBonusView
from base.views.constants_view import ConstantView
from base.views.daily_reports import DailyReportsView
from base.views.download_csv_view import DownloadCSVView, DailyCSVView
from base.views.individual_changes_view import IndividualChangesView, IndividualLineView, IndividualPositionView, \
    IndividualPositionDependView, IndividualCreateDependView
from base.views.lines_view import LinesView
from base.views.navigation_view import NavigationView
from base.views.utils import UpdateModelField

urlpatterns = [
                  path('login', ApiLoginView.as_view(), name='login'),
                  path('logout', ApiLoginView.as_view(), name='logout'),
                  path('user', UserProfileView.as_view(), name='user'),
              ] + \
              [
                  path('bonus', BonusView.as_view(), name='bonus'),
                  path('bonus_linefk', BonusLineView.as_view(), name='bonus_linefk'),
                  path('bonus_block', BlockBonusView.as_view(), name='bonus_block'),

                  path('line', LinesView.as_view(), name='lines'),
              ] + \
              [
                  path('constant', ConstantView.as_view(), name='constant'),
              ] + \
              [
                  path('individual_change', IndividualChangesView.as_view(), name='individual_change'),
                  path('individual_change_linefk', IndividualLineView.as_view(), name='individual_change_linefk'),
                  path('individual_change_positionfk', IndividualPositionView.as_view(),
                       name='individual_change_positionfk'),
                  path('individual_change_positionfk_depend', IndividualPositionDependView.as_view(),
                       name='individual_change_positionfk_depend'),
                  path('individual_create', IndividualCreateDependView.as_view(), name='individual_create'),
              ] + \
              [
                  path('download_csv', DownloadCSVView.as_view(), name='download_csv'),
              ] + \
              [
                  path('navigation', NavigationView.as_view(), name='navigation'),
              ] + \
              [
                  path('daily_report', DailyReportsView.as_view(), name='daily_reports'),
              ] + \
              [
                  path('update_field/<str:entity>/<int:id>', UpdateModelField.as_view(), name='update_model_field'),
              ] + \
              [
                  path('reports/<str:entity>', DailyCSVView.as_view(), name='update_csv'),
              ]

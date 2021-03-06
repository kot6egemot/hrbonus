from django.urls import path
from base.views.auth_view import ApiLoginView, UserProfileView
from base.views.bonus_view import BonusView, BonusLineView
from base.views.constants_view import ConstantView
from base.views.download_scv_view import DownloadCSVView
from base.views.individual_changes_view import IndividualChangesView, IndividualLineView, IndividualPositionView, \
    IndividualPositionDependView, IndividualCreateDependView
from base.views.lines_view import LinesView

urlpatterns = [
                  path('login', ApiLoginView.as_view(), name='login'),
                  path('logout', ApiLoginView.as_view(), name='logout'),
                  path('user', UserProfileView.as_view(), name='user'),
              ] + \
              [
                  path('bonus', BonusView.as_view(), name='bonus'),
                  path('bonus_linefk', BonusLineView.as_view(), name='bonus_linefk'),

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
              ]

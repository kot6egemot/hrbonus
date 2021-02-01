from django.urls import path
from base.views.auth_view import ApiLoginView, UserProfileView
from base.views.bonus_view import BonusView, BonusLineView
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
              ]

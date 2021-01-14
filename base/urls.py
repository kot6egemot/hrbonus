from django.urls import path
from base.auth_view import ApiLoginView, UserProfileView
from base.bonus_view import TestQueryView

urlpatterns = [
                  path('login', ApiLoginView.as_view(), name='login'),
                  path('logout', ApiLoginView.as_view(), name='logout'),
                  path('user', UserProfileView.as_view(), name='user'),
              ] + \
              [
                  path('query_test', TestQueryView.as_view(), name='test_query')
              ]

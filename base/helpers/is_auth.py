from django.http import HttpResponse
from rest_framework import permissions


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        else:
            entity = view._param_entity
            if entity in ['bonus', 'line', 'constant', 'individual_change', 'cvs_upload']:
                if not request.user.role.rule[view._param_entity]['view'] and request.method == 'GET':
                   return False
                if not request.user.role.rule[view._param_entity]['edit'] and request.method == 'POST':
                   return False
                if not request.user.role.rule[view._param_entity]['add'] and request.method == 'PUT':
                   return False
                if not request.user.role.rule[view._param_entity]['delete'] and request.method == 'DELETE':
                   return False
        return super(IsAuthenticated, self).has_permission(request, view)


from django.contrib.auth.models import User
from rest_framework import serializers

from base.views.utils import BaseGenericListView


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'id')

    def get_role(self, instance):
        return instance.role.rule


class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

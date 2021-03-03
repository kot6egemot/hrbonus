from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from base.models import UserRole
from base.serializers.auth_serializer import UserSerializer, UserViewSerializer
from base.views.utils import BaseGenericListView


class UserProfileView(APIView):

    def get(self, request):
        user = request.user
        serialize = UserSerializer(user)
        return JsonResponse({"result": True, 'user': serialize.data})


class ApiLoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            try:
                user.auth_token.delete()
            except Exception as e:
                pass
            Token.objects.create(user=user)

            user_serialize = UserSerializer(user)
            user_data = user_serialize.data
            user_data['token'] = user.auth_token.key
            response = JsonResponse({"result": True, "user": user_data})
            return response
        else:
            return JsonResponse({"error": "Wrong Credentials"})

class UsersViewGenericListView(APIView):
    def get(self, request):
        if user_id := request.GET.get('id'):
            serialize = UserSerializer(User.objects.get(id=user_id))
            return JsonResponse(
                {
                    "result": True,
                    "users": serialize.data,
                }
            )
        entity = User.objects.all()
        columns = [
            {'text': 'Действия', 'value': 'Actions'},
            {'text': 'Персональный номер', 'value': 'id'},
            {'text': 'username', 'value': 'username'},
            {'text': 'first_name', 'value': 'first_name'},
            {'text': 'last_name', 'value': 'last_name'}
        ]

        serialize = UserViewSerializer(entity, many=True)

        return JsonResponse(
            {
                "result": True,
                "users": serialize.data,
                'columns': columns,
            }
        )

    # {"bonus": {"view": false, "edit": true, "delete": true, "add": true},
    #  "line": {"view": true, "edit": true, "delete": true, "add": true},
    #  "constant": {"view": true, "edit": true, "delete": true, "add": false},
    #  "individual_change": {"view": false, "edit": true, "delete": true, "add": true},
    #  "cvs_upload": {"view": true, "edit": true, "delete": true, "add": true},
    #  "users": {"view": false, "edit": true, "delete": true, "add": false}}

    def put(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        data_role = request.data.get('role')

        new_user = User.objects.create_user(username=username, password=password)
        new_user.save()

        role = UserRole()
        role.user_id = new_user

        rule_of_role = {}
        for entity in data_role:
            rule_of_role[entity["entity"]] = {}
            for r in entity["rules"]:
                rule_of_role[entity["entity"]][r["name"]] = r["value"]
        role.rule = rule_of_role
        role.save()

        serialize = UserViewSerializer(new_user)
        return JsonResponse(
            {
                "result": True,
                "item": serialize.data,
            }
        )

    def post(self, request):
        id = request.data.get('id')
        username = request.data.get('username')
        password = request.data.get('password')
        data_role = request.data.get('role')

        user = User.objects.get(id=id)
        if password:
            user.set_password(password)
        user.username = username
        user.save()
        try:
            user.auth_token.delete()
        except Exception as e:
            pass

        role = user.role
        role.rule = {}

        rule_of_role = {}
        for entity in data_role:
            print(entity)
            rule_of_role[entity["entity"]] = {}
            for r in entity["rules"]:
                rule_of_role[entity["entity"]][r["name"]] = r["value"]
        role.rule = rule_of_role
        role.save()

        serialize = UserSerializer(user)
        return JsonResponse(
            {
                "result": True,
                "item": serialize.data,
            }
        )

    def delete(self, request):
        id = request.data.get('id')
        user = User.objects.get(id=id)
        user.delete()

        return JsonResponse(
            {
                "result": True,
            }
        )

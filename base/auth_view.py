from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from base.serializers.auth_serializer import UserSerializer


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
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)

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

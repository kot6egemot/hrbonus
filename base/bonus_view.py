from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Bonuses_Summary


class TestQueryView(APIView):
    test_query = Bonuses_Summary.objects.all()
    print(test_query)

    def get(self, request):
        return JsonResponse({"result": True})


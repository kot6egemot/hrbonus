from django.http import JsonResponse
from rest_framework.views import APIView

from base.models import Bonuses_Summary
from base.serializers.bonus_serializer import BonusSerializer


class BonusView(APIView):

    def get(self, request):
        bonuses = Bonuses_Summary.objects.all()
        fields = Bonuses_Summary.get_model_fields()
        headers = [{'text': field, 'value': field} for field in fields] + [{'text': 'Actions', 'value': 'Actions'}]
        serialize = BonusSerializer(bonuses, many=True)
        return JsonResponse({"result": True, "_bonus": serialize.data, "__bonus": serialize.data, 'bonus_headers': headers})


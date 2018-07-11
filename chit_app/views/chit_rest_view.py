from rest_framework import views, response
from chit_app.serializers import *
from chit_app.models import *

class ChitListRestView(views.APIView):

    def get(self, request, **kwargs):
        chits = Chit.objects.all().filter(user__id = request.user.id)
        chits = ChitlistSerializer(chits, many=True)
        return response.Response(data = chits.data)
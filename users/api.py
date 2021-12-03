from simulations.models import Membership, Simulation
from users.serializer import SearchUserSerialize
from .models import CustomUser
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView


@permission_classes((AllowAny, ))
class SearchUserSerializer(APIView):
    def post(self, request):
        owner_email = self.request.META["HTTP_OWNEREMAIL"]
        input = request.data["input"]

        try:
            target_simulation = Simulation.objects.get(name=self.request.META["HTTP_SIMULATIONNAME"])
        except:
            target_simulation = None

        try:
            membership = Membership.objects.get(
                user=CustomUser.objects.get(email=owner_email),
                simulation=target_simulation
            )
        except:
            membership = None

        if membership is not None and target_simulation is not None:
            email_search_user = list(CustomUser.objects.filter(email__contains=input))
            full_name_search_user = list(CustomUser.objects.filter(first_name__contains=input) or CustomUser.objects.filter(last_name__contains=input))

            final_users_list = list(dict.fromkeys(email_search_user + full_name_search_user))

            serializer = SearchUserSerialize(final_users_list, many=True)

            return JsonResponse({"users": serializer.data}, safe=False, status=status.HTTP_200_OK)

        message = ""
        if membership is None:
            message += "Permission denied."

        if target_simulation is None:
            message += "Simulation not found."

        return JsonResponse({"message": message}, safe=False, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status, permissions
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import OdWeightId, CasingTubing, Simulation, Membership, Role
from .serializers import OdWeightIdSerializer, CasingTubingSerializerGet, FluidSerializer, DesignSerializer, CasingTubingSerializerPost, CasingTubingSerializerDelete, CasingTubingSerializerPut, SimulationListSerialize, MembershipListFields, MembershipListSerialize, SimulationListFields, SimulationUpdateSerialize, GetSimulationSerialize
from users.models import CustomUser

@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_list_of_simulations_apiview(request):
    list_of_simulation_info = []
    simulations = list(Simulation.objects.all())

    for i in range(0, len(simulations)):
        list_of_simulation_info.append(SimulationListFields(
            name=simulations[i].name,
            time_created=simulations[i].created_at,
            user_email=Membership.objects.get(simulation=simulations[i], is_user_creator=True).user.email,
            url=simulations[i].url,
        ))

    serializer = SimulationListSerialize(list_of_simulation_info, many=True)
    return Response({"simulations": serializer.data}, status=status.HTTP_200_OK)


# class SimulationListSerializer(APIView):
#     def get(self, request):
#         list_of_simulation_info = []
#         simulations = list(Simulation.objects.all())
#
#         for i in range(0, len(simulations)):
#             list_of_simulation_info.append(SimulationListFields(
#                 name=simulations[i].name,
#                 time_created=simulations[i].created_at,
#                 user_email=Membership.objects.get(simulation=simulations[i], is_user_creator=True).user.email,
#                 url=simulations[i].url,
#             ))
#
#         serializer = SimulationListSerialize(list_of_simulation_info, many=True)
#
#         return JsonResponse({"simulations": serializer.data}, safe=False, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class SimulationUpdateSerializer(APIView):
    def post(self, request):
        serializer = SimulationUpdateSerialize(data=request.data)
        message = []
        owner_email = self.request.META["HTTP_OWNEREMAIL"]
        try:
            owner_user = CustomUser.objects.get(email=owner_email)
        except:
            return JsonResponse({"message": "Permission denied."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_simulation = Simulation.objects.get(url=self.request.META["HTTP_URL"])
        except:
            return JsonResponse({"message": "Simulation not found."})

        if serializer.is_valid():

            url = ""
            description = ""
            name = ""
            visibility = ""

            if serializer.data.get("visibility"):
                visibility = serializer.data.get("visibility")
            else:
                visibility = target_simulation.visibility

            if serializer.data.get("url"):
                url = serializer.data.get("url")
            else:
                url = target_simulation.url

            if serializer.data.get("name"):
                name = serializer.data.get("name")
            else:
                name = target_simulation.name

            if serializer.data.get("description"):
                description = serializer.data.get("description")
            else:
                description = target_simulation.description

            if target_simulation is not None:
                target_simulation.url = url
                target_simulation.name = visibility
                target_simulation.description = description
                target_simulation.name = name
                target_simulation.save()
                return JsonResponse({"message": "Simulation updated successfully."})
            else:
                return JsonResponse({"message": "Target simulation does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        else:

            for i in range(0, len(list(serializer.errors.values()))):
                for j in list(serializer.errors.values())[i]:
                    if j not in message:
                        message.append(str(j))
            message_string = ""
            for i in range(0, len(message)):
                message_string += message[i]
            return JsonResponse({"message": message})


@permission_classes((AllowAny, ))
class GetSimulationSerializer(APIView):
    def post(self, request):
        message = ""
        owner_email = self.request.META["HTTP_OWNEREMAIL"]

        try:
            target_simulation = Simulation.objects.get(url=self.request.META["HTTP_URL"])
        except:
            target_simulation = None

        try:
            owner_user = CustomUser.objects.get(email=owner_email)
            is_owner_membership_exists = Membership.objects.get(user=owner_user, simulation=target_simulation)
        except:
            is_owner_membership_exists = None

        simulation = GetSimulationSerialize(target_simulation)
        memberships = Membership.objects.filter(simulation=target_simulation)

        if memberships:
            list_of_memberships = []
            for x in memberships:
                list_of_memberships.append(
                    MembershipListFields(
                        user_email=x.user.email,
                        role=x.role.name,
                    )
                )

                mems = MembershipListSerialize(list_of_memberships, many=True)
        else:
            mems = None

        if is_owner_membership_exists is not None:
            if target_simulation is not None:
                return JsonResponse(
                    {
                        "message": message,
                        "simulation": simulation.data,
                        "membership": mems.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return JsonResponse({"message": "Simulation not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"message": "Permission denied."}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))
class RemoveSimulationSerializer(APIView):
    def post(self, request):
        owner_email = self.request.META["HTTP_OWNEREMAIL"]
        try:
            target_simulation = Simulation.objects.get(url=self.request.META["HTTP_URL"])
        except:
            target_simulation = None

        try:
            owner_user = CustomUser.objects.get(email=owner_email)
            is_owner_membership_exists = Membership.objects.get(user=owner_user, simulation=target_simulation)
        except:
            is_owner_membership_exists = None

        if is_owner_membership_exists is not None:
            if target_simulation is not None:
                target_simulation.delete()
                return JsonResponse({"message": "Simulation removed successfully."}, status=status.HTTP_200_OK)
            return JsonResponse({"message": "Simulation not found.."}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({"message": "Permission denied."}, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class GetSimulationMembersSerializer(APIView):
    def post(self, request):

        owner_email = self.request.META["HTTP_OWNEREMAIL"]

        try:
            target_simulation = Simulation.objects.get(url=self.request.META["HTTP_URL"])
        except:
            target_simulation = None

        try:
            owner_user = CustomUser.objects.get(email=owner_email)
            is_owner_membership_exists = Membership.objects.get(user=owner_user, simulation=target_simulation)
        except:
            return JsonResponse({"message": "permission denied."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            memberships = Membership.objects.filter(simulation=target_simulation)

            if memberships:
                list_of_memberships = []
                for x in memberships:
                    list_of_memberships.append(
                        MembershipListFields(
                            user_email=x.user.email,
                            role=x.role.name,
                        )
                    )

                    mems = MembershipListSerialize(list_of_memberships, many=True)

                return JsonResponse(
                    {
                        "message": "Simulation find successfully.",
                        "membership": mems.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return JsonResponse(
                    {
                        "message": "Simulation find successfully.",
                        "membership": ""
                    },
                    status=status.HTTP_200_OK
                )

        except:
            return JsonResponse({"message": "Simulation not found."}, status=status.HTTP_204_NO_CONTENT)


@permission_classes((AllowAny, ))
class MemberShipSaveSerializer(APIView):
    def post(self, request):

        role = Role.objects.filter(name=request.data["role"]).first()
        owner_email = self.request.META["HTTP_OWNEREMAIL"]
        target_user_email = request.data["email"]

        try:
            target_simulation = Simulation.objects.get(name=self.request.META["HTTP_SIMULATIONNAME"])
        except:
            target_simulation = None

        try:
            target_user = CustomUser.objects.get(email=target_user_email)
            Membership.objects.get(simulation=target_simulation, user=target_user, role=role)
            return JsonResponse({"message": "This membership is already exists."}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            try:
                membership = Membership.objects.get(
                    user=CustomUser.objects.get(email=owner_email),
                    simulation=target_simulation
                )
            except:
                membership = None

            try:
                user = CustomUser.objects.get(email=request.data["email"])
            except:
                user = None

            if membership is not None and user is not None:
                Membership.objects.create(simulation=target_simulation, user=user, role=role)
                return JsonResponse({"message": "User was added successfully."}, safe=False,
                                    status=status.HTTP_200_OK)

            message = ""
            if user is None:
                message += "Target user not found."

            if membership is None:
                message += "Permission denied."

            if target_simulation is None:
                message += "Simulation not found."
            return JsonResponse({"message": message}, safe=False, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))
class RemoveMembershipSerializer(APIView):
    def post(self, request):

        owner_email = self.request.META["HTTP_OWNEREMAIL"]
        target_user_email = request.data["email"]

        try:
            target_simulation = Simulation.objects.get(url=self.request.META["HTTP_URL"])
        except:
            target_simulation = None

        try:
            owner_membership = Membership.objects.get(
                user=CustomUser.objects.get(email=owner_email),
                simulation=target_simulation
            )
        except:
            owner_membership = None

        try:
            user = CustomUser.objects.get(email=request.data["email"])
        except:
            user = None

        try:
            target_membership = Membership.objects.get(simulation=target_simulation, user=CustomUser.objects.get(email=target_user_email))
        except:
            target_membership = None

        if target_membership is not None:
            target_membership.delete()
            return JsonResponse({"message": "User was removed successfully."}, safe=False,
                                status=status.HTTP_200_OK)

        message = ""
        if user is None:
            message += "Target user not found."

        if owner_membership is None:
            message += "Permission denied."

        if target_simulation is None:
            message += "Simulation not found."
        if target_membership is None:
            message += "This user has no membership to this simulation."

        return JsonResponse({"message": message}, safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_list_of_od_weight_id_apiview(request):
    all_items = OdWeightId.objects.values("outside_diameter_OD", "inside_diameter_ID", "weight")
    serializer = OdWeightIdSerializer(all_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_list_of_casing_tubing_apiview(request):
    all_items = CasingTubing.objects.values("id", "type", "bottom", "top", "inside_diameter", "outside_diameter", "roughness")
    serializer = CasingTubingSerializerGet(all_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_casing_tubing_apiview(request):
    serializer = CasingTubingSerializerPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        message = []
        for i in range(0, len(list(serializer.errors.values()))):
            for j in list(serializer.errors.values())[i]:
                if j not in message:
                    message.append(str(j))
        print(serializer.error_messages)
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
def update_casing_tubing_apiview(request):
    found_items = []
    updated_items = []
    not_found_items = []
    for i in range(0, len(request.data)):
        try:
            object = CasingTubing.objects.get(id=request.data[i]["id"])
            found_items.append(request.data[i]["id"])
        except:
            not_found_items.append(request.data[i]["id"])
        serializer = CasingTubingSerializerPut(object, data=request.data[i])
        if serializer.is_valid():
            operation = serializer.save()
            if operation:
                updated_items.append(request.data[i]["id"])
        else:
            message = []
            for i in range(0, len(list(serializer.errors.values()))):
                for j in list(serializer.errors.values())[i]:
                    if j not in message:
                        message.append(str(j))
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"Updated items": updated_items, "Found items": found_items, "Not found items": not_found_items},
        status=status.HTTP_200_OK
    )



@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
def delete_casing_tubing_apiview(request):
    found_items = []
    deleted_items = []
    not_found_items = []
    for i in range(0, len(request.data)):
        try:
            object = CasingTubing.objects.get(id=request.data[i]["id"])
            found_items.append(request.data[i]["id"])
        except:
            not_found_items.append(request.data[i]["id"])
        serializer = CasingTubingSerializerDelete(object, data=request.data[i])
        if serializer.is_valid():
            operation = object.delete()
            if operation:
                deleted_items.append(request.data[i]["id"])
        else:
            message = []
            for i in range(0, len(list(serializer.errors.values()))):
                for j in list(serializer.errors.values())[i]:
                    if j not in message:
                        message.append(str(j))
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"Deleted items": deleted_items, "Found items": found_items, "Not found items": not_found_items},
        status=status.HTTP_200_OK
    )



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_design_apiview(request):
    serializer = DesignSerializer(data=request.data)
    if serializer.is_valid():
        print("valid")
        intake_pressure = 0.0
        fluid_over_pump = 0.0
        tdh = 0.0
        free_gas_intake = 0.0

        operation = serializer.save(
            intake_pressure=intake_pressure,
            fluid_over_pump=fluid_over_pump,
            tdh=tdh,
            free_gas_intake=free_gas_intake
        )
        if operation:
            return Response(
                {
                    "intake_pressure": intake_pressure,
                    "fluid_over_pump": fluid_over_pump,
                    "tdh": tdh,
                    "free_gas_intake": free_gas_intake
                 },
                status=status.HTTP_201_CREATED
            )
    else:
        message = []
        for i in range(0, len(list(serializer.errors.values()))):
            for j in list(serializer.errors.values())[i]:
                if j not in message:
                    message.append(str(j))
        print("invalid")
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_fluid_apiview(request):
    serializer = FluidSerializer(data=request.data)
    if serializer.is_valid():
        return Response(status=status.HTTP_201_CREATED)
    else:
        message = []
        for i in range(0, len(list(serializer.errors.values()))):
            for j in list(serializer.errors.values())[i]:
                if j not in message:
                    message.append(str(j))
        print("invalid")
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
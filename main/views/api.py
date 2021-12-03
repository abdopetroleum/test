import json
from django.http import JsonResponse
from simulations.models import Option, Fluid, IPR, Well, Separator
from main.models import Unit
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny
from ..serializers import FluidSerializer, IPRSerializer, WellSerializer, SeparatorSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView


def options(request, fields_names):
    """this method gets a field name and returns the corresponding options

    Args:
        request (GET Request): field

    Returns:
        json array: [id, display_name, value]
    """

    fields_names = fields_names.split(',')
    options = list(Option.objects.filter(field_name__in=fields_names).values('id', 'field_name', 'display_name', 'value'))
    return JsonResponse(options, safe=False)


def units(request, unit_type):
    """Returns units

    Args:
        request (Get Request): unit_type

    Returns:
        json array: [id, display_name]
    """

    units = list(Unit.objects.filter(unit_type=unit_type).values('id', 'display_name'))
    return JsonResponse(units, safe=False)


class IPRCreate(APIView):
    """ this view is just for shows all IPR objects and adds new object.

        Args: request(POST and GET) : IPR

        Return:
    """

    queryset = IPR.objects.all()
    serializer_class = IPRSerializer


    def get(self, request):
        iprs = IPR.objects.all()
        serialzer = IPRSerializer(iprs, many=True)
        return Response(serialzer.data)

    def post(self, request):
        serializer = IPRSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FluidCreate(APIView):
    """this view is just for shows all IPR objects and adds new object.

        Args: request(POST and GET) : IPR

        Return:

    """
    queryset = Fluid.objects.all()
    serializer_class = FluidSerializer

    def get(self, request):
        fluids = Fluid.objects.all()
        serializer = FluidSerializer(fluids, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FluidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WellCreate(APIView):
    """ this view is just for shows all Well objects and adds new object.

        Args: request(POST and GET) : Well

        Return:
    """

    queryset = Well.objects.all()
    serializer_class = WellSerializer


    def get(self, request):
        wells = Well.objects.all()
        serializer = WellSerializer(wells, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WellSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeparatorCreate(APIView):
    """ this view is just for shows all Separator objects and adds new object.

        Args: request(POST and GET) : Separator

        Return:
    """

    queryset = Separator.objects.all()
    serializer_class = SeparatorSerializer


    def get(self, request):
        separators = Separator.objects.all()
        serializer = SeparatorSerializer(separators, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SeparatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_fluid(request, id):

    """ Get fluid object by id.

    Args: request(GET) and id.

    Return:
        JsonResponse : Fluid object
    """
    fluid = Fluid.objects.filter(id=id)
    serializer = FluidSerializer(fluid, many=True)

    if fluid:
        return JsonResponse({'Fluid': serializer.data}, safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message": "Not found this fluid."})


@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_fluid(request, id):
    """ Delete fluid object by id.

    Args: request and id.

    Return:
        Response : Message OR Error.
    """
    try:
        fluid = Fluid.objects.get(id=id)

        fluid.delete()

        return Response({"message": "Fluid deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except ObjectDoesNotExist:
        return JsonResponse({'error': "Not found this fluid."}, safe=False, status=status.HTTP_404_NOT_FOUND)

    except Exception:
        return JsonResponse({'error': 'Something went wrong.'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_ipr(request, id):

    """ get ipr object by id.
    request: GET
    args: request, id
    return: JsonResponse
    """
    ipr = IPR.objects.filter(id=id)
    serializer = IPRSerializer(ipr, many=True)

    if ipr:
        return JsonResponse({'IPR': serializer.data}, safe=False, status=status.HTTP_200_OK)

    else:
        return JsonResponse({"message": "Not found this ipr."})

@api_view(["GET"])
@permission_classes([AllowAny])
def get_well(request, id):

    """ get well object by id.
    request: GET
    args: request, id
    return: JsonResponse
    """
    ipr = Well.objects.filter(id=id)
    serializer = WellSerializer(well, many=True)

    if ipr:
        return JsonResponse({'Well': serializer.data}, safe=False, status=status.HTTP_200_OK)

    else:
        return JsonResponse({"message": "Not found this ipr."})

@api_view(["GET"])
@permission_classes([AllowAny])
def get_separator(request, id):

    """ get separator object by id.
    request: GET
    args: request, id
    return: JsonResponse
    """
    ipr = Separator.objects.filter(id=id)
    serializer = SeparatorSerializer(well, many=True)

    if ipr:
        return JsonResponse({'Separator': serializer.data}, safe=False, status=status.HTTP_200_OK)

    else:
        return JsonResponse({"message": "Not found this ipr."})


@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_ipr(request, id):
    """ Delete ipr object by id.
     Args: request, id
    return: JsonResponse
    """
    try:

        ipr = IPR.objects.get(id=id)
        ipr.delete()
        return Response({"message": "IPR deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except ObjectDoesNotExist:
        return JsonResponse({'error': "Not found this ipr."}, safe=False, status=status.HTTP_404_NOT_FOUND)

    except Exception:
        return JsonResponse({'error': 'Something went wrong.'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_well(request, id):
    """ Delete well object by id.
     Args: request, id
    return: JsonResponse
    """
    try:

        well = Well.objects.get(id=id)
        well.delete()
        return Response({"message": "Well deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except ObjectDoesNotExist:
        return JsonResponse({'error': "Not found this well."}, safe=False, status=status.HTTP_404_NOT_FOUND)

    except Exception:
        return JsonResponse({'error': 'Something went wrong.'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_separator(request, id):
    """ Delete separator object by id.
     Args: request, id
    return: JsonResponse
    """
    try:

        separator = Separator.objects.get(id=id)
        separator.delete()
        return Response({"message": "Separator deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except ObjectDoesNotExist:
        return JsonResponse({'error': "Not found this separator."}, safe=False, status=status.HTTP_404_NOT_FOUND)

    except Exception:
        return JsonResponse({'error': 'Something went wrong.'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateIprById(UpdateAPIView):
    """ this method gets Ipr id and then update it object

    """

    queryset = IPR.objects.all()
    serializer_class = IPRSerializer
    lookup_field = 'id'


class UpdateFluidById(UpdateAPIView):
    """ this method gets Fluid id and then update it object

    """
    queryset = Fluid.objects.all()
    serializer_class = FluidSerializer
    lookup_field = 'id'


class UpdateWellById(UpdateAPIView):
    """ this method gets Well id and then update it object

    """
    queryset = Well.objects.all()
    serializer_class = WellSerializer
    lookup_field = 'id'


class UpdateSeparatorById(UpdateAPIView):
    """ this method gets Separator id and then update it object

    """
    queryset = Separator.objects.all()
    serializer_class = SeparatorSerializer
    lookup_field = 'id'


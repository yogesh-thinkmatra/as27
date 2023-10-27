from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ai.serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import os
from .models import *
from django.forms.models import model_to_dict
from django.conf import settings
from rest_framework.decorators import api_view
from datetime import datetime,timedelta

class ElectricianView(APIView):
    try:
        def post(self, request, format=None):
            serializer = ElectricianSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            electrician = serializer.save()
            return Response({"msg": 'Electrician has been created', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

        def get(self, request, pk=None, format=None):
            
            id = pk
            
            if id is not None:
                electrician = Electricians.objects.get(id=id)
                serializer = ElectricianSerializer(electrician)
                return Response({"msg": 'Data Fetched', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

            electricians = Electricians.objects.filter(status=True)
            serializer = ElectricianSerializer(electricians, many=True)
            return Response({"msg": 'Data Fetched', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

        def put(self, request, pk, format=None):
            id = pk
            module = Electricians.objects.get(id=id)
            serializer = ElectricianSerializer(module, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"msg": 'Data updated', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

        def patch(self, request, pk, format=None):
            id = pk
            module = Electricians.objects.get(id=id)
            serializer = ElectricianSerializer(module, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"msg": 'Data updated partially', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

        def delete(self, request, pk, format=None):
            id = pk
            module = Electricians.objects.get(id=id)
            serializer = ElectricianSerializer(module)
            print(serializer.data)
            module.status=False
            module.save()
            return Response({
                "msg": "Data has been deleted",
                "data":None,
                "status_code":200
            }, status=status.HTTP_200_OK)


    except Exception as e:

        print(e)
 


class SitesView(APIView):
    try:
        def post(self, request, format=None):
            serializer = SitesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            site = serializer.save()
            return Response({"msg": 'Sites has been created', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

        def get(self, request, pk=None, format=None):
            
            id = pk
            
            if id is not None:
                Sites = Sites.objects.get(id=id)
                serializer = SitesSerializer(Sites)
                return Response({"msg": 'Data Fetched', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

            sites = Sites.objects.filter(status=True)
            serializer = SitesSerializer(sites, many=True)
            return Response({"msg": 'Data Fetched', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

        def put(self, request, pk, format=None):
            id = pk
            site = Sites.objects.get(id=id)
            serializer = SitesSerializer(site, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"msg": 'Data updated', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

        def patch(self, request, pk, format=None):
            id = pk
            site = Sites.objects.get(id=id)
            serializer = SitesSerializer(site, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"msg": 'Data updated partially', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

        def delete(self, request, pk, format=None):
            id = pk
            site = Sites.objects.get(id=id)
            serializer = SitesSerializer(site)
            site.status=False
            site.save()
            return Response({
                "msg": "Data has been deleted",
                "data":None,
                "status_code":200
            }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)



@api_view(['POST'])
def assign_electricians_to_sites():
    # Get the current date
    current_date = datetime.now().date()

    electricians = Electricians.objects.all()
    sites = Sites.objects.all()

    # Separate grievance and general sites
    grievance_sites = sites.filter(grievance=True)
    general_sites = sites.filter(grievance=False)

    for site in grievance_sites:
        if electricians:
            grievance_electricians = electricians.filter(grievance=True)
            if grievance_electricians:
                for electrician in grievance_electricians:
                    if SitesAllocation.objects.filter(electrician=electrician).count() < 3:
                        SitesAllocation.objects.create(site=site, electrician=electrician)

    for site in general_sites:
        if electricians:
            electrician = electricians.pop(0)
            if SitesAllocation.objects.filter(electrician=electrician).count() < 3:
                SitesAllocation.objects.create(site=site, electrician=electrician)

    return Response({
                "msg": "Allocation Done",
                "data":None,
                "status_code":200
            }, status=status.HTTP_200_OK)
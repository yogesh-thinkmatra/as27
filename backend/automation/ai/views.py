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
    def post(self, request, format=None):
        try:
            serializer = ElectricianSerializer(data=request.data)
            if serializer.is_valid():
                electrician = serializer.save()
                return Response({"msg": 'Electrician has been created', "status": 200, "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"msg": 'An error occurred', "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk=None, format=None):
        try:
            if pk is not None:
                electrician = Electricians.objects.get(id=pk)
                serializer = ElectricianSerializer(electrician)
                return Response({"msg": 'Data Fetched', "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)

            electricians = Electricians.objects.filter(status=True)
            serializer = ElectricianSerializer(electricians, many=True)
            return Response({"msg": 'Data Fetched', "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        except Electricians.DoesNotExist:
            return Response({"msg": 'Electrician not found', "status": 404}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"msg": 'An error occurred', "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            electrician = Electricians.objects.get(id=pk)
            serializer = ElectricianSerializer(electrician, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": 'Data updated', "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Electricians.DoesNotExist:
            return Response({"msg": 'Electrician not found', "status": 404}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"msg": 'An error occurred', "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk, format=None):
        try:
            electrician = Electricians.objects.get(id=pk)
            serializer = ElectricianSerializer(electrician, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": 'Data updated partially', "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Electricians.DoesNotExist:
            return Response({"msg": 'Electrician not found', "status": 404}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"msg": 'An error occurred', "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        try:
            electrician = Electricians.objects.get(id=pk)
            serializer = ElectricianSerializer(electrician)
            electrician.status = False
            electrician.save()
            return Response({"msg": "Data has been deleted", "data": None, "status_code": 200}, status=status.HTTP_200_OK)
        except Electricians.DoesNotExist:
            return Response({"msg": 'Electrician not found', "status": 404}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"msg": 'An error occurred', "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SitesView(APIView):
    try:
        def get_assigned_electrician(self, request, pk, format=None):
            try:
                site = Sites.objects.get(pk=pk)
                try:
                    allocation = SitesAllocation.objects.get(site=site)
                    electrician = allocation.electrician
                    electrician_serializer = ElectricianSerializer(electrician)
                    return Response({
                        "msg": "Electrician assigned to the site",
                        "status": 200,
                        "data": electrician_serializer.data
                    }, status=status.HTTP_200_OK)
                except SitesAllocation.DoesNotExist:
                    return Response({
                        "msg": "No electrician assigned to this site",
                        "status": 200,
                        "data": None
                    }, status=status.HTTP_200_OK)
            except Sites.DoesNotExist:
                return Response({
                    "msg": "Site not found",
                    "status": 404,
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)



        def post(self, request, format=None):
            serializer = SitesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            site = serializer.save()
            return Response({"msg": 'Sites has been created', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

        def get(self, request, pk=None, format=None):
            
            id = pk
            
            if id is not None:
                sites = Sites.objects.get(id=id)
                serializer = SitesSerializer(sites)
                return Response({"msg": 'Data Fetched', "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

            site = Sites.objects.filter(status=True)
            serializer = SitesSerializer(site, many=True)
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


@api_view(['get'])
def assign_electricians_to_sites(request):
    electricians = Electricians.objects.all()
    sites = Sites.objects.all()

    grievance_sites = sites.filter(grievance=True)
    general_sites = sites.filter(grievance=False)

    for site in grievance_sites:
        if electricians:
            available_electricians = electricians.filter(cities__contains=[site.city]).filter(grievance=True)
            if available_electricians:
                for electrician in available_electricians:
    
                    if not SitesAllocation.objects.filter(site=site).exists():
                        if SitesAllocation.objects.filter(electrician=electrician).count() < 3:
                            SitesAllocation.objects.create(site=site, electrician=electrician)

    for site in general_sites:
        if electricians:
            available_electricians = electricians.filter(cities__contains=[site.city]).filter(grievance=False)
            if available_electricians:
                for electrician in available_electricians:
                   
                    if not SitesAllocation.objects.filter(site=site).exists():
                        if SitesAllocation.objects.filter(electrician=electrician).count() < 3:
                            SitesAllocation.objects.create(site=site, electrician=electrician)

    pending_sites = sites.filter(sitesallocation__isnull=True)
    for site in pending_sites:
        if electricians:
            available_electricians = electricians.filter(cities__contains=[site.city])
            if available_electricians:
                electrician = available_electricians.first()
             
                if not SitesAllocation.objects.filter(site=site).exists():
                    if SitesAllocation.objects.filter(electrician=electrician).count() < 3:
                        SitesAllocation.objects.create(site=site, electrician=electrician)

    return Response({
        "msg": "Auto Assigned Done",
        "data": None,
        "status_code": 200
    }, status=status.HTTP_200_OK)

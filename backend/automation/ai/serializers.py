from dataclasses import fields
from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import *
import re
import ast

class CityListField(serializers.ListField):
    def to_internal_value(self, data):
        if isinstance(data, list):
            return data
        if isinstance(data, str):
            try:
                # Safely evaluate the string as a Python list
                city_list = ast.literal_eval(data)
                if isinstance(city_list, list):
                    return city_list
            except (ValueError, SyntaxError):
                pass
        self.fail('invalid', format='city')

    def to_representation(self, value):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            try:
                # Safely evaluate the string as a Python list
                city_list = ast.literal_eval(value)
                if isinstance(city_list, list):
                    return [city.strip() for city in city_list]
            except (ValueError, SyntaxError):
                pass
        self.fail('invalid', format='city')






class ElectricianSerializer(serializers.ModelSerializer):
    allotment_count = serializers.SerializerMethodField()
    cities = CityListField(required=False)
    class Meta:
        model = Electricians
        fields  ='__all__'
    def validate(self, data):
        instance = self.instance   
        phone_number = data.get('phone_number')
        if instance:
            if (instance.phone_number==phone_number and Electricians.objects.filter(phone_number=phone_number).filter(status=True).exists()):  
                return data
            if instance and Electricians.objects.filter(phone_number=phone_number).filter(status=True).exists():
                raise serializers.ValidationError('A record with this phone number already exists.')
        if Electricians.objects.filter(phone_number=phone_number).filter(status=True).exists():
            raise serializers.ValidationError('A record with this phone number already exists.')
        return data
    def get_allotment_count(self, obj):
        return SitesAllocation.objects.filter(electrician=obj).count()



class SitesSerializer(serializers.ModelSerializer):
    electrician = serializers.SerializerMethodField()
    class Meta:
        model = Sites
        fields  ='__all__'
    def validate(self, data):
       
        return data
    def get_electrician(self, obj):
        allocation=SitesAllocation.objects.filter(site=obj).filter(status=True).last()
        if allocation is None:
            return None
        electrician=allocation.electrician.name
        return electrician
    


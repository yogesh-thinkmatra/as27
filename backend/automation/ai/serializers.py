from dataclasses import fields
from rest_framework import serializers
from ai.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import *
import re




class ElectricianSerializer(serializers.ModelSerializer):

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
    


class SitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sites
        fields  ='__all__'
    def validate(self, data):
       
        return data
    
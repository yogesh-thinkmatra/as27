import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db.models.signals import post_save,pre_save



class BaseModel(models.Model):
    id=models.AutoField(primary_key=True,editable=False)
    status=models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    
    class Meta:
        abstract=True # Set this model as Abstract



class Electricians(BaseModel):
    class Meta:
            db_table = 'electricians'
        
    name=models.CharField(max_length=50,blank=True,null=False)
    phone_number=models.CharField(max_length=50,blank=True,null=False)
    grievance=models.BooleanField(default=False,blank=True,null=False)
    cities = models.TextField(blank=True, default='[]')
    
    def __str__(self):
        return self.name
    
class Sites(BaseModel):
    class Meta:
            db_table = 'sites'

    name=models.CharField(max_length=50,blank=True,null=False)
    phone_number=models.CharField(max_length=50,blank=True,null=False)
    city=models.CharField(max_length=50,blank=True,null=False)
    installation_date=models.DateField(blank=True,null=False)
    grievance=models.BooleanField(default=False,blank=True,null=False)
    
    def __str__(self):
        return self.name
    
class SitesAllocation(BaseModel):
    class Meta:
            db_table = 'sites_allocation'

    site=models.ForeignKey(Sites,blank=True,null=True, on_delete=models.SET_NULL)
    electrician=models.ForeignKey(Electricians,blank=True,null=True, on_delete=models.SET_NULL)

    
    def __str__(self):
        return self.name
    

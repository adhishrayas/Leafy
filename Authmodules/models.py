import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
 
TYPES = (
    (1,'VENDOR'),
    (2,'BUYER'),
)

class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    Type = models.IntegerField(choices=TYPES,default=False,null=False)
    username = models.CharField(max_length=255,blank=False,unique=True)
    password = models.CharField(max_length=255,blank=False)
    Profile_pic = models.ImageField(blank = True,null = True,upload_to='profiles/')
    Petal_credits = models.FloatField(default = 0)
    email = models.EmailField(blank=False)
    Phone_no = models.IntegerField(blank=True,null=True)
    Verified = models.BooleanField(default = False)
    
    def __str__(self):
        return self.username
    

class Address(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    active = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank = True,null = True)
    Address_line1 = models.CharField(max_length=255,blank=True,null=True)
    Address_line2 = models.CharField(max_length=255,blank=True,null=True)
    City = models.CharField(max_length=255,blank=True,null=True)
    State = models.CharField(max_length=255,blank=True,null=True)
    Pin_code = models.IntegerField(blank=True,null=True)

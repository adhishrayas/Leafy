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
    
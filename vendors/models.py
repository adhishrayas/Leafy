import uuid
from django.db import models
from Authmodules.models import CustomUser
# Create your models here.
class Vendors(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    User = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Name = models.CharField(max_length=255,blank=False,null = False)
    Address_line = models.CharField(max_length=255,blank=False,null = False)
    City = models.CharField(max_length=255,blank=False,null=False)
    State = models.CharField(max_length=255,blank=False,null=False)
    Pin_code = models.IntegerField(max_length =6,blank = False,null=False)
    Contact_no = models.IntegerField(max_length=10,blank=False,null = False)
    Shop_icon = models.ImageField(blank=True,null=True,upload_to= 'shop_icons/')
    Customer_no = models.IntegerField(default=0)
    
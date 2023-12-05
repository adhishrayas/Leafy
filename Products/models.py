import uuid
from django.db import models
from vendors.models import Vendors
# Create your models here.

class Products(models.Model):

    id = models.UUIDField(
        editable=False,
        primary_key=True,
        default=uuid.uuid4
    )
    Name = models.CharField(max_length=255,blank=False)
    Vendor = models.ForeignKey(Vendors,on_delete=models.CASCADE)
    Image = models.ImageField(blank=True,null=True,upload_to='products/')
    Price = models.FloatField(blank=False,default=0)
    Date_posted = models.DateField(auto_now_add=True)
    Views = models.IntegerField(default=0)
    Rating = models.FloatField(default=0)

    def __str__(self):
        return self.Name

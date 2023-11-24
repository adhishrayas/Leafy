from django.urls import path,include
from .models import Vendors
from .views import CreateVendorView

app_name = 'Vendors'
urlpatterns = [
    path('vendor_creation/',CreateVendorView.as_view(),name = 'Vendor Creation')
]

from django.urls import path,include
from .views import ProductFeedView,ProductDetailView

urlpatterns = [
    path('Feed/',ProductFeedView.as_view(),name = 'Feed'),
    path('Details/<uuid:pk>',ProductDetailView.as_view(),name = 'Detail')
]

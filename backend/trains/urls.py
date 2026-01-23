from rest_framework_simplejwt.views import TokenObtainPairView
from .views import TrainCreateView, TrainSearchView
from django.urls import path

urlpatterns = [
    path("", TrainCreateView.as_view(), name='train details'),
    path("search/", TrainSearchView.as_view(), name='train search')
]

from rest_framework_simplejwt.views import TokenObtainPairView
from .views import BookingsCreateView, BookingsListView
from django.urls import path

urlpatterns = [
    path("", view=BookingsCreateView.as_view(), name="train booking"),
    path("my/", view=BookingsListView.as_view(), name="list bookings")
]

from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, LoginView, UsersBooked
from django.urls import path

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path("booked-users/", UsersBooked.as_view(), name='booked users')
]


from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema

from .models import User
from bookings.models import Booking
from bookings.serializers import BookingListSerializer
from .serializers import RegisterSerializer, LoginSerializer, UserBooked

# view for register
@extend_schema(tags=['Authentication'])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer 
    
    # anyone can create an account
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
            
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
            
        return Response(
            {
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                },
                "refresh": str(refresh),
                "token": str(refresh.access_token)
            },
            status=status.HTTP_201_CREATED
        )
        
        
# view for login
@extend_schema(tags=['Authentication'])
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    
    # anyone can login to their account
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = request.data.get('email')
        password = request.data.get("password")
        
        user = authenticate(email=email, password=password)
        
        if not user:
            return Response({ "error": "Invalid Credentials" }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "token": str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )
        
@extend_schema(tags=['Users'])
class UsersBooked(generics.ListAPIView):
    serializer_class=UserBooked
    
    def get_queryset(self):
        users = Booking.objects.values_list("user", flat=True)
        return User.objects.filter(id__in=users)
    
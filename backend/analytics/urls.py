from rest_framework_simplejwt.views import TokenObtainPairView
from .views import AnalyticsView
from django.urls import path

urlpatterns = [
    path("top-routes/", view=AnalyticsView.as_view(), name="top routes")
]

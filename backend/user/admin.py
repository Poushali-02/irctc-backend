from django.contrib import admin
from user.models import CustomUserManager, User

# Register your models here.
admin.site.register(User)
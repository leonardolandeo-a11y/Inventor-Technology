from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username","email","is_worker","is_boss","is_staff")
    fieldsets = UserAdmin.fieldsets + ((None,{"fields":("is_worker","is_boss")}),)
    list_filter = ("is_worker", "is_boss", "is_staff", "is_superuser")


from django.contrib import admin
from .models import UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notification']

    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import CustomUser

# Register your models here.

class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'created_at',
                    'updated_at', 'is_admin', 'is_active',
                    'is_staff')
    readonly_fields = ('id', 'created_at', 'updated_at')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(CustomUser, UserAdmin)
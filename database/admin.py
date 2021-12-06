from django.contrib import admin
from. models import *
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'username', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)



class AdminDoorFoldingCost(admin.ModelAdmin):
    list_display = ('user', 'brand', 'color', 'thick', 'price')



# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(DoorFoldingCost, AdminDoorFoldingCost)
admin.site.register(Glasscost)
admin.site.register(OtherCost)


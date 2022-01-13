from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .models import CustomUser, Profile, Region
from django.contrib import admin


class RegionAdmin(admin.ModelAdmin):
    model = Region
    verbose_name = _('region')
    verbose_name_plural = _('regions')
    ordering = ['region']


# admin.site.register(CustomUser)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = _('profile')
    verbose_name_plural = _('profiles')


# Define a new User admin
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    inlines = (ProfileInline,)


# Re-register UserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Region, RegionAdmin)

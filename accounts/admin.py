from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render
from django.urls import path
from django.utils.translation import gettext, gettext_lazy as _

from .models import CustomUser, Profile, Region
from django.contrib import admin


class RegionAdmin(admin.ModelAdmin):
    model = Region
    verbose_name = _('region')
    verbose_name_plural = _('regions')
    ordering = ['region']

    def get_urls(self):
        urls = super().get_urls()
        upload_url = [
            path(
                'upload/',
                self.admin_site.admin_view(self.upload_regions),
                name='upload_from_csv'
            ),
        ]
        return upload_url + urls

    def upload_regions(self, request):
        # TODO write logic
        return render(request, 'admin/base_site.html', {'messages': (_('Regions uploaded from csv.'),)})


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
    search_fields = ('first_name', 'last_name', 'email')
    inlines = (ProfileInline,)


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'full_name',
        'region',
    ]


# Re-register UserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Region, RegionAdmin)

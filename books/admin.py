from django.contrib import admin

from .models import Items


class ItemsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("title", )
    }

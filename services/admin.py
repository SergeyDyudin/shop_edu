from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Purchase, Rent, Invoice


class PurchaseInlineAdmin(admin.StackedInline):
    model = Purchase
    extra = 0
    verbose_name = _('purchase')
    verbose_name_plural = _('purchases')
    readonly_fields = [
        'price'
    ]


class RentInlineAdmin(admin.StackedInline):
    model = Rent
    extra = 0
    verbose_name = _('rent')
    verbose_name_plural = _('rents')
    readonly_fields = [
        'price'
    ]


class InvoiceAdmin(admin.ModelAdmin):
    readonly_fields = [
        'price_total'
    ]
    inlines = [
        PurchaseInlineAdmin,
        RentInlineAdmin
    ]


class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = [
        'price'
    ]


class RentAdmin(admin.ModelAdmin):
    readonly_fields = [
        'price'
    ]


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Rent, RentAdmin)
admin.site.register(Invoice, InvoiceAdmin)

from django.contrib import admin

from .models import Purchases, Rents, Invoices


class PurchasesInlineAdmin(admin.StackedInline):
    model = Purchases
    extra = 0
    verbose_name = 'purchase'
    verbose_name_plural = 'purchases'
    readonly_fields = [
        'price'
    ]


class RentInlineAdmin(admin.StackedInline):
    model = Rents
    extra = 0
    verbose_name = 'rent'
    verbose_name_plural = 'rents'
    readonly_fields = [
        'price'
    ]


class InvoicesAdmin(admin.ModelAdmin):
    readonly_fields = [
        'total_price'
    ]
    inlines = [
        PurchasesInlineAdmin,
        RentInlineAdmin
    ]


class PurchasesAdmin(admin.ModelAdmin):
    readonly_fields = [
        'price'
    ]


class RentsAdmin(admin.ModelAdmin):
    readonly_fields = [
        'price'
    ]


admin.site.register(Purchases, PurchasesAdmin)
admin.site.register(Rents, RentsAdmin)
admin.site.register(Invoices, InvoicesAdmin)

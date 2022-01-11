from django.contrib import admin

from .models import Statuses, Purchases, Rents, Invoices


class PurchasesInlineAdmin(admin.StackedInline):
    model = Purchases
    extra = 0
    verbose_name = 'purchase'
    verbose_name_plural = 'purchases'


class RentInlineAdmin(admin.StackedInline):
    model = Rents
    extra = 0
    verbose_name = 'rent'
    verbose_name_plural = 'rents'


class InvoicesAdmin(admin.ModelAdmin):
    inlines = [
        PurchasesInlineAdmin,
        RentInlineAdmin
    ]


admin.site.register(Statuses)
admin.site.register(Purchases)
admin.site.register(Rents)
admin.site.register(Invoices, InvoicesAdmin)

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .filters import UnpaidOldInvoiceListFilter
from .models import Purchase, Rent, Invoice


class PurchaseInlineAdmin(admin.StackedInline):
    model = Purchase
    extra = 0
    autocomplete_fields = [
        'item',
    ]
    verbose_name = _('purchase')
    verbose_name_plural = _('purchases')
    readonly_fields = [
        'price'
    ]


class RentInlineAdmin(admin.StackedInline):
    model = Rent
    extra = 0
    autocomplete_fields = [
        'item',
    ]
    verbose_name = _('rent')
    verbose_name_plural = _('rents')
    readonly_fields = [
        'price'
    ]


class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'status',
        'price_total'
    ]
    list_filter = [
        'status',
        UnpaidOldInvoiceListFilter
    ]
    readonly_fields = [
        'date_created',
        'price_total'
    ]
    autocomplete_fields = [
        'user_id'
    ]
    inlines = [
        PurchaseInlineAdmin,
        RentInlineAdmin
    ]
    search_fields = [
        'id',
        'user_id__email',
    ]

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            if request.user.is_superuser:
                choices = db_field.get_choices()
                choices.remove(('Оплачен', _('Оплачен')))
                kwargs['choices'] = choices
        return super().formfield_for_choice_field(db_field, request, **kwargs)


class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = [
        'price'
    ]
    autocomplete_fields = [
        'item',
        'invoice',
    ]
    list_display = [
        'item',
        'status_invoice',
        'quantity',
    ]
    search_fields = [
        'item__title'
    ]
    search_help_text = 'Enter item'

    @admin.display(description=_('Status'))
    def status_invoice(self, obj):
        return obj.invoice.status


class RentAdmin(admin.ModelAdmin):
    readonly_fields = [
        'price'
    ]
    autocomplete_fields = [
        'item',
        'invoice',
    ]
    list_display = [
        'item',
        'status_invoice',
        'quantity',
    ]
    search_fields = [
        'item__title'
    ]
    search_help_text = 'Enter item'

    @admin.display(description=_('Status'))
    def status_invoice(self, obj):
        return obj.invoice.status


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Rent, RentAdmin)
admin.site.register(Invoice, InvoiceAdmin)

from django.db import models
from django.db.models import Sum, F, Count, ExpressionWrapper, DurationField
from django.db.models.functions import ExtractDay


class InvoiceManager(models.Manager):

    def get_queryset(self):
        qs = super(InvoiceManager, self).get_queryset()
        return qs
        # return qs.annotate(total=F('purchase__item__price') * F('purchase__quantity'))


class ServiceManager(models.Manager):

    def get_queryset(self):
        qs = super(ServiceManager, self).get_queryset()
        return qs.annotate(purchase_price=F('item__price') * F('quantity'))


class RentManager(models.Manager):

    def get_queryset(self):
        qs = super(RentManager, self).get_queryset()
        return qs.annotate(
            rent_price=F('quantity') * F('daily_payment') * (
                ExtractDay(ExpressionWrapper(F('date_to') - F('date_from'), output_field=DurationField())) + 1
            )
        )

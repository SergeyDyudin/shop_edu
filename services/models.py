from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser
from books.models import Item
from shop_edu import settings


class Invoice(models.Model):

    class InvoiceStatuses(models.TextChoices):
        PAID = 'Оплачен', _('Оплачен')
        UNPAID = 'Ожидает оплаты', _('Ожидает оплаты')
        CANCELED = 'Отменен', _('Отменен')

    user_id = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    status = models.CharField(
        max_length=30,
        choices=InvoiceStatuses.choices,
        default=InvoiceStatuses.UNPAID,
        blank=False,
        verbose_name=_('status')
    )
    date_created = models.DateTimeField(
        _('date created'),
        auto_now_add=True
    )
    status_updated = models.DateTimeField(
        _('status updated'),
        default=timezone.now
    )

    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')
        permissions = [
            ('can_change_status', _('Can change status'))
        ]

    def __str__(self):
        return f'[{self.id}] {self.user_id}'

    @property
    @admin.display(description=_('Total price'))
    def price_total(self):
        total = 0
        for obj in self.purchase_set.all():
            total += obj.price
        for obj in self.rent_set.all():
            total += obj.price
        return total

    def get_final_price_and_currency(self):
        """
        Evaluate final_price = price - currency and new_currency
        :return: (final_price, new_currency)
        """
        max_discount = self.price_total*settings.MAX_DISCOUNT
        bound_price = self.price_total - max_discount
        diff = max_discount - self.user_id.profile.currency
        if diff >= 0:
            return bound_price + diff, 0
        return bound_price, diff*(-1)

    @property
    def user_profile(self):
        return self.user_id.profile


class Service(models.Model):
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE, verbose_name=_('item'))
    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE, verbose_name=_('invoice'))
    quantity = models.PositiveSmallIntegerField(_('quantity'), default=1, blank=False)

    path_template = 'services/item_service.html'

    class Meta:
        abstract = True

    def __str__(self):
        return f'[{self.invoice.status}]-{self.item.title}'

    @property
    def price(self):
        return self.item.price * self.quantity

    def delete(self, using=None, keep_parents=False):
        self.item.count_available += self.quantity
        self.item.save()
        result_delete = super().delete()
        if not self.invoice.purchase_set.exists() and not self.invoice.rent_set.exists():
            self.invoice.delete()
        return result_delete


class Purchase(Service):

    class Meta:
        verbose_name = _('purchase')
        verbose_name_plural = _('purchases')


class Rent(Service):
    date_from = models.DateField(_('Date from'), default=timezone.now)
    date_to = models.DateField(_('Date to'))
    daily_payment = models.PositiveSmallIntegerField(
        _('daily payment'),
        default=50,
        help_text=_('Daily payment'),
        blank=False,
        null=False
    )

    path_template = 'services/item_rent.html'

    class Meta:
        verbose_name = _('rent')
        verbose_name_plural = _('rents')

    @property
    def price(self):
        if not (self.date_to and self.date_from):
            raise ValueError('Date_to or date_from are not specified')
        return self.quantity * ((self.date_to - self.date_from).days + 1) * self.daily_payment

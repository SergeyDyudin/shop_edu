from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser
from books.models import Items


class Invoices(models.Model):

    class InvoiceStatuses(models.TextChoices):
        PAID = 'Оплачен', 'Оплачен'
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

    def __str__(self):
        vL_TEATED = f'[{self.id}-{self.status}]{self.user_id}'
        return vL_TEATED

    @property
    def total_price(self):
        total = 0
        for obj in self.purchases_set.all():
            total += obj.price
        for obj in self.rents_set.all():
            total += obj.price
        return total


class Services(models.Model):
    item = models.ForeignKey(to=Items, on_delete=models.CASCADE, verbose_name=_('item'))
    invoice = models.ForeignKey(to=Invoices, on_delete=models.CASCADE, verbose_name=_('invoice'))
    quantity = models.PositiveSmallIntegerField(_('quantity'), default=1, blank=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'[{self.invoice.status}]-{self.item.title}'

    @property
    def price(self):
        return self.item.price * self.quantity


class Purchases(Services):

    class Meta:
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'


class Rents(Services):
    date_from = models.DateField(_('Date from'), default=timezone.now)
    date_to = models.DateField(_('Date to'))
    daily_payment = models.PositiveSmallIntegerField(
        _('daily payment'),
        default=50,
        help_text=_('Daily payment'),
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'rent'
        verbose_name_plural = 'rents'

    @property
    def price(self):
        if not (self.date_to and self.date_from):
            raise ValueError
        return self.quantity * ((self.date_to - self.date_from).days + 1) * self.daily_payment

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser
from books.models import Items


class Statuses(models.Model):
    status = models.CharField(_('status'), max_length=50, unique=True, blank=False)

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')

    def __str__(self):
        return self.status


class Invoices(models.Model):
    user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name=_('user'))
    status = models.ForeignKey(to=Statuses, on_delete=models.PROTECT, verbose_name=_('status'))
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    status_updated = models.DateTimeField(_('status updated'), default=timezone.now)

    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')

    def __str__(self):
        return f'{self.user_id}-{self.status}'


class Services(models.Model):
    item = models.ForeignKey(to=Items, on_delete=models.CASCADE, verbose_name=_('item'))
    order = models.ForeignKey(to=Invoices, on_delete=models.CASCADE, verbose_name=_('order'))
    quantity = models.PositiveSmallIntegerField(_('quantity'), default=1, blank=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.__class__.__name__}-{self.item.title}'


class Purchases(Services):

    class Meta:
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'


class Rents(Services):
    date_from = models.DateField(_('Date from'), default=timezone.now)
    date_to = models.DateField(_('Date to'))
    percentage_per_day = models.FloatField(_('percentage per day'), default=0.1, blank=False, null=False)

    class Meta:
        verbose_name = 'rent'
        verbose_name_plural = 'rents'

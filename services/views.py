import datetime
import logging
from http.client import HTTPResponse

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, CreateView, FormView, ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy

from accounts.models import CustomUser
from books.models import Item
from services.forms import RentForm
from services.models import Rent, Purchase, Invoice


logger = logging.getLogger('book_store')


class PurchaseView(LoginRequiredMixin, SuccessMessageMixin, View):
    success_message = _('Товар %s (%s) добавлен в корзину')
    model = Purchase
    login_url = reverse_lazy('accounts:login')

    def get(self, request, **kwargs):
        return redirect('books:item', Item.objects.get(pk=kwargs['pk']).slug)

    @transaction.atomic
    def post(self, request, **kwargs):
        item = Item.objects.get(pk=kwargs['pk'])
        quantity = int(request.POST['quantity'])
        if item.count_available >= quantity:
            invoice, created = Invoice.objects.get_or_create(
                user_id=CustomUser.objects.get(pk=request.user.id),
                status='Ожидает оплаты'
            )
            Purchase(item=item, invoice=invoice, quantity=quantity).save()
            item.count_available -= quantity
            item.save()
            messages.success(self.request, self.success_message % (item, quantity))
            self.email_add_rent(request, {'item': item})
            return redirect('services:cart')
        messages.error(self.request, _('Неверное количество товара'))
        return redirect(request.META['HTTP_REFERER'])

    def email_add_rent(self, request, data):
        subject = _(f'Add {data["item"]} to cart')
        current_site = get_current_site(request)
        message = render_to_string('services/email_add_to_cart.html', {
            'user': self.request.user,
            'data': data,
            'current_site': current_site,
            'cart_link': request.build_absolute_uri(reverse('services:cart'))
        })
        request.user.email_user(subject, message)


class RentView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    success_message = _('Товар %s добавлен в корзину')
    model = Rent
    template_name = 'services/rent.html'
    form_class = RentForm
    success_url = reverse_lazy('services:cart')
    percent_of_price = 0.1

    def get(self, request, *args, **kwargs):
        self.object = None
        item = get_object_or_404(Item, pk=kwargs['pk'])
        kwargs['form'] = RentForm(initial={
            'item': f'{item.pk} {item.title}',
            'daily_payment': item.price * self.percent_of_price,
            'date_from': timezone.now(),
            'date_to': timezone.now() + datetime.timedelta(days=1),
        })
        # return super(RentView, self).get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data(**kwargs))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {
            'item': Item.objects.get(pk=self.request.POST['item'].split()[0]),
            'date_from': datetime.datetime(year=int(self.request.POST['date_from_year']),
                                           month=int(self.request.POST['date_from_month']),
                                           day=int(self.request.POST['date_from_day'])),
            'date_to': datetime.datetime(year=int(self.request.POST['date_to_year']),
                                         month=int(self.request.POST['date_to_month']),
                                         day=int(self.request.POST['date_to_day'])),
            'daily_payment': self.request.POST['daily_payment'],
        }
        form = RentForm(data=data)
        if form.is_valid():
            item = form.cleaned_data['item']
            if item.count_available >= 1:
                invoice, created = Invoice.objects.get_or_create(
                    user_id=CustomUser.objects.get(pk=request.user.id),
                    status='Ожидает оплаты'
                )
                Rent(item=item,
                     invoice=invoice,
                     quantity=1,
                     date_from=form.cleaned_data['date_from'],
                     date_to=form.cleaned_data['date_to'],
                     daily_payment=item.price * self.percent_of_price).save()
                item.count_available -= 1
                item.save()
                messages.success(self.request, self.success_message % item.title)
                self.email_add_rent(request, form.cleaned_data)
                return redirect('services:cart')
            messages.error(self.request, _('Товар отсутствует на складе в данный момент'))
            return redirect(request.META['HTTP_REFERER'])

    def email_add_rent(self, request, data):
        subject = f'Add {data["item"]} to cart'
        current_site = get_current_site(request)
        message = render_to_string('services/email_add_to_cart.html', {
            'user': self.request.user,
            'data': data,
            'current_site': current_site,
            'cart_link': request.build_absolute_uri(reverse('services:cart'))
        })
        request.user.email_user(subject, message)


class CartView(LoginRequiredMixin, View):

    def get(self, request):
        try:
            invoice = Invoice.objects.get(
                user_id=request.user.id,
                status='Ожидает оплаты')
        except Invoice.DoesNotExist:
            messages.warning(request, _('Вы еще ничего не добавили в корзину'))
            invoice = None
            # if request.META.get('HTTP_REFERER', False):
            #     if request.META['HTTP_REFERER'] == request.build_absolute_uri():
            #         return redirect('books:home')
            #     return redirect(request.META['HTTP_REFERER'])
            # return redirect('books:home')
        context = {
            'invoice': invoice
        }
        return render(request, 'services/cart.html', context)

    @transaction.atomic
    def post(self, request):
        invoice = Invoice.objects.get(
            user_id=request.user.id,
            status='Ожидает оплаты')
        invoice.status = 'Оплачен'
        invoice.save()
        messages.info(request, _('Заказ оплачен'))
        logger.info(f'Invoice {invoice} paid.')
        self.email_payment_done(request, invoice)
        return redirect('books:home')

    def email_payment_done(self, request, invoice):
        current_site = get_current_site(request)
        subject = 'Payment is done!'
        message = render_to_string('services/email_payment_done.html', {
            'user': self.request.user,
            'invoice': invoice,
            'current_site': current_site,
        })
        request.user.email_user(subject, message)


def delete_service(request, **kwargs):
    service_id = kwargs['pk']
    service_type = kwargs['service']
    if service_type == 'purchase':
        Purchase.objects.get(id=service_id).delete()
    elif service_type == 'rent':
        Rent.objects.get(id=service_id).delete()
    return redirect('services:cart')


class HistoryListView(ListView):
    model = Purchase
    template_name = 'services/history.html'

    def get_context_data(self, **kwargs):
        object_list = Purchase.objects.filter(invoice__user_id=self.request.user.id).exclude(invoice__status='Отменен')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['rents'] = Rent.objects.filter(invoice__user_id=self.request.user.id).exclude(invoice__status='Отменен')
        return context

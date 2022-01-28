import datetime
from http.client import HTTPResponse

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, CreateView, FormView, ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy

from accounts.models import CustomUser
from books.models import Item
from services.forms import RentForm
from services.models import Rent, Purchase, Invoice


class PurchaseView(SuccessMessageMixin, View):
    success_message = _('Товар %s (%s) добавлен в корзину')
    model = Purchase

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
            return redirect('services:cart')
        messages.error(self.request, _('Неверное количество товара'))
        return redirect(request.META['HTTP_REFERER'])


class RentView(SuccessMessageMixin, FormView):
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
                return redirect('services:cart')
            messages.error(self.request, _('Товар отсутствует на складе в данный момент'))
            return redirect(request.META['HTTP_REFERER'])


class CartView(View):

    def get(self, request):
        try:
            invoice = Invoice.objects.get(
                user_id=CustomUser.objects.get(pk=request.user.id),
                status='Ожидает оплаты')
        except Invoice.DoesNotExist:
            messages.warning(request, _('Вы еще ничего не добавили в корзину'))
            try:
                # TODO: Переделать ссылку и возможно сам алгоритм
                if request.META['HTTP_REFERER'] == 'http://' + request.get_host() + reverse('services:cart'):
                    return redirect('books:home')
                return redirect(request.META['HTTP_REFERER'])
            except KeyError:
                return redirect('books:home')
        context = {
            'invoice': invoice
        }
        return render(request, 'services/cart.html', context)


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


from django.http import Http404
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext as _

from .models import Item, Book, Magazine, Figure


class ItemsListView(ListView):
    model = Item
    paginate_by = 30
    ordering = [
        'price'
    ]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemsListView, self).get_context_data(object_list=object_list, **kwargs)
        context.update({
            'title': 'Items'
        })
        return context


class ItemDetailView(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.object
        })
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.prefetch_related().get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class CategoryListView(ListView):
    model = Item

    def get_queryset(self):
        if self.kwargs['cat'] == 'Все':
            return self.model.objects.all()
        return self.model.objects.filter(category__name=self.kwargs['cat'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.kwargs['cat']
        })
        return context


class TypeListView(ListView):
    model = Item
    template_name = 'books/item_list.html'

    def get_queryset(self):
        if self.kwargs['type'] == 'Все товары':
            return self.model.objects.all()
        self.get_type()
        return self.model.objects.all()

    def get_type(self):
        if self.kwargs['type'] == 'Книги':
            self.model = Book
        elif self.kwargs['type'] == 'Журналы':
            self.model = Magazine
        elif self.kwargs['type'] == 'Фигурки':
            self.model = Figure

    def get_context_object_name(self, object_list):
        return 'item_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.kwargs['type']
        })
        return context

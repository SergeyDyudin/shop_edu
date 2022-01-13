from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Item, Book, Author, Category, Genre, Publisher, Language, Brand, Figure, Magazine


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', )
    }
    list_display = [
        'title',
        'count_available',
        'price',
    ]


class AuthorInline(admin.StackedInline):
    model = Book.author.through
    extra = 0
    verbose_name = _('author')
    verbose_name_plural = _('authors')
    fields = []


class BookInline(admin.StackedInline):
    model = Book.author.through
    extra = 0
    verbose_name = _('book')
    verbose_name_plural = _('books')


class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'get_authors',
        'price'
    ]
    prepopulated_fields = {
        'slug': ('title', )
    }
    inlines = [
        AuthorInline
    ]
    filter_horizontal = [
        'genre',
        'category'
    ]
    exclude = ('author',)


class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline
    ]


class MagazineAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', 'date')
    }
    filter_horizontal = [
        'category'
    ]


class FigureAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', )
    }
    filter_horizontal = [
        'category'
    ]


class BrandAdmin(admin.ModelAdmin):
    pass


admin.site.register(Item, ItemAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Publisher)
admin.site.register(Language)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Figure, FigureAdmin)
admin.site.register(Magazine, MagazineAdmin)

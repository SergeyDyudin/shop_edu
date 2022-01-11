from django.contrib import admin

from .models import Items, Books, Authors, Categories, Genres, Publishers, Languages


class ItemsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', )
    }


class AuthorsInline(admin.StackedInline):
    model = Books.author.through
    extra = 0
    verbose_name = 'author'
    verbose_name_plural = 'authors'
    fields = []


class BooksInline(admin.StackedInline):
    model = Books.author.through
    extra = 0
    verbose_name = 'book'
    verbose_name_plural = 'books'


class BooksAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', )
    }
    inlines = [
        AuthorsInline
    ]
    filter_horizontal = [
        'genre',
        'category'
    ]
    exclude = ('author',)


class AuthorsAdmin(admin.ModelAdmin):
    inlines = [
        BooksInline
    ]


admin.site.register(Items, ItemsAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(Authors, AuthorsAdmin)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Publishers)
admin.site.register(Languages)

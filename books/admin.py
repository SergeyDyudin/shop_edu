from django.contrib import admin

from .models import Items, Books, Authors, Categories, Genres, Publishers, Languages, Brands, Figures, Magazines


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
    list_display = [
        'title',
        'get_authors',
        'price'
    ]
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


class MagazinesAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', 'date')
    }
    filter_horizontal = [
        'category'
    ]


class FiguresAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', )
    }
    filter_horizontal = [
        'category'
    ]


class BrandsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Items, ItemsAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(Authors, AuthorsAdmin)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Publishers)
admin.site.register(Languages)
admin.site.register(Brands, BrandsAdmin)
admin.site.register(Figures, FiguresAdmin)
admin.site.register(Magazines, MagazinesAdmin)

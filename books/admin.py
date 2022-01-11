from django.contrib import admin

from .models import Items, Books, Authors, Categories, Genres, Publishers, Languages


class ItemsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', )
    }


class BooksAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', )
    }


admin.site.register(Items, ItemsAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(Authors)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Publishers)
admin.site.register(Languages)

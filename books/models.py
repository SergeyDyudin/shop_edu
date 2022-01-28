from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils.utils import transliterate_string


class Language(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=30)

    class Meta:
        unique_together = ['code', 'name']
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(_('publisher'), unique=True, max_length=100)
    address = models.TextField(_('address'))

    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(_('author'), max_length=50, blank=False)
    description = models.TextField(_('description'), blank=True)
    photo = models.ImageField(verbose_name=_("author's photo"), upload_to='books/authors_photo', blank=True, null=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(_('genre'), max_length=30, unique=True, blank=False)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(_('category'), max_length=50, blank=True, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=70, unique=True, blank=False)
    description = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(_('title'), max_length=70)
    description = models.TextField(_('description'), blank=True)
    category = models.ManyToManyField(to=Category, blank=True)
    count_available = models.PositiveSmallIntegerField(_('count available'), default=0, blank=False)
    price = models.PositiveIntegerField(_('price'))
    photo = models.ImageField(verbose_name=_('photo'), upload_to='items/photo/', blank=True, null=True)
    slug = models.SlugField(_('URL'), unique=True, blank=False)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.title

    def save_with_slug(self, *args, **kwargs):
        self.slug = transliterate_string(self.title.lower())
        super(Item, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books:item', kwargs={'slug': self.slug})


class Book(Item):
    author = models.ManyToManyField(to=Author)
    genre = models.ManyToManyField(to=Genre)
    language = models.ForeignKey(to=Language, on_delete=models.CASCADE, verbose_name=_('language'))
    publisher = models.ForeignKey(to=Publisher, on_delete=models.CASCADE, verbose_name=_('publisher'))
    year = models.DateField(verbose_name=_('year'))

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    @admin.display(description='Author')
    def get_authors(self):
        return ', '.join([author.name for author in self.author.all()])


class Magazine(Item):
    date = models.DateField(verbose_name=_('date'), default=timezone.now)
    number = models.PositiveSmallIntegerField(_('magazine number'), blank=True, null=True)
    language = models.ForeignKey(to=Language, on_delete=models.CASCADE, verbose_name=_('language'))

    class Meta:
        verbose_name = 'magazine'
        verbose_name_plural = 'magazines'

    def __str__(self):
        return f'[{self.date}] {self.title}'


class Figure(Item):
    character = models.CharField(max_length=80, blank=True)
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=80, blank=True)

    class Meta:
        verbose_name = 'figure'
        verbose_name_plural = 'figures'

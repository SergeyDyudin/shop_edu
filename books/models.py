from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# TODO пересмотреть Items.save_with_slug()
alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


class Items(models.Model):
    title = models.CharField(_('title'), max_length=70)
    description = models.TextField(_('description'), max_length=250)
    price = models.PositiveIntegerField(_('price'))
    available = models.PositiveSmallIntegerField(_('available'), default=0, blank=False)
    slug = models.SlugField(_('URL'), unique=True, blank=False)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.title

    def save_with_slug(self, *args, **kwargs):
        self.slug = slugify(''.join(alphabet.get(w, w) for w in self.title.lower()))
        super(Items, self).save(*args, **kwargs)


class Languages(models.Model):
    code = models.CharField(max_length=5)
    language = models.CharField(max_length=30)

    class Meta:
        unique_together = ['code', 'language']
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.language


class Publishers(models.Model):
    name = models.CharField(_('publisher'), max_length=100)
    address = models.TextField(_('address'))

    class Meta:
        unique_together = ['name', 'address']
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.name


class Authors(models.Model):
    name = models.CharField(_('author'), max_length=50, blank=False)
    description = models.TextField(_('description'), blank=True)
    photo = models.ImageField(verbose_name=_("author's photo"), upload_to='books/authors_photo', blank=True, null=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(_('genre'), max_length=30, unique=True, blank=False)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(_('category'), max_length=50, blank=True, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Books(Items):
    author = models.ManyToManyField(to=Authors)
    genre = models.ManyToManyField(to=Genres)
    category = models.ManyToManyField(to=Categories)
    language = models.ForeignKey(to=Languages, on_delete=models.CASCADE, verbose_name=_('language'))
    publisher = models.ForeignKey(to=Publishers, on_delete=models.CASCADE, verbose_name=_('publisher'))
    year = models.DateField(verbose_name=_('year'))
    cover = models.ImageField(verbose_name=_('cover'), upload_to='books/cover/', blank=True, null=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

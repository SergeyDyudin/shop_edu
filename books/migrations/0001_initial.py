# Generated by Django 4.0 on 2022-01-11 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='author')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='books/authors_photo', verbose_name="author's photo")),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, unique=True, verbose_name='category')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='genre')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='title')),
                ('description', models.TextField(max_length=250, verbose_name='description')),
                ('price', models.PositiveIntegerField(verbose_name='price')),
                ('available', models.PositiveSmallIntegerField(default=0, verbose_name='available')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='Publishers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='publisher')),
                ('address', models.TextField(verbose_name='address')),
            ],
            options={
                'unique_together': {('name', 'address')},
                'verbose_name': 'Publisher',
                'verbose_name_plural': 'Publishers',
            },
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('language', models.CharField(max_length=30)),
            ],
            options={
                'unique_together': {('code', 'language')},
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('items_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='books.items')),
                ('year', models.DateField(verbose_name='year')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='books/cover/', verbose_name='cover')),
                ('author', models.ManyToManyField(to='books.Authors')),
                ('category', models.ManyToManyField(to='books.Categories')),
                ('genre', models.ManyToManyField(to='books.Genres')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.languages', verbose_name='language')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.publishers', verbose_name='publisher')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
            bases=('books.items',),
        ),
    ]

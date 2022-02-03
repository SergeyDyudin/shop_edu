from django import template

from books.models import Category


register = template.Library()


@register.inclusion_tag('books/categories.html')
def list_category(user):
    return {'cats': Category.objects.adult_control(user).all()}


@register.inclusion_tag('books/types.html')
def list_type():
    return {'types': ['Все товары', 'Книги', 'Журналы', 'Фигурки']}

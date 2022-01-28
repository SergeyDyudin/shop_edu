from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.ItemsListView.as_view(), name='home'),
    path('category/<str:cat>', views.CategoryListView.as_view(), name='category'),
    path('type/<str:type>', views.TypeListView.as_view(), name='type'),
    path('<slug:slug>/', views.ItemDetailView.as_view(), name='item')
]

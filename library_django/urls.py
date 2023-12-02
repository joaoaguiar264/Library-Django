from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search-book/', views.search_book, name='search_book'),
    path('add-book/', views.add_book, name='add_book'),
    path('loaned-books/', views.loaned_books, name='loaned_books'),
    path('lend-book/<int:id>', views.lend_book, name='lend_book'),
    path('return-book/<int:id>', views.return_book, name='return_book')
]
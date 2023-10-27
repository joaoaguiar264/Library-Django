from django.shortcuts import render, redirect
from .models import Books, Genres
from random import randint
from datetime import datetime

def index(request):
    books = Books.objects.all()
    return render(request, 'pages/index.html', {'books':books})


def add_book(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        genre = request.POST.get('genre')
        image = request.FILES.get('image')
        pages_number = request.POST.get('pages_number')
        quantity = request.POST.get('quantity')
        in_stock = True

        Books.objects.create(
            name = name,
            genre_id = genre,
            image = image,
            pages_number = pages_number,
            quantity = quantity,
            in_stock = in_stock
        )
        return redirect('home')
    else:
        genres = Genres.objects.all()
        return render(request, 'pages/add-book.html', {'genres':genres})
    
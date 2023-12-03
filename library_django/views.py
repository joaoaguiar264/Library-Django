from django.shortcuts import render, redirect
from .models import Books, Genres, LoanedBooks
from random import randint
from .utils import send_email
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='login')

def index(request):
    books = Books.objects.all()
    return render(request, 'pages/index.html', {'books':books})

def out_stock(request):    
    books = Books.objects.filter(in_stock=False)
    return render(request, 'pages/index.html', {'books':books})

def search_book(request):
    q = request.GET.get('q')
    books = Books.objects.filter(name__icontains=q)
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
    
def loaned_books(request):
    loanedBooks = LoanedBooks.objects.filter(user_id=request.user.id, returned=False)
    books = []
    for livroEmprestado in loanedBooks:
        books.append(livroEmprestado.book)
    
    return render(request, 'pages/loaned-books.html', {'books':books})

def lend_book(request, id):
    book = Books.objects.get(id=id)
    book.quantity -= 1
    LoanedBooks.objects.create(
        user_id=request.user.id,
        book_id=id
    )
    dt = datetime.now()
    newDt = dt.replace(microsecond=0)
    send_email("Book Loan", f"You just borrowed the book {book.name}\n{newDt}", request.user.email)

    if book.quantity == 0:
        book.in_stock = False
    
    book.save()
    return redirect('home')

def return_book(request, id):
    loanedBooks = LoanedBooks.objects.filter(user_id=request.user.id, book_id=id, returned=False)
    loanedBook = loanedBooks[0]
    loanedBook.returned = True
    loanedBook.save()

    book = Books.objects.get(id=id)
    if not book.in_stock:
        book.in_stock = True
    book.quantity += 1
    book.save()
    
    return redirect('loaned_books')
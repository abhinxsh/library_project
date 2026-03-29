

# Create your views here.
# books/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book

def index(request):
    query = request.GET.get('q', '')
    
    if query:
        books = Book.objects.filter(
            title__icontains=query
        ) | Book.objects.filter(
            author__icontains=query
        )
    else:
        books = Book.objects.all().order_by('-id')

    return render(request, 'books/index.html', {
        'books': books,
        'query': query
    })


def add_book(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        quantity = int(request.POST['quantity'])

        Book.objects.create(title=title, author=author, quantity=quantity)
    return redirect('index')


def update_book(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.quantity = int(request.POST['quantity'])
        book.save()

    return redirect('index')


def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('index')
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book


# ── Frontend Page ───────────────────────────────────────
def index(request):
    return render(request, 'books/index.html')


# ── API: GET + POST ─────────────────────────────────────
@csrf_exempt
def api_books(request):
    if request.method == "GET":
        books = list(Book.objects.values())
        return JsonResponse(books, safe=False)

    if request.method == "POST":
        data = json.loads(request.body)

        book = Book.objects.create(
            title=data.get("title", ""),
            author=data.get("author", ""),
            quantity=data.get("quantity", 0)
        )

        return JsonResponse({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "quantity": book.quantity
        })


# ── API: PUT + DELETE ───────────────────────────────────
@csrf_exempt
def api_book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)

        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.quantity = data.get("quantity", book.quantity)
        book.save()

        return JsonResponse({"status": "updated"})

    if request.method == "DELETE":
        book.delete()
        return JsonResponse({"status": "deleted"})

    return JsonResponse({"error": "Invalid method"}, status=405)
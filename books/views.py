from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from .models import Book


# ── Hardcoded credentials ────────────────────────────────
# Change these to your real credentials
CREDENTIALS = {
    "admin@library.com": {"password": "admin123", "role": "admin"},
    "user@library.com":  {"password": "user123",  "role": "user"},
    # Add more users here:
    # "staff@library.com": {"password": "pass456", "role": "user"},
}


# ── Auth helpers ─────────────────────────────────────────
def get_role_from_session(request):
    return request.session.get("role")

def is_admin(request):
    return get_role_from_session(request) == "admin"

def is_authenticated(request):
    return get_role_from_session(request) in ("admin", "user")

def auth_required(view_fn):
    def wrapper(request, *args, **kwargs):
        if not is_authenticated(request):
            return JsonResponse({"error": "Authentication required"}, status=401)
        return view_fn(request, *args, **kwargs)
    return wrapper

def admin_required(view_fn):
    def wrapper(request, *args, **kwargs):
        if not is_authenticated(request):
            return JsonResponse({"error": "Authentication required"}, status=401)
        if not is_admin(request):
            return JsonResponse({"error": "Admin access required"}, status=403)
        return view_fn(request, *args, **kwargs)
    return wrapper


# ── Frontend Page ────────────────────────────────────────
@ensure_csrf_cookie  # forces Django to set csrftoken cookie on every page load
def index(request):
    return render(request, 'books/index.html')


# ── Auth: Login / Logout ─────────────────────────────────
@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data     = json.loads(request.body)
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = CREDENTIALS.get(email)

    if not user or user["password"] != password:
        return JsonResponse({"error": "Invalid email or password"}, status=401)

    request.session["role"]  = user["role"]
    request.session["email"] = email

    return JsonResponse({"role": user["role"], "email": email})


@csrf_exempt
def api_logout(request):
    request.session.flush()
    return JsonResponse({"status": "logged out"})


# ── Auth: Session status ──────────────────────────────────
def api_me(request):
    role  = request.session.get("role")
    email = request.session.get("email")
    if not role:
        return JsonResponse({"authenticated": False}, status=401)
    return JsonResponse({"authenticated": True, "role": role, "email": email})


# ── API: GET (all users) + POST (admin only) ─────────────
@csrf_exempt
@auth_required
def api_books(request):
    if request.method == "GET":
        books = list(Book.objects.values())
        return JsonResponse(books, safe=False)

    if request.method == "POST":
        if not is_admin(request):
            return JsonResponse({"error": "Admin access required"}, status=403)

        data = json.loads(request.body)
        book = Book.objects.create(
            title=data.get("title", ""),
            author=data.get("author", ""),
            quantity=data.get("quantity", 0)
        )
        return JsonResponse({
            "id":       book.id,
            "title":    book.title,
            "author":   book.author,
            "quantity": book.quantity
        })

    return JsonResponse({"error": "Method not allowed"}, status=405)


# ── API: PUT + DELETE (admin only) ───────────────────────
@csrf_exempt
@admin_required
def api_book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        book.title    = data.get("title",    book.title)
        book.author   = data.get("author",   book.author)
        book.quantity = data.get("quantity", book.quantity)
        book.save()
        return JsonResponse({"status": "updated"})

    if request.method == "DELETE":
        book.delete()
        return JsonResponse({"status": "deleted"})

    return JsonResponse({"error": "Invalid method"}, status=405)